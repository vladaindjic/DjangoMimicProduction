# Auth and Tests in Django
This repo introduces a simple web-application that uses Django auth system and 
contains a simple test suite.

## Django Auth System
The default Django authentication system has been used to provide user 
authentication and authorization on a few places in the app (see 
kasa\_view.py for the demo).

## Django Tests
In order to run provided Django test suite, run the following commands:
```console
$ cd prodavnicesajt
$ python manage.py test prodavnice.tests --noinput
```
Option `--noinput` automatically destroys the test database before each run.

Follow the instructions in the README.txt document in order to build and run 
the Django app itself.

## CI
This repo specifies a Django workflow that enables some sort of basic CI/CD.
