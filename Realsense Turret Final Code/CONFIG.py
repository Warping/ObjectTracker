""" 
CONFIG.py
A file containing constants loaded from a configuration file,
default = ./config.ini
"""
import configparser
config = configparser.ConfigParser()


def setup_config(config_path=None, cmdline_config=None):
    global config
    config.read('./config.ini')
    if cmdline_config != None:
        config.read_dict(cmdline_config)


