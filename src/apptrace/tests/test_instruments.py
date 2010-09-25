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
"""Unit tests for the apptrace instruments."""

import unittest


class TestIntruments(unittest.TestCase):
    """Test case for apptrace instruments."""

    def setUp(self):
        """Setup test requirements."""

        from google.appengine.api import apiproxy_stub_map
        from google.appengine.api.memcache import memcache_stub

        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

        apiproxy_stub_map.apiproxy.RegisterStub(
            'memcache',
            memcache_stub.MemcacheServiceStub())

    def test_Recorder(self):
        """Testing the recorder."""

        from apptrace import instruments

        class Config(object):
            INDEX_KEY     = 'apptrace_test_index'
            RECORD_PREFIX = 'apptrace_test_record'
            IGNORE_NAMES  = []
            @staticmethod
            def get_modules():
                return ['apptrace.instruments']

        recorder = instruments.Recorder(Config)
        recorder.trace()
        recorder.trace()

        # Retrieve records
        self.assertEqual(2, len(recorder.get_records()))
