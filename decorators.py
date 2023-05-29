def do_twice(func):
    def wrapper():
        func()
        func()
    return wrapper