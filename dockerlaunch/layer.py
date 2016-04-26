import docker
import tempfile
import requests
import os
import traceback
import re


class DockerLayer:
    _docker_socket = 'unix://var/run/docker.sock'
    _container_id = None
    _container_info = None

    def __init__(self, allowed_images, logger, script_filename,
                 max_containers=10,
                 docker_socket=None, shutdown_timeout=5,
                 data_container='glossiaserverside_data_1',
                 allow_host_mounting=False):
        self._logger = logger
        if docker_socket is not None:
            self._docker_socket = docker_socket

        self._allowed_images = allowed_images
        self._max_containers = max_containers
        self._data_container = data_container
        self._allow_host_mounting = allow_host_mounting

        self._logger.info("Trying to connect to Docker as %d:%d",
                          os.getuid(), os.getgid())

        self._docker_client = docker.Client(base_url=self._docker_socket,
                                            version='auto')
        self._shutdown_timeout = shutdown_timeout
        self._script_filename = script_filename
        self._bridges = {}

        self._logger.info("New Docker layer created")

    def __del__(self):
        self.destroy()

    def get_container_id(self):
        return self._container_id

    def get_container_info(self):
        if not self._container_info and self._container_id:
            self._container_info = self._docker_client.inspect_container(self._container_id)
        return self._container_info

    def get_image_id(self):
        container_info = self.get_container_info()
        if container_info and 'Image' in container_info:
            return container_info['Image']

        return None

    def get_container_count(self):
        if self._docker_client:
            return len(self._docker_client.containers())

        return None

    def get_container_logs(self, only=None):
        if self._docker_client and self._container_id:
            if only == 'stdout':
                return self._docker_client.logs(self._container_id, stdout=True, stderr=False).decode('UTF-8')
            elif only == 'stderr':
                return self._docker_client.logs(self._container_id, stdout=False, stderr=True).decode('UTF-8')
            elif only is None:
                return {h: self.get_container_logs(only=h) for h in ('stdout', 'stderr')}

        return None

    def try_launch(self, image, data_location, update_socket=None):
        if image not in self._allowed_images:
            return False, "This image is not a whitelisted image for dockerlaunch"

        c = self._docker_client
        container_count = len(c.containers())
        self._logger.info("Currently %d containers" % container_count)

        if len(c.containers()) > self._max_containers:
            return False, ("Too many containers (max: %d)" % self._max_containers)
        else:
            container_id, temporary_directory, output_directory, input_directory, socket_available, bridge_id = \
                self._launch(
                    c,
                    image,
                    data_location,
                    self._data_container,
                    self._script_filename,
                    self._logger,
                    update_socket
                )

            self._container_id = container_id
            self._temporary_directory = temporary_directory
            self._output_directory = output_directory
            self._input_directory = input_directory
            self._bridges[self._container_id] = bridge_id

            return True, {
                'volume location': temporary_directory.name,
                'output subdirectory': output_directory,
                'input subdirectory': input_directory,
                'update socket available': socket_available
            }

    def wait(self, timeout, destroy=False):
        if self._container_id:
            if self._container_id in self._bridges:
                bridge_id = self._bridges[self._container_id]
            else:
                bridge_id = None

            try:
                container_destroyed = self._wait(
                    self._docker_client,
                    self._container_id,
                    timeout,
                    self._logger,
                    destroy=destroy,
                    bridge_id=bridge_id
                )
            except Exception as e:
                self._logger.error(
                    "Did not complete while waiting (timeout %d): %s" %
                    (timeout, str(e))
                )
                return False, "Could not wait: %s" % str(e)
            else:
                if container_destroyed:
                    self._container_id = None

            return True, "Exited"
        else:
            return False, "No container currently associated"

    def destroy(self):
        return self.wait(self._shutdown_timeout, destroy=True)

    @staticmethod
    def _launch(c, docker_image, data_location, data_container, script_filename, logger, update_socket=None):
        # Cleaned when object that holds it (instance of DL class) is destroyed
        try:
            temporary_directory = tempfile.TemporaryDirectory()
        except Exception:
            traceback.print_exc()
            raise
        os.chmod(temporary_directory.name, 0o755)

        tmpdir = temporary_directory.name

        logger.info("Created temporary directory: %s" % tmpdir)

        output_suffix = 'output'
        output_directory = os.path.join(tmpdir, output_suffix)
        os.makedirs(output_directory)
        os.chmod(output_directory, 0o777)

        input_suffix = 'input'
        input_directory = os.path.join(tmpdir, input_suffix)
        os.makedirs(input_directory)

        print("FIXME: proper group permissions for input/output directories")

        os.chmod(input_directory, 0o777)

        logger.info("Changed permissions: %s" % tmpdir)

        # Hack to work around Docker API < 1.15
        volumes = ['/shared', '/docker-launch-inner.py']
        binds = {
        }

        logger.info("Set up docker API")
        environment = {}

        # TODO: should there be additional security checks before mounting this sock?
        # FIXME: at least that it is a socket, not a symlink and the unprivileged requester has write access
        if update_socket:
            #volumes.append(update_socket)
            #binds[update_socket] = {
            #    'bind': '/update.sock',
            #    'mode': 'rw'
            #}
            update_socket_available = True
            environment['GSSA_STATUS_SOCKET'] = '/shared/update.sock'
            logger.info("Set GSSA_STATUS_SOCKET to %s" % environment['GSSA_STATUS_SOCKET'])

        logger.info("About to start...")

        if docker.utils.compare_version('1.15', c._version) < 0:
            container = c.create_container(
                docker_image,
                volumes=volumes,
                environment=environment
            )
            container_id = container['Id']

            logger.info("Created container %s (old API)" % container_id)

            c.start(container_id, binds=binds, network_mode='none')
        else:
            config = c.create_host_config(
                binds=binds,
                network_mode='none'
            )
            container = c.create_container(
                docker_image,
                volumes=volumes,
                host_config=config,
                environment=environment
            )
            container_id = container['Id']

            logger.info("Created container %s" % container_id)

            c.start(container_id)

        logger.info("Started")

        data_location = re.sub(r'[^a-zA-Z0-9-_]', '_', data_location)
        bridge = c.create_container(
            'gosmart/glossia-bridge',
            command=[data_location],
            environment=environment
        )
        c.start(bridge, volumes_from=[data_container, container_id])
        logger.info("Bridge up")

        return container_id, temporary_directory, \
            output_suffix, input_suffix, update_socket_available, bridge['Id']

    @staticmethod
    def _wait(c, container_id, timeout, logger, destroy=False, bridge_id=None):
        logger.info("Waiting for %s" % container_id)

        destroyed = False

        try:
            c.wait(container_id, timeout)
        except requests.exceptions.Timeout:
            logger.info("...timed out")
        else:
            logger.info("Completed %s" % container_id)

        if destroy:
            c.remove_container(container_id, force=True)
            logger.info("Removed %s" % container_id)

            destroyed = True

        if bridge_id:
            c.stop(bridge_id)
            logger.info("Removed bridge %s" % bridge_id)

        return destroyed
