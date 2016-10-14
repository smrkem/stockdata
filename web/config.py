# config.py
import os


class BaseConfig(object):
    DEBUG = os.environ['DEBUG']
