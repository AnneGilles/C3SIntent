C3SIntent README

This webapp offers a form to submit and declare an artists intention to join 
Cultural Commons Collecting Society (C3S) as member. A GnuPG encrypted mail 
with the details submitted will be sent to C3S.


setup
=====

create a virtualenv, preferrably with the python 2.7 variant:

$ virtualenv env

activate your new virtualenv:

$ . env/bin/activate

get ready for development:

$ python setup.py develop

this will take a little while and install all necessary dependencies.


run (in development mode)
=========================

$ pserve development.ini --reload


run (in production mode)
========================

$ pserve production.ini
