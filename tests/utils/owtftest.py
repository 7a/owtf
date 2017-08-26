from __future__ import print_function
import os
import copy
import glob

import tornado
import unittest
import mock
from hamcrest import *

from tests.utils.clean import db_clean, clean_owtf_review
from tests.utils.utils import load_log, DIR_OWTF_REVIEW, DIR_OWTF_LOGS
from tests.utils.service.web.server import WebServerProcess


class OWTFCliTestCase(unittest.TestCase):

    """Basic OWTF test case that initialises basic patches."""

    DEFAULT_ARGS = ['--nowebui']
    PROTOCOL = 'http'
    IP = '127.0.0.1'
    DOMAIN = 'localhost'
    PORT = '8888'

    def __init__(self, methodName='runTest'):
        super(OWTFCliTestCase, self).__init__(methodName)
        self.args = copy.copy(self.DEFAULT_ARGS)

    def setUp(self):
        self.args = copy.copy(self.DEFAULT_ARGS)
        self.clean_old_runs()
        self.raw_input_patcher = mock.patch('__builtin__.raw_input', return_value=['Y'])
        self.raw_input_patcher.start()

    def tearDown(self):
        self.raw_input_patcher.stop()
        self.clean_logs()

    ###
    # OWTF utils methods.
    ###

    def run_owtf(self, *extra_args):
        """Run OWTF with args plus ``extra_args`` if any."""
        if self.args:
            args = self.args[:]
        else:
            args = self.DEFAULT_ARGS[:]
        if extra_args:
            args += extra_args
        print("with the following options: %s" % args)
        args_str = ' '.join(args)
        os.system("python -m owtf %s" % args_str)
        self.load_logs()

    def load_logs(self):
        """Load all file logs generated by OWTF during the run."""
        abs_path = os.path.join(os.getcwd(), DIR_OWTF_REVIEW, DIR_OWTF_LOGS)
        self.logs_main_process = []
        for main_process_log in glob.glob(os.path.join(abs_path, 'MainProcess*.log')):
            self.logs_main_process.extend(load_log(main_process_log, absolute_path=True))
        self.logs_worker = []
        for worker_log in glob.glob(os.path.join(abs_path, 'Worker*.log')):
            self.logs_worker.extend(load_log(worker_log, absolute_path=True))
        self.logs_proxy_process = []
        for proxy_log in glob.glob(os.path.join(abs_path, 'ProxyProcess*.log')):
            self.logs_proxy_process.extend(load_log(proxy_log, absolute_path=True))
        self.logs_transaction_logger = []
        for trans_log in glob.glob(os.path.join(abs_path, 'TransactionLogger*.log')):
            self.logs_transaction_logger.extend(load_log(trans_log, absolute_path=True))
        self.logs = {
            'MainProcess': self.logs_main_process,
            'Worker': self.logs_worker,
            'ProxyProcess': self.logs_proxy_process,
            'TransactionLogger': self.logs_transaction_logger}
        self.logs_all = []
        for log in self.logs.items():
            self.logs_all.extend(log)

    def clean_logs(self):
        """Remove old logs that have been loaded during a run."""
        if hasattr(self, 'logs_main_process'):
            self.logs_main_process = []
        if hasattr(self, 'logs_worker'):
            self.logs_worker = []
        if hasattr(self, 'logs_proxy_process'):
            self.logs_proxy_process = []
        if hasattr(self, 'logs_transaction_logger'):
            self.logs_transaction_logger = []
        if hasattr(self, 'logs'):
            self.logs = {}
        if hasattr(self, 'logs_all'):
            self.logs_all = []

    @staticmethod
    def clean_old_runs():
        """Clean the database and the older owtf_review directory."""
        # Reset the database.
        db_clean()
        # Remove old OWTF outputs
        clean_owtf_review()

    ###
    # Specific methods that test logs and function calls.
    ###

    def assert_has_been_logged(self, text, name=None, msg=None):
        if name and name in self.logs:
            assert_that(self.logs[name], has_item(text), msg)
        else:
            assert_that(self.logs_all, has_item(text), msg)

    def assert_has_not_been_logged(self, text, name=None, msg=None):
        if name and name in self.logs:
            assert_that(self.logs[name], not(has_item(text)), msg)
        else:
            assert_that(self.logs_all, not(has_item(text)), msg)

    def assert_is_in_logs(self, text, name=None, msg=None):
        if name and name in self.logs:
            self.assertTrue(text in str(self.logs[name]), msg)
        else:
            self.assertTrue(text in str(self.logs_all), msg)

    def assert_is_not_in_logs(self, text, name=None, msg=None):
        if name and name in self.logs:
            self.assertFalse(text in str(self.logs[name]), msg)
        else:
            self.assertFalse(text in str(self.logs_all), msg)

    def assert_are_in_logs(self, texts, name=None, msg=None):
        for text in texts:
            self.assert_is_in_logs(text, name, msg)

    def assert_are_not_in_logs(self, texts, name=None, msg=None):
        for text in texts:
            self.assert_is_not_in_logs(text, name, msg)


class OWTFCliWebPluginTestCase(OWTFCliTestCase):

    DEFAULT_ARGS = ['--nowebui']
    PROTOCOL = 'http'
    IP = '127.0.0.1'
    PORT = '8888'
    MATCH_PLUGIN_START = 'Execution Start'
    MATCH_BUG = 'OWTF BUG'
    DYNAMIC_METHOD_REGEX = "^set_(head|get|post|put|delete|options|connect)_response"

    def setUp(self):
        super(OWTFCliWebPluginTestCase, self).setUp()
        # Web server initialization.
        self.server = WebServerProcess(self.IP, self.PORT)
        self.server.start()

    def tearDown(self):
        super(OWTFCliWebPluginTestCase, self).tearDown()
        self.server.stop()
        tornado.ioloop.IOLoop.clear_instance()
