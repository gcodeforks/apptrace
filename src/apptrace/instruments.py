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
"""Instruments for measuring the memory footprint of a GAE application."""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from django.utils import simplejson
from guppy import hpy

import gc
import logging


class Recorder(object):
    """Traces the memory usage of various appllication modules."""

    def __init__(self, app, modules):
        """Constructor.

        Args:
            app: A WSGIApplication instance.
            modules: List of module names data shall be recorded for.
        """
        self.app = app
        self.modules = modules

    def trace(self):
        """Records momory data."""

        gc.collect()
        hp = hpy()
        results = []
        for name in self.modules:
            if name not in sys.modules:
                continue
            module_dict = sys.modules[name].__dict__
            data = []
            for key in module_dict:
                obj = module_dict[key]
                iso = hp.iso(obj)
                # The dominated size of an object is the total size of memory
                # that will become deallocated.
                data.append((key, obj.__class__.__name__, iso.domisize)) 
            results.append((name, data))
        logging.info("%s", simplejson.dumps(results))
