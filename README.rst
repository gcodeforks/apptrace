==============================
Apptrace for Google App Engine
==============================

The apptrace package provides a WSGI middleware for tracking down memory leaks
in Google App Engine Python applications.

Since apptrace is meant for development and debugging purposes only, it works
with the development appserver of the Google App Engine Python SDK and
TyphoonAE. It will definitely not work on the GAE production environment.

Copyright and License
---------------------

Copyright 2010 Tobias Rodaebel

This software is released under the Apache License, Version 2.0. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Google App Engine is a trademark of Google Inc.

Requirements
------------

The apptrace package requires Guppy-PE (http://guppy-pe.sourceforge.net) to be
installed on your PYTHONPATH. It will be automatically installed when you use
the `easy_install` command.

Contact
-------

Tobias Rodaebel <tobias dot rodaebel at googlemail dot com>
