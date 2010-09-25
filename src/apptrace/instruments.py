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
from google.appengine.api import memcache
from guppy import hpy

import gc


class Recorder(object):
    """Traces the memory usage of various appllication modules."""

    def __init__(self, config):
        """Constructor.

        Args:
            config: A middleware.Config instance.
        """
        self._config = config

    @property
    def config(self):
        return self._config

    def trace(self):
        """Records momory data.

        Uses Heapy to retrieve information about allocated memory.
        """

        gc.collect()
        hp = hpy()

        results = []

        for name in self.config.get_modules():
            if name not in sys.modules:
                continue
            module_dict = sys.modules[name].__dict__
            data = []
            obj_keys = sorted(set(module_dict.keys())-
                              set(self.config.IGNORE_NAMES))
            for key in obj_keys:
                obj = module_dict[key]
                iso = hp.iso(obj)
                # The dominated size of an object is the total size of memory
                # that will become deallocated.
                data.append((key, obj.__class__.__name__, iso.domisize)) 
            results.append((name, data))

        # We use memcache to store records and take a straightforward
        # approach with a very simple index which is basically a counter.
        index = 1
        if not memcache.add(key=self.config.INDEX_KEY, value=index):
            index = memcache.incr(key=self.config.INDEX_KEY)
        key = self.config.RECORD_PREFIX + str(index)
        memcache.add(key=key, value=simplejson.dumps(results))

    def get_records(self, limit=100, offset=0):
        """Returns stored records beginning with the latest.

        Args:
            limit: Max number of records.
            offset: Offset within overall results.
        """

        curr_index = memcache.get(self.config.INDEX_KEY)
        if not curr_index:
            return []

        if curr_index < limit: limit = curr_index 

        keys = ['%i' % (curr_index-i) for i in xrange(offset, limit)]

        records = memcache.get_multi(keys=keys,
                                     key_prefix=self.config.RECORD_PREFIX)

        return [simplejson.loads(records[key]) for key in keys]
