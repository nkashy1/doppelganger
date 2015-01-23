# Standard modules
import inspect

# External modules

# Internal modules



def empty_function(*args, **kwargs):
    return None


class Mock(type):
    
    def __init__(self, name, bases, dct):
        self.forbidden_attributes = ['__module__', '__subclasshook__', '__class__', '__dict__', '__weakref__']
        
        self.base = bases[0]
        if hasattr(self.base, '__metaclass__'):
            self.base_metaclass = self.base.__metaclass__
        else:
            self.base_metaclass = type
    
    
    def __call__(self, *args, **kwargs):
        self_instance = self.base_metaclass.__call__(self, *args, **kwargs)
        self_instance_dictionary = self.retrieve_attribute_dictionary(self_instance)
        attribute_names = self_instance_dictionary.keys()
        
        self.clear_attributes(self_instance, attribute_names)
        
        return self_instance
    
    
    def clear_attributes(self, self_instance, attribute_names):
        for name in attribute_names:
            if not (name in self.forbidden_attributes):
                object.__setattr__(self_instance, name, empty_function.__get__(self, self_instance))
    
    
    def declare_untouchable(self, attribute_name):
        self.forbidden_attributes.append(attribute_name)
    
    
    def retrieve_attribute_dictionary(self, obj):
        attribute_dictionary = dict(inspect.getmembers(obj))
        return attribute_dictionary