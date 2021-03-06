#!/usr/bin/python
# -*- coding: utf-8 -*-

import binascii
import codecs
import gzip
#import http.cookiejar
import os
import platform
import random
import re
import signal
import socket
import struct
import subprocess
import sys 
import threading
import time

"""
-------------------------------------------------------------------------------
Function:
【整理】Python中的logging模块的使用（可以实现同时输出信息到cmd终端窗口和log文件（txt）中）
 
http://www.crifan.com/summary_python_logging_module_usage
 
Author:     Crifan
Verison:    2012-11-23
-------------------------------------------------------------------------------
"""
 
import logging;
 
#-------------------------------------------------------------------------------
def loggingDemo():
    """Just demo basic usage of logging module
    """
    logging.info("You should see this info both in log file and cmd window");
    logging.warning("You should see this warning both in log file and cmd window");
    logging.error("You should see this error both in log file and cmd window");
     
    logging.debug("You should ONLY see this debug in log file");
    return;
 
#-------------------------------------------------------------------------------   
def initLogging2(logFilename):
    pass

def initLogging(logFilename):
    
    """Init for logging
    """
    logging.basicConfig(
                    level    = logging.DEBUG,
#format   = '%(name)-12s.%(lineno)-4d  %(levelname)-8s %(message)s',
                    format   = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
#                    ('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)  
                    datefmt  = '%m-%d %H:%M')#,
#filename = logFilename,
#filemode = 'w');
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler();
    console.setLevel(logging.INFO);
    # set a format which is simpler for console use
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
    # tell the handler to use this format
    console.setFormatter(formatter);
#logging.getLogger('').addHandler(console);
 
 
###############################################################################
###初始化log信息
logFilename = "crifan_logging_demo.log";
initLogging(logFilename);

if __name__=="__main__":
    logFilename = "crifan_logging_demo.log";
    initLogging(logFilename);
    loggingDemo();
