# Standard modules

# External modules

# Internal modules



def fake_method(obj, name, fake_method_return_value):
    fake_function = create_fake_function(fake_method_return_value)
    monkey_patch(obj, name, fake_function)


def monkey_patch(obj, name, function):
    bound_method = function.__get__(obj)
    setattr(obj, name, bound_method)


def create_fake_function(fake_function_return_value):
    def fake_function(*args, **kwargs):
        return fake_function_return_value
    
    return fake_function