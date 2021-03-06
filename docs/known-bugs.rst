Known bugs
==========

Permission denied on simulation launch
--------------------------------------

Occasionally (seemingly when Glossia is killed
without Docker cleaning up, such as in a full system reset), Docker may try and recreate
the dangling dockerlaunch socket when the Docker (*not* dockerlaunch) daemon restarts.
This is apparently due to it being mounted in the Glossia data container
(in a normal set-up) when the system dies. The symptoms are that dockerlaunch
cannot connect to its socket, neither can Glossia, as it is now a file owned by root.

To prevent Docker recreating the socket, the stopped Glossia containers should be manually
removed using ``docker rm`` (by default named glossiaserverside_data_1, glossiaserverside_glossia_1).
This situation can be confirmed by stopping the Docker daemon and restarting with ``docker -d -D``.
A line should be present: ``error registering volume /run/dockerlaunch/dockerlaunch.sock: Volume exists: [[UUID]]``

In later versions of Docker, the ``docker volume`` command may be useful for identifying the
fouling container, if there is ambiguity, using the ``[[UUID]]`` above.
