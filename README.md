## Audio Stream manager project

### Installation

Make sure you have vagrant activated with VirtualBox backend.

Then run:

    $ vagrant up --provision

then go to the application directory

    $ cd /app

If you want to run in a development environment use:

    $ export DEV=1

then create your schema using:

    $ python3 manage.py create

create a superuser following the instructions:

    $ python3 manage.py makesuperuser
