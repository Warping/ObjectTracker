""" 
CONFIG.py
A file containing constants loaded from a configuration file,
default = ./config.ini
"""
import configparser
#from numpy import numpy.deg2rad
config = configparser.ConfigParser()


def setup_config(config_path=None, cmdline_config=None):
    global config
    config.read('./config.ini')
    if cmdline_config != None:
        config.read_dict(cmdline_config)



"""
# Define constants here

_CAMERA_DFOV = numpy.deg2rad(86)
_CAMERA_HFOV = numpy.deg2rad(73)
_CAMERA_VFOV = numpy.deg2rad(58)
_CAMERA_WIDTH = 640
_CAMERA_HEIGHT = 480
_CAMERA_DISTANCE = 100
_DEBUG_LEVEL = 0
_ARCHITECTURE = 'cpu'
_SHOW_GRAPHS = False
_SHOW_VIDEO = False
_SHOW_OUTPUT = True
_OUTPUT_LOG_FILE = None
_DEBUG_LOG_FILE = None
_FRAMERATE = 30
"""

"""
Maybe I don't really need to do all this bullshit????
def setup_config(file_path=None:str, ):
    config = configparser.ConfigParser()
    config.read('./config.ini')
    if "dfov" in config['Camera']:
        _CAMERA_DFOV = config['Camera']['dfov']
    if "hfov" in config['Camera']:
        _CAMERA_HFOV = config['Camera']['hfov']
    if "vfov" in config['Camera']:
        _CAMERA_VFOV = config['Camera']['vfov']
    #Lots of tedious work! will do later
    """

