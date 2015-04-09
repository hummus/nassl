import os
import unittest

def as_test_suite():
    loc = os.path.abspath(os.path.dirname(__file__))
    testmodules = [test[:-3] for test in os.listdir(loc) if test.endswith('Tests.py')]

    suite = unittest.TestSuite()
    for test in testmodules:
        full_mod_name = 'nassl.tests.{}'.format(test)
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(full_mod_name, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(full_mod_name))

    return suite
