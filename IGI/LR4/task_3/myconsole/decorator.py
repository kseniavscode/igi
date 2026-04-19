def decorator(fun):
    def wrapper(x, value: list):
        print("Decorator starts")
        fun(x, value)
        print("Decorator has been done")
    return wrapper

def valid_input(x_type, error_string, condition=lambda x: True):
    def decorator(fun):
        def wrapper():
            input_string = fun();
            while True:
                try:
                    x = x_type(input(input_string))
                    if condition(x):
                        break
                except ValueError:
                    print(error_string)
            print("")
            return x
        return wrapper
    return decorator
