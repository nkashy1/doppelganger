# Standard modules
import inspect

# External modules

# Internal modules



class Fake(type):
    
    def __init__(self, name, bases, dct):
        self.untouchable_attributes = []
        self.explicitly_touchable_attributes = []
        
        self.base = bases[0]
        if hasattr(self.base, '__metaclass__'):
            self.base_metaclass = self.base.__metaclass__
        else:
            self.base_metaclass = type
    
    
    def __call__(self, *args, **kwargs):
        self_instance = self.base_metaclass.__call__(self, *args, **kwargs)
        self_instance_dictionary = self.retrieve_attribute_dictionary(self_instance)
        attribute_names = self_instance_dictionary.keys()
        
        self.make_magic_attributes_untouchable_unless_explicitly_touchable(attribute_names)
        self.clear_attributes(self_instance, attribute_names)
        
        return self_instance
    
    
    def clear_attributes(self, self_instance, attribute_names):
        for name in attribute_names:
            if not (name in self.untouchable_attributes):
                object.__setattr__(self_instance, name, None)
    
    
    def declare_untouchable(self, attribute_name):
        if attribute_name in self.explicitly_touchable_attributes:
            self.explicitly_touchable_attributes.remove(attribute_name)
        
        self.untouchable_attributes.append(attribute_name)
    
    
    def declare_touchable(self, attribute_name):
        if attribute_name in self.untouchable_attributes:
            self.untouchable_attributes.remove(attribute_name)
        
        self.explicitly_touchable_attributes.append(attribute_name)
    
    
    def make_magic_attributes_untouchable_unless_explicitly_touchable(self, attribute_names):
        for attribute_name in attribute_names:
            if (not (attribute_name in self.explicitly_touchable_attributes)) and self.is_magic_attribute(attribute_name):
                self.declare_untouchable(attribute_name)
    
    
    def retrieve_attribute_dictionary(self, obj):
        attribute_dictionary = dict(inspect.getmembers(obj))
        return attribute_dictionary
    
    
    # An attribute is magical if and only if it has two leading underscores followed by a non-underscore character
    # and two trailing underscores preceded by a non-underscore character.
    @classmethod
    def is_magic_attribute(self, name):
        if len(name) < 4:
            return False
        
        underscore = '_'
        if name[0] != underscore or name[1] != underscore or name[-1] != underscore or name[-2] != underscore:
            return False
        
        if name[2] == underscore or name[-3] == underscore:
            return False
        
        return True