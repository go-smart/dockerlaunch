.. dockerlaunch documentation master file, created by
   sphinx-quickstart on Tue Mar 29 14:47:39 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dockerlaunch's documentation!
========================================

Contents:

.. toctree::
   :maxdepth: 2

   commands
   known-bugs
   Code <api/modules>
   documentation

This daemon allows a specific, limited set of commands to be issued from
within a prepared container (e.g. `Glossia <https://github.com/go-smart/glossia>`_)
to trigger interaction with the Docker server.

Communication with the container is via a Unix domain socket, by default
located at ``/var/run/dockerlaunch/dockerlaunch.sock``. This is mounted
into the master container.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

