# Standard modules

# External modules

# Internal modules



def patch_returner(obj, name, fake_method_return_value):
    fake_returner = create_fake_returner(fake_method_return_value)
    monkey_patch(obj, name, fake_returner)


def patch_caller(obj, name, function_to_call, *args, **kwargs):
    fake_caller = create_fake_caller(function_to_call, *args, **kwargs)
    monkey_patch(obj, name, fake_caller)


def monkey_patch(obj, name, function):
    bound_method = function.__get__(obj)
    setattr(obj, name, bound_method)


def create_fake_returner(fake_returner_return_value):
    def fake_returner(self, *method_args, **method_kwargs):
        return fake_returner_return_value
    
    return fake_returner


def create_fake_caller(function_to_call):
    def fake_caller(self, *method_args, **method_kwargs):
        return function_to_call(*method_args, **method_kwargs)
    
    return fake_caller