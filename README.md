## Audio Stream manager project


### Description

The project contains two parts the `backend` and `frontend` parts.

### Development instructions

To work in this project follow this instructions

#### Frontend

The frontend is written in ES6 using vuejs

	$ cd frontend

and run 

	$ npm start dev


This is the project structure

	.
	├── build/                      # webpack config files
	│   └── ...
	├── config/
	│   ├── index.js                # main project config
	│   └── ...
	├── src/
	│   ├── main.js                 # app entry file
	│   ├── App.vue                 # main app component
	│   ├── components/             # ui components
	│   │   └── ...
	│   └── assets/                 # module assets (processed by webpack)
	│       └── ...
	├── static/                     # pure static assets (directly copied)
	├── test/
	│   └── unit/                   # unit tests
	│   │   ├── specs/              # test spec files
	│   │   ├── index.js            # test build entry file
	│   │   └── karma.conf.js       # test runner config file
	│   └── e2e/                    # e2e tests
	│   │   ├── specs/              # test spec files
	│   │   ├── custom-assertions/  # custom assertions for e2e tests
	│   │   ├── runner.js           # test runner script
	│   │   └── nightwatch.conf.js  # test runner config file
	├── .babelrc                    # babel config
	├── .postcssrc.js               # postcss config
	├── .eslintrc.js                # eslint config
	├── .editorconfig               # editor config
	├── index.html                  # index.html template
	└── package.json                # build scripts and dependencie


#### Backend

The backend is written in python3 using Flask, celery and a lot of moving stuff

	$ cd backend
	$ export DEV=true

This is the project structure

	.
	├── addreqs.sh              # script to add the python requirements
	├── audiosm
	│   ├── compat.py           # Compatibility script though it's broken
	│   ├── database.py         # Database code
	│   ├── exceptions.py       # API Exceptions
	│   ├── extensions.py       # Backend extensions preparing
	│   ├── __init__.py         # Contains an application factory
	│   ├── jobs                # jobs module
	│   │   ├── models.py       # models 
	│   │   ├── serializers.py  # data serializers
	│   │   └── views.py        # The api views
	│   ├── settings.py         # settings
	│   ├── streams
	│   │   ├── __init__.py
	│   │   ├── models.py
	│   │   ├── serializers.py
	│   │   └── views.py
	│   ├── tasks               # The celery tasks
	│   │   ├── __init__.py
	│   │   └── stream.py
	│   ├── task_worker.py      # a module which exposes a celery instance
	│   ├── users
	│   │   ├── __init__.py
	│   │   ├── models.py
	│   │   ├── serializers.py
	│   │   └── views.py
	│   └── utils.py           # helper functions
	├── installpy.sh
	├── manage.py              # Classic manager
	├── migrations             # Database migrations stuff
	│   ├── alembic.ini
	│   ├── env.py
	│   ├── __pycache__
	│   ├── README
	│   ├── script.py.mako
	│   └── versions
	│       ├── xxxx.py
	├── nginx.conf             # Nginx config
	├── requirements           # The requirements file
	│   ├── dev.txt            # development requirements
	│   └── prod.txt           # production requirements
	└── wsgi.py                # a module which exposes the application instance

Dependencies:

- Nginx with RTMP module
- Redis server


So you need to install nginx with the rtmp module, using the script I provide and copy to it the nginx config.

You also need to have

Please make sure you add the requirements every time you add a new feature, by running the correspondent script.


### Production instructions

#### Frontend

just run

	$ npm run build
	
and then serve the static files, using your favorite webserver


#### Backend

Dependencies:

- Same as Development
- Postgresql

I may have over engineered this solution but the usage is easy:

	$ export DEV=0
	$ python manage.py runserver

You may want to check your migrations also

	$ python manage.py db upgrade
	
to upgrade migrations, it is adviced that you add the migration files
to git.
