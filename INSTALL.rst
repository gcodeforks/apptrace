==============================
Apptrace for Google App Engine
==============================

The apptrace package provides a WSGI middleware for tracking down memory leaks
in Google App Engine applications.

Buildout
--------

Install the development environment by typing following commands::

  $ python bootstrap.py --distribute
  $ ./bin/buildout

Running Apptrace
----------------

In order to run the demo application with apptrace run following commands::

  $ ./bin/apptracectl init demo 
  $ python dev_appserver.py demo

Running Unit Tests
------------------

All unit tests can be run by executing the following command::

  $ ./bin/python setup.py test --appengine-lib=<path to the SDK>
