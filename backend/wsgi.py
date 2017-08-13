"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

from .injector import app_factory, devConfig

app = app_factory(devConfig)
