# -*- coding: utf-8 -*-
#
# Copyright 2010 Tobias Rodäbel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""User interface for interactive retrieval of apptrace records."""

from apptrace.middleware import config
from apptrace.instruments import Recorder
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

import email
import mimetypes
import os
import time


class StaticHandler(webapp.RequestHandler):
    """Request handler to serve static files."""

    def get(self):
        path = self.request.path
        filename = path[path.rfind('/')+1:]
        filename = os.path.join(os.path.dirname(__file__), 'static', filename)
        content_type, encoding = mimetypes.guess_type(filename)
        assert content_type and '/' in content_type, repr(content_type)
        expiration = email.Utils.formatdate(time.time()+3600, usegmt=True)
        try:
            fp = open(filename, 'rb')
        except IOError:
            self.response.set_status(404)
            return
        try:
            self.response.out.write(fp.read())
        finally:
            fp.close()
        self.response.headers['Content-type'] = content_type
        self.response.headers['Cache-Control'] = 'public, max-age=expiry'
        self.response.headers['Expires'] = expiration


class OverviewHandler(webapp.RequestHandler):
    """Serves the overview page."""

    def get(self):
        records = Recorder(config).get_raw_records()
        template_vars = {'records': records}
        self.response.out.write(template.render('index.html', template_vars))


def main():
    """The main function."""

    app = webapp.WSGIApplication([
        ('.*/static/.*', StaticHandler),
        ('.*', OverviewHandler),
    ], debug=True)

    util.run_bare_wsgi_app(app)


if __name__ == "__main__":
    main()
