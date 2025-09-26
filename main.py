#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(current+"/libs")

# LIBS
from log import * 
from str import *

current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current+"/constants")
sys.path.append(current+"/iu")

# CONSTANTS
from constants.general import *

from iu.copyfiles import CopyFilesHomeScreen


if __name__ == "__main__":

    str_client = app_name

    current = os.path.dirname(os.path.realpath(__file__)) 
    str_log_file = log_setup_log_file(current, str_client)
    
    copyfiles = CopyFilesHomeScreen(str_client, str_log_file)

    
    copyfiles.run()
    