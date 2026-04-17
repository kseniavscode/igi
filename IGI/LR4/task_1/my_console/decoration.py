import re
def checking(type_value, error_output, regex=None, condition=None):
    def dec(func):
        def wrapper():
            while True:
                try:
                    x = input(func())
                    clean_x = re.sub(r"^\s+|\s+$","", x)
                    
                    if regex and not re.fullmatch(regex, clean_x):
                        raise ValueError
                    clean_x = type_value(clean_x)
                    if condition and not condition(clean_x):
                        raise ValueError
                    
                    return clean_x    
                except ValueError:
                    print(error_output)
        return wrapper
    return dec