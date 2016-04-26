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
from unittest.mock import MagicMock, patch, mock_open , Mock

from dockerlaunch.handler import ThreadedUnixRequestHandler

import docker
import tempfile
import requests
import os
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
def handler( monkeypatch ):
    docker_settings     = MagicMock()
    logger              = MagicMock()
    docker_socket       = MagicMock()
    shutdown_timeout    = MagicMock()
    arg1                = MagicMock()
    arg2                = MagicMock()
    arg3                = MagicMock()

    monkeypatch.setattr( 'docker.Client'    , lambda version , base_url : 2123456 )
    monkeypatch.setattr( 'dockerlaunch.layer.DockerLayer' , lambda logger=None : 'p2' )
    
    class turh_parent(Mock):
        _logger = 1
                
    patcher = patch.object ( ThreadedUnixRequestHandler , "__bases__" , ( turh_parent , ) )
    with patcher: 
        patcher.is_local = True
        handler = ThreadedUnixRequestHandler ( docker_settings, logger , arg1 , arg2 , arg3 )

    return handler 



    ###############################
    ######### LEGACY.PY ###########    
    ###############################   
 
    
 
def test_configure ( monkeypatch , handler ):
    random_docker_settings  = MagicMock()
    handler.logger          = MagicMock()
    handler._docker_layer   = MagicMock()    
    random_docker_settings = { 'logger' : 'logger1' }
    handler._configure ( random_docker_settings )
    #dockerlaunch.layer.DockerLayer.assert_called_with ( arg1 , arg2 , arg3 )
    
    

#def test_handle ( monkeypatch , handler ) :
    #handler.connection = MagicMock()
    #monkeypatch.setattr ( 'select.select', lambda p1 , p2 , p3 : ( True  , True , True ) )
    #data007 = MagicMock()
    #data007.index.return_value = -7
    #handler.connection.recv.return_value = data007
    #handler.handle()
    
    
    
def test_process_message1  ( monkeypatch , handler ) :
    random_message          = MagicMock()
    random_arguments        = MagicMock()
    random_message          =   "START"
    random_arguments        = { 'image' : 'pic1' , 'update socket' : True }
    handler._docker_layer   = MagicMock()
    handler._docker_layer.try_launch.return_value = ( True , "LOGS" )
    result = handler._process_message ( random_message , random_arguments )
    
    
    
    
