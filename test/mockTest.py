# Unit testing framework
import unittest

# Test target
import mockingbird

# Standard modules
import inspect

# External modules

# Internal modules



# TEST CASES

class MockTest(unittest.TestCase):
    
    class TrueClass(object):
        member = 0
        
        def method(self):
            return 'lol'
    
    
    def setUp(self):
        self.mocking_attributes = ['__metaclass__', 'forbidden_attributes']
    
    
    def test_mock_object_attribute_names(self):
        mock_object = self.make_mock_object()
        
        true_object = self.make_true_object()
        
        true_attribute_names = self.attribute_names(true_object)
        mock_attribute_names = self.attribute_names(mock_object)
        
        for name in true_attribute_names:
            self.assertIn(name, mock_attribute_names)
    
    
    def test_mock_object_member(self):
        mock_object = self.make_mock_object()
        self.assertIsNone(mock_object.member())
    
    
    def test_mock_object_method(self):
        mock_object = self.make_mock_object()
        self.assertIsNone(mock_object.method())
    
    
    def test_mock_object_invalid_descriptor(self):
        mock_object = self.make_mock_object()
        with self.assertRaises(AttributeError):
            getattr(mock_object, 'invalid_descriptor')
    
    
    def test_mock_object_with_untouched_member(self):
        true_object = self.make_true_object()
        mock_object = self.make_mock_object_with_the_following_untouchable_attributes(['member'])
        self.assertEqual(mock_object.member, true_object.member)
        self.assertIsNone(mock_object.method())
    
    
    def test_mock_object_with_untouched_method(self):
        true_object = self.make_true_object()
        mock_object = self.make_mock_object_with_the_following_untouchable_attributes(['method'])
        self.assertEqual(mock_object.method(), true_object.method())
        self.assertIsNone(mock_object.member())
    
    
    def test_mock_object_with_untouched_member_and_method(self):
        true_object = self.make_true_object()
        mock_object = self.make_mock_object_with_the_following_untouchable_attributes(['member', 'method'])
        self.assertEqual(mock_object.member, true_object.member)
        self.assertEqual(mock_object.method(), true_object.method())
    
    
    def make_true_object(self):
        true_object = self.TrueClass()
        return true_object
    
    
    def make_mock_object(self):
        mock_class = self.make_mock_class()
        mock_object = mock_class()
        return mock_object
    
    
    def make_mock_object_with_the_following_untouchable_attributes(self, untouchable_attributes = []):
        mock_class = self.make_mock_class()
        map(mock_class.declare_untouchable, untouchable_attributes)
        mock_object = mock_class()
        return mock_object
    
    
    def make_mock_class(self):
        class MockClass(self.TrueClass):
            __metaclass__ = mockingbird.Mock
        
        return MockClass
    
    
    def attribute_names(self, obj):
        members = inspect.getmembers(obj)
        attribute_names = dict(members).keys()
        return attribute_names



# TEST SUITE

if __name__ == '__main__':
    cases = (MockTest,)
    
    suite = unittest.TestSuite()
    
    for test_case in cases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_case))
    
    unittest.TextTestRunner(verbosity = 2).run(suite)