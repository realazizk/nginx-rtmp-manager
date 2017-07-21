from .injector import app_factory, devConfig

app = app_factory(devConfig)
