import pytest
import asyncio.coroutines
import asyncio
from unittest.mock import MagicMock
import time
import uuid
import traceback
import pdb
import lxml.etree
import builtins
from unittest.mock import MagicMock, patch, mock_open

from dockerlaunch.app import DockerLaunchApp

import docker
import tempfile
import requests
import threading
import os
import signal
import traceback
import re


known_guid   = str(uuid.uuid4()).upper()
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
def launchapp( monkeypatch ):
    docker_settings     = MagicMock()
    socket_location     = MagicMock()
    pidfile_path        = MagicMock()
    logger              = MagicMock()
    docker_socket       = MagicMock()
    shutdown_timeout    = MagicMock()
    launchapp = DockerLaunchApp ( docker_settings, socket_location,
                 pidfile_path, logger, pidfile_timeout=5,
                 stdout_path='/dev/tty', stderr_path='/dev/tty',
                 stdin_path='/dev/null')
    launchapp.launchapp = MagicMock()
    return launchapp 



    ###############################
    ######### LEGACY.PY ###########    
    ###############################   



def test_terminate  ( monkeypatch , launchapp ) :
    random_signo        = MagicMock()
    random_stackframe   = MagicMock()
    launchapp._logger   = MagicMock()
    launchapp._server   = MagicMock()
    monkeypatch.setattr( 'os.access'  , lambda p1 , p2 : True )
    monkeypatch.setattr( 'os.remove'  , lambda p1      : True )
    launchapp.terminate ( random_signo , random_stackframe )
    launchapp._logger.info.assert_called_with("Server shutdown")
    launchapp._server.shutdown.assert_called_with()



def test_run  ( monkeypatch , launchapp ) :
    launchapp._logger           = MagicMock()
    launchapp._server           = MagicMock()
    launchapp.socket_location   = MagicMock()    
    panos12                     = MagicMock()
    monkeypatch.setattr( 'dockerlaunch.handler.ThreadedUnixRequestHandler'  , panos12  )
    monkeypatch.setattr( 'dockerlaunch.server.ThreadedUnixServer'  , lambda p1 , panos7 : panos7 ( 'p1' , 'p2' , 'panosargs3' , panos = 'p4' ) )
    monkeypatch.setattr( 'signal.signal'  , lambda p1 , p2 : True )
    launchapp.run (  )
    launchapp._logger.info.assert_called_with ("Starting server")



    
