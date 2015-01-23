# Standard modules

# External modules

# Internal modules



def mock_method(obj, name, mock_method_return_value):
    mock_function = create_mock_function(mock_method_return_value)
    monkey_patch(obj, name, mock_function)


def monkey_patch(obj, name, function):
    bound_method = function.__get__(obj)
    setattr(obj, name, bound_method)


def create_mock_function(mock_function_return_value):
    def mock_function(*args, **kwargs):
        return mock_function_return_value
    
    return mock_function