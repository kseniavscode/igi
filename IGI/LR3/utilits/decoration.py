
def decorator(fun):
    def wrapper(x, value: list):
        print("Decorator starts")
        fun(x, value)
        print("Decorator has been done")
    return wrapper