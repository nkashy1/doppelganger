# Unit testing framework
import unittest

# Test target
import doppelganger

# Standard modules
import inspect

# External modules

# Internal modules



# TEST CASES

class doppelgangerTest(unittest.TestCase):
    
    class TrueClass(object):
        member = 0
        
        def method(self):
            return 'lol'
    
    
    def test_fake_object_attribute_names(self):
        fake_object = self.make_fake_object()
        
        true_object = self.make_true_object()
        
        true_attribute_names = self.attribute_names(true_object)
        fake_attribute_names = self.attribute_names(fake_object)
        
        for name in true_attribute_names:
            self.assertIn(name, fake_attribute_names)
    
    
    def test_fake_object_member(self):
        fake_object = self.make_fake_object()
        self.assertIsNone(fake_object.member)
    
    
    def test_fake_object_method(self):
        fake_object = self.make_fake_object()
        self.assertIsNone(fake_object.method)
    
    
    def test_fake_object_invalid_descriptor(self):
        fake_object = self.make_fake_object()
        with self.assertRaises(AttributeError):
            getattr(fake_object, 'invalid_descriptor')
    
    
    def test_fake_object_with_untouched_member(self):
        true_object = self.make_true_object()
        fake_object = self.make_fake_object_with_the_following_untouchable_attributes(['member'])
        self.assertEqual(fake_object.member, true_object.member)
        self.assertIsNone(fake_object.method)
    
    
    def test_fake_object_with_untouched_method(self):
        true_object = self.make_true_object()
        fake_object = self.make_fake_object_with_the_following_untouchable_attributes(['method'])
        self.assertEqual(fake_object.method(), true_object.method())
        self.assertIsNone(fake_object.member)
    
    
    def test_fake_object_with_untouched_member_and_method(self):
        true_object = self.make_true_object()
        fake_object = self.make_fake_object_with_the_following_untouchable_attributes(['member', 'method'])
        self.assertEqual(fake_object.member, true_object.member)
        self.assertEqual(fake_object.method(), true_object.method())
    
    
    def test_monkey_patch(self):
        fake_object = self.make_fake_object()
        
        return_string = 'rofl'
        fake_method = lambda self: return_string
        doppelganger.tools.monkey_patch(fake_object, 'method', fake_method)
        
        self.assertEqual(fake_object.method(), return_string)
    
    
    def test_create_fake_returner(self):
        fake_function_return_value = 0
        fake_function = doppelganger.tools.create_fake_returner(fake_function_return_value)
        self.assertEqual(fake_function(), fake_function_return_value)
    
    
    def test_patch_returner(self):
        fake_object = self.make_fake_object()
        
        fake_method_return_value = 'rofl'
        doppelganger.tools.patch_returner(fake_object, 'method', fake_method_return_value)
        
        self.assertEqual(fake_object.method(), fake_method_return_value)
    
    
    def test_is_magic_attribute(self):
        is_magic_attribute = doppelganger.Doppel.is_magic_attribute
        self.assertFalse(is_magic_attribute('lol'))
        self.assertTrue(is_magic_attribute('__class__'))
        self.assertFalse(is_magic_attribute('___three_underscores___'))
        self.assertTrue(is_magic_attribute('__name_with_underscores__'))
    
    
    def test_make_magic_attributes_untouchable_unless_explicitly_touchable(self):
        fake_class = self.make_fake_class()
        attribute_names = ['nonmagical_attribute', '__magic_attribute__']
        fake_class.make_magic_attributes_untouchable_unless_explicitly_touchable(attribute_names)
        self.assertIn('__magic_attribute__', fake_class.untouchable_attributes)
    
    
    def test_declare_touchable(self):
        fake_class = self.make_fake_class()
        fake_class.declare_untouchable('method')
        fake_class.declare_touchable('method')
        fake_object = fake_class()
        self.assertIsNone(fake_object.method)
        
        fake_class.declare_untouchable('method')
        fake_object = fake_class()
        self.assertIsNotNone(fake_object.method)
    
    
    def test_create_fake_caller(self):
        function_to_call = lambda x, y: x + 1
        input_values = (10, 20)
        fake_caller = doppelganger.tools.create_fake_caller(function_to_call, *input_values)
        self.assertEqual(fake_caller(), input_values[0] + 1)
    
    
    def test_patch_caller(self):
        function_to_call = lambda x, y: x + y
        first_argument = 10
        second_argument = 1.1
        
        fake_object = self.make_fake_object()
        doppelganger.tools.patch_caller(fake_object, 'method', function_to_call, first_argument, second_argument)
        
        true_value = first_argument + second_argument
        self.assertEqual(fake_object.method(), true_value)
    
    
    def make_true_object(self):
        true_object = self.TrueClass()
        return true_object
    
    
    def make_fake_object(self):
        fake_class = self.make_fake_class()
        fake_object = fake_class()
        return fake_object
    
    
    def make_fake_object_with_the_following_untouchable_attributes(self, untouchable_attributes = []):
        fake_class = self.make_fake_class()
        map(fake_class.declare_untouchable, untouchable_attributes)
        fake_object = fake_class()
        return fake_object
    
    
    def make_fake_class(self):
        class fakeClass(self.TrueClass):
            __metaclass__ = doppelganger.Doppel
        
        return fakeClass
    
    
    def attribute_names(self, obj):
        members = inspect.getmembers(obj)
        attribute_names = dict(members).keys()
        return attribute_names



# TEST SUITE

if __name__ == '__main__':
    cases = (doppelgangerTest,)
    
    suite = unittest.TestSuite()
    
    for test_case in cases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_case))
    
    unittest.TextTestRunner(verbosity = 2).run(suite)