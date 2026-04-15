def checking(type_value, error_output, condition):
    def dec(func):
        def wrapper():
            while True:
                try:
                    x = type_value(input(func()))
                    if condition(x):
                        return x
                    else:
                        raise ValueError
                except ValueError:
                    print(error_output)
        return wrapper
    return dec