### -*- coding: utf-8 -*- ####################################################
"""
=========   given from http://alarin.blogspot.com/ ===========
Test runner with code coverage.

"""

import os

from django.test.simple import (DjangoTestSuiteRunner, build_test, get_app,
                     build_suite, get_apps, TestCase, reorder_suite)
from django.conf import settings
from django.utils import unittest

from coverage import coverage as Caverage

class CaverageTestSuiteRunner(DjangoTestSuiteRunner):

    omit_folders = ('tests', 'settings', 'migrations')

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        coverage = Caverage()
        coverage.start()
        test_results = super(CaverageTestSuiteRunner, self).run_tests(test_labels, extra_tests=None, **kwargs)
        coverage.stop()

        if kwargs.get('verbosity', 1) >= 1:
            print "Generating coverage report..."

        coverage_modules = []
        for app in test_labels:
            try:
                module = __import__(app, globals(), locals(), [''])
            except ImportError:
                coverage_modules = None
                break
            if module:
                base_path = os.path.join(os.path.split(module.__file__)[0], "")
                for root, dirs, files in os.walk(base_path):
                    if not root.endswith(self.omit_folders):
                        for fname in files:
                            if fname.endswith(".py") and os.path.getsize(os.path.join(root, fname)) > 1:
                                try:
                                    mname = os.path.join(app, os.path.join(root, fname).replace(base_path, ""))
                                    coverage_modules.append(mname)
                                except ImportError:
                                    pass #do nothing

        if coverage_modules or not test_labels:
            coverage.html_report(coverage_modules, directory=settings.COVERAGE_REPORT_PATH)

        return test_results


    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = unittest.TestSuite()

        if test_labels:
            for label in test_labels:
                if '.' in label:
                    suite.addTest(build_test(label))
                else:
                    app = get_app(label)
                    suite.addTest(build_suite(app))
        else:
            for app in get_apps():
                if app.__file__.startswith(os.path.abspath('.')):
                    suite.addTest(build_suite(app))

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, (TestCase,))
