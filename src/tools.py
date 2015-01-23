# Standard modules

# External modules

# Internal modules



def monkey_patch(obj, name, function):
    bound_method = function.__get__(obj)
    setattr(obj, name, bound_method)