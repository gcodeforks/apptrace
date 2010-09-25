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

    def test_RecordEntry(self):
        """Generating record entries."""

        from apptrace import instruments
        from django.utils import simplejson

        entry = instruments.RecordEntry('foo', 'bar', 'int', 32)
        self.assertEqual(
            {u'module_name': u'foo', u'obj_type': u'int',
             u'dominated_size': 32, u'name': u'bar'},
            simplejson.loads(entry.EncodeJSON()))

        new_entry = instruments.RecordEntry.FromJSON(
            '{"module_name": "test", "name": "l", "obj_type": "list",'
            '"dominated_size": 3112}')

        self.assertEqual(3112, new_entry.dominated_size)

        new_entry.module_name = 'foomodule'

        self.assertEqual(
            {u'module_name': u'foomodule', u'obj_type': u'list',
             u'dominated_size': 3112, u'name': u'l'},
            simplejson.loads(new_entry.EncodeJSON()))

    def test_Record(self):
        """Generating records."""

        from apptrace import instruments
        from django.utils import simplejson

        json = ('{"module_name": "test", "name": "l", "obj_type": "list",'
                '"dominated_size": 3112}')
        record = instruments.Record([instruments.RecordEntry.FromJSON(json)])
        self.assertEqual(
            {u'entries': [{u'module_name': u'test', u'obj_type': u'list',
                           u'dominated_size': 3112, u'name': u'l'}]},
            simplejson.loads(record.EncodeJSON()))

        json = ('{"entries": [{"module_name": "test", "obj_type": "list", '
                              '"dominated_size": 3112, "name": "l"}]}')
        new_record = instruments.Record.FromJSON(json)
        self.assertTrue(
            isinstance(new_record.entries[0], instruments.RecordEntry))

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
        self.assertEqual(2, len(recorder.get_raw_records()))
        self.assertEqual(2, len(recorder.get_records()))
