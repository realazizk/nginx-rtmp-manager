from injector import app_factory, devConfig

app = app_factory(devConfig)


app.run(
    debug=True,
    host='0.0.0.0',
    port=5000
)
