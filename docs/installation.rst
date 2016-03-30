Installation & Usage
====================

Installation is using an out-of-source CMake build:

Dependencies
------------

- Docker
- Python 3:
        - lockfile
        - `python-daemon <https://github.com/go-smart/python-daemon>`_ (Go-Smart version)
        - docker-py

These may be installed using (Ubuntu):

.. code-block:: bash

  sudo apt-get install docker.io
  sudo pip3 install lockfile \
    git+git://github.com/numa-engineering/python-daemon.git@master \
    docker-py

Installation
------------

.. code-block:: bash

  git clone https://github.com/go-smart/dockerlaunch.git
  mkdir dockerlaunch-build
  cd dockerlaunch-build
  cmake ../dockerlaunch-build
  make
  sudo make install

This will create a ``dockerlaunch`` user and group,
and add the ``dockerlaunch`` user to the Docker group.
Note that this gives the ``dockerlaunch`` user access
to the ``/var/run/docker.sock`` socket and, through
a complex but plausible set of steps, root access.
As such, care should be taken about any activity involving
the ``dockerlaunch`` user.

However, the ``dockerlaunch``
**group** is intended only to allow access to the
``/var/run/dockerlaunch/dockerlaunch.sock`` socket -
adding a user to this allows them to issue dockerlaunch
commands, without consequently being able to directly access
Docker's socket. Bear in mind that your protection against
exploitation is limited to the security of the dockerlaunch
daemon - please make your own analysis accordingly.

NO WARRANTY is provided, implied or otherwise, and use
of ``dockerlaunch`` is entirely at the user's risk.

Usage
-----

Ensure Docker is running (on Ubuntu, ``sudo service docker start``).
The dockerlaunch daemon may be started using the command:

.. code-block:: bash

  sudo dockerlaunchd start

Once started, it also accepts ``stop`` and ``restart``
arguments. It will provide a small amount of diagnostic
output to stdout.

Note that, if Docker is restarted, dockerlaunch will
also need restarted (and consequently Glossia, if you
are using dockerlaunch for that purpose).
