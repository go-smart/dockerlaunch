import pytest
import asyncio.coroutines
import asyncio
from unittest.mock import MagicMock
import uuid

from dockerlaunch.layer import DockerLayer

import docker
import tempfile


known_guid = str(uuid.uuid4()).upper()
unknown_guid = str(uuid.uuid4()).upper()


def magic_coro():
    mock = MagicMock()
    return mock, asyncio.coroutine(mock)


@asyncio.coroutine
def wait():
    pending = asyncio.Task.all_tasks()
    relevant_tasks = [t for t in pending if ('test_' not in t._coro.__name__)]
    yield from asyncio.gather(*relevant_tasks)


@pytest.fixture(scope="function")
def launchlayer(monkeypatch):
    allowed_images = MagicMock()
    logger = MagicMock()
    script_filename = MagicMock()
    max_containers = MagicMock()
    docker_socket = MagicMock()
    shutdown_timeout = MagicMock()
    monkeypatch.setattr('docker.Client', lambda version, base_url: 2123456)
    launchlayer = DockerLayer(allowed_images, logger, script_filename,
                              max_containers, docker_socket, shutdown_timeout)
    launchlayer.launchlayer = MagicMock()
    return launchlayer


#   def init has nothing to test ...

def test_init_(monkeypatch, launchlayer):
    random_allowed_images = MagicMock()
    random_logger = MagicMock()
    random_script_filename = MagicMock()
    random_max_containers = MagicMock()
    random_docker_socket = MagicMock()
    random_shutdown_timeout = MagicMock()
    launchlayer._allowed_images = MagicMock()
    launchlayer._logger = MagicMock()
    launchlayer._script_filename = MagicMock()
    launchlayer._max_containers = MagicMock()
    launchlayer._docker_socket = MagicMock()
    launchlayer._shutdown_timeout = MagicMock()    
    launchlayer._bridges = MagicMock()    
    random_max_containers = 10
    random_docker_socket = None
    random_shutdown_timeout = 5
    monkeypatch.setattr('os.getuid', lambda: 123456)
    monkeypatch.setattr('os.getgid', lambda: 123456)
    monkeypatch.setattr('docker.Client', lambda version, base_url: 123456)
    launchlayer.__init__(
        random_allowed_images, random_logger,
        random_script_filename, random_max_containers, random_docker_socket,
        random_shutdown_timeout)
    # launchlayer._logger.info.assert_called_with(
    #   "Trying to connect to Docker as %d:%d", os.getuid(), os.getgid()
    # )
    launchlayer._docker_client = docker.Client(
        base_url=launchlayer._docker_socket,
        version='auto'
    )
    launchlayer._logger.info.assert_called_with("New Docker layer created")


def test_quatro(monkeypatch, launchlayer):
    launchlayer.destroy = MagicMock()
    launchlayer._container_id = MagicMock()
    launchlayer._docker_client = MagicMock()
    launchlayer._container_id = True
    launchlayer._docker_client.containers.return_value = 'AAA'
    launchlayer._docker_client.logs.return_value = 'BBB'
    launchlayer.__del__()
    result1 = launchlayer.get_container_id()
    result2 = launchlayer.get_container_count()
    result3 = launchlayer.get_container_logs()
    launchlayer.destroy.assert_called_with()
    launchlayer._docker_client.containers.assert_called_with()
    launchlayer._docker_client.logs.assert_called_with(True)
    assert(result1 is True)
    assert(result2 == 3)
    assert(result3 == 'BBB')


def test_try_launch(monkeypatch, launchlayer):
    random_image = MagicMock()
    random_data_location = MagicMock()
    random_update_socket = MagicMock()
    launchlayer._allowed_images = MagicMock()
    launchlayer._docker_client = MagicMock()
    launchlayer._logger.info = MagicMock()
    launchlayer._max_containers = MagicMock()
    launchlayer._launch = MagicMock()
    launchlayer._script_filename = MagicMock()
    launchlayer._logger = MagicMock()
    launchlayer._container_id = MagicMock()
    launchlayer._temporary_directory = MagicMock()
    launchlayer._output_directory = MagicMock()
    launchlayer._input_directory = MagicMock()
    random_update_socket = None
    random_image = 'img1'
    launchlayer._allowed_images = {'img1': 'pic1'}
    launchlayer._docker_client.containers.return_value = '1234567'
    launchlayer._max_containers = 100 + 7
    tdir = MagicMock()
    tdir.name = 'name1'
    launchlayer._launch.return_value = (
        'id1',
        tdir,
        'outdir1',
        'indir',
        'socket1')
    result = launchlayer.try_launch(random_image, random_data_location,
                                    random_update_socket)
    assert(result == (
        True, {
            'volume location': 'name1',
            'output subdirectory': 'outdir1',
            'input subdirectory': 'indir',
            'update socket available': 'socket1'
        }
    ))


def test_wait(monkeypatch, launchlayer):
    random_timeout = MagicMock()
    random_destroy = MagicMock()
    launchlayer._container_id = MagicMock()
    launchlayer._bridges = MagicMock()
    launchlayer._wait = MagicMock()
    launchlayer._docker_client = MagicMock()
    launchlayer._logger = MagicMock()
    random_destroy = False
    launchlayer._container_id = 'id1'
    launchlayer._bridges = {'id1': 'AAA'}
    launchlayer._wait.return_value = 'container1'
    result = launchlayer.wait(random_timeout, random_destroy)
    assert (result == (True, "Exited"))


def test_destroy(monkeypatch, launchlayer):
    launchlayer.wait = MagicMock()
    launchlayer._shutdown_timeout = MagicMock()
    launchlayer.wait = MagicMock()
    launchlayer.wait.return_value = True
    result = launchlayer.destroy()
    assert (result is True)


def test_launch(monkeypatch, launchlayer):
    random_c = MagicMock()
    random_docker_image = MagicMock()
    random_data_location = MagicMock()
    random_script_filename = MagicMock()
    random_logger = MagicMock()
    random_update_socket = MagicMock()
    tdir = MagicMock()
    tdir.name = 'name1'
    monkeypatch.setattr('tempfile.TemporaryDirectory', lambda: tdir)
    monkeypatch.setattr('docker.utils.compare_version', lambda q1, q2: -3)
    monkeypatch.setattr('os.chmod', lambda p1, p2: 'aaa')
    monkeypatch.setattr('os.makedirs', lambda p3: 'bbb')
    monkeypatch.setattr('re.sub', lambda p4, p5, p6: 'bbb')
    random_c.create_container.return_value = {'Id': 'id1'}
    random_c.start.return_value = 'start1'
    tempfile.TemporaryDirectory.return_value = 'dir1'
    result = launchlayer._launch(
        random_c,
        random_docker_image,
        random_data_location,
        random_script_filename,
        random_logger,
        random_update_socket)
    assert(result == 'id1', 'dir1', 'output', 'input', True)


def test___wait__(monkeypatch, launchlayer):
    random_c = MagicMock()
    random_container_id = MagicMock()
    random_timeout = MagicMock()
    random_logger = MagicMock()
    random_destroy = MagicMock()
    random_bridge_id = MagicMock()
    random_destroy = True
    random_bridge_id = True
    random_c.wait.return_value = True
    random_c.remove_container.return_value = True
    random_c.stop.return_value = True
    result = launchlayer._wait(
        random_c,
        random_container_id,
        random_timeout,
        random_logger,
        random_destroy,
        random_bridge_id)
    assert(result is True)
