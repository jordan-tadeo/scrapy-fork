import sys
import os
import unittest

from scrapy.item import Item, Field
from scrapy.utils.misc import (load_object, load_module_or_object, arg_to_iter,
                               walk_modules, get_module_from_filepath)

__doctests__ = ['scrapy.utils.misc']

class UtilsMiscTestCase(unittest.TestCase):

    def test_load_object(self):
        obj = load_object('scrapy.utils.misc.load_object')
        self.assertIs(obj, load_object)
        not_a_string = int(1000)
        self.assertIs(load_object(not_a_string), not_a_string)
        self.assertRaises(ImportError, load_object, 'nomodule999.mod.function')
        self.assertRaises(NameError, load_object, 'scrapy.utils.misc.load_object999')

    def test_load_module_or_object(self):
        testmod = load_module_or_object(__name__ + '.testmod')
        self.assertTrue(hasattr(testmod, 'TESTVAR'))
        testmod = load_module_or_object(
                    os.path.join(os.path.dirname(__file__), 'testmod.py'))
        self.assertTrue(hasattr(testmod, 'TESTVAR'))
        obj = load_object('scrapy.utils.misc.load_object')
        self.assertIs(obj, load_object)

    def test_walk_modules(self):
        mods = walk_modules('tests.test_utils_misc.test_walk_modules')
        expected = [
            'tests.test_utils_misc.test_walk_modules',
            'tests.test_utils_misc.test_walk_modules.mod',
            'tests.test_utils_misc.test_walk_modules.mod.mod0',
            'tests.test_utils_misc.test_walk_modules.mod1',
        ]
        self.assertEquals(set([m.__name__ for m in mods]), set(expected))

        mods = walk_modules('tests.test_utils_misc.test_walk_modules.mod')
        expected = [
            'tests.test_utils_misc.test_walk_modules.mod',
            'tests.test_utils_misc.test_walk_modules.mod.mod0',
        ]
        self.assertEquals(set([m.__name__ for m in mods]), set(expected))

        mods = walk_modules('tests.test_utils_misc.test_walk_modules.mod1')
        expected = [
            'tests.test_utils_misc.test_walk_modules.mod1',
        ]
        self.assertEquals(set([m.__name__ for m in mods]), set(expected))

        self.assertRaises(ImportError, walk_modules, 'nomodule999')

    def test_walk_modules_egg(self):
        egg = os.path.join(os.path.dirname(__file__), 'test.egg')
        sys.path.append(egg)
        try:
            mods = walk_modules('testegg')
            expected = [
                'testegg.spiders',
                'testegg.spiders.a',
                'testegg.spiders.b',
                'testegg'
            ]
            self.assertEquals(set([m.__name__ for m in mods]), set(expected))
        finally:
            sys.path.remove(egg)

    def test_get_module_from_filepath(self):
        testmodpath = os.path.join(os.path.dirname(__file__), 'testmod.py')
        testmod = get_module_from_filepath(testmodpath)
        self.assertTrue(hasattr(testmod, 'TESTVAR'))

        testpkgpath = os.path.join(os.path.dirname(__file__), 'testpkg')
        testpkg = get_module_from_filepath(testpkgpath)
        self.assertTrue(hasattr(testpkg, 'TESTVAR2'))
        # Check submodule access
        import testpkg.submod
        self.assertTrue(hasattr(testpkg.submod, 'TESTVAR3'))
        self.assertIs(testpkg.submod.TESTVAR3,
                      load_object(testpkg.__name__ + ".submod.TESTVAR3"))

    def test_arg_to_iter(self):

        class TestItem(Item):
            name = Field()

        assert hasattr(arg_to_iter(None), '__iter__')
        assert hasattr(arg_to_iter(100), '__iter__')
        assert hasattr(arg_to_iter('lala'), '__iter__')
        assert hasattr(arg_to_iter([1, 2, 3]), '__iter__')
        assert hasattr(arg_to_iter(l for l in 'abcd'), '__iter__')

        self.assertEqual(list(arg_to_iter(None)), [])
        self.assertEqual(list(arg_to_iter('lala')), ['lala'])
        self.assertEqual(list(arg_to_iter(100)), [100])
        self.assertEqual(list(arg_to_iter(l for l in 'abc')), ['a', 'b', 'c'])
        self.assertEqual(list(arg_to_iter([1, 2, 3])), [1, 2, 3])
        self.assertEqual(list(arg_to_iter({'a':1})), [{'a': 1}])
        self.assertEqual(list(arg_to_iter(TestItem(name="john"))), [TestItem(name="john")])

if __name__ == "__main__":
    unittest.main()
