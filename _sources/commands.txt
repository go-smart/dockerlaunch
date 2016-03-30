Container management commands
=============================

The format shown is "COMMAND (reqarg) [optarg]" where "reqarg" is required
and "optarg" is optional. This would be represented
in a JSON instruction, via the Unix socket, as:

.. code-block:: javascript

        {
                "command": COMMAND,
                "arguments": {
                        "reqarg": REQARG_VAL,
                        "optarg": OPTARG_VAL
                }
        }


Or, optionally, if no arguments are supplied for a command:

.. code-block:: javascript

        {
                "command", COMMAND,
                "arguments": null
        }


Commands
--------

- ``CONTAINER``
        - Give back the container ID of the container managed by this connection, and the image
          ID. Note that the latter is useful as it is the UUID, not the tag, and so provides a
          canonical reference for reproducibility.

          .. code-block:: javascript

                {
                        "container_id": CONTID,
                        "image_id": IMAGID
                }

- ``DESTROY``
        - Kill the container associated with the current connection.
- ``LOGS``
        - Return logs for the container controlled by the current connection.
- ``START (image) (volume location) [update socket]``
        - Start a container based on the provided image, with the volume mounted to ``/simdata``
          on the bridge and an optional update socket, also mounted on the bridge, for feeding
          status reports back directly. Image *must* be a known image tag. At present these
          settings are coded into dockerlaunch, but will soon be migrated to a config file:

                  - gosmart/glossia-fenics
                  - gosmart/gfoam
                  - gosmart/glossia-goosefoot
- ``USAGE``
        - Provide number of containers running on this system.
- ``WAIT [timeout]``
        - Do not return until the container has exited. If a timeout is supplied, kill the
          container if it has not returned within the interval.
