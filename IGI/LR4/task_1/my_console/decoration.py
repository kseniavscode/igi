import re
def checking(type_value, error_output, regex=None, condition=None):
    def dec(func):
        def wrapper():
            while True:
                try:
                    x = type_value(input(func()))

                    if regex and not re.findall(regex, x):
                        raise ValueError
                    
                    if condition and not condition(x):
                        raise ValueError
                    
                    return x    
                except ValueError:
                    print(error_output)
        return wrapper
    return dec