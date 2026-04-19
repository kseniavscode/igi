import re
def checking(type_value, error_output, regEx=None, condition=None):
    def decorator(fun):
        def wrapper():
            while True:
                try:
                    x = type_value(re.sub(r"^\s+|\s+$","",input(fun())))
                    if regEx and not re.fullmatch(regEx, x):
                        raise ValueError
                    if condition and not condition(x):
                        raise ValueError
                    return x
                except ValueError:
                    print(error_output)
        return wrapper    
    return decorator