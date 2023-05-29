# 26.1. Функции и как они работают. Возвращаемые типы и типы передаваемых параметров:

# 1

name = 'John'

def say_hello(name):
    return f"Hello {name}"

def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"

def greet_bob(be_awesome):
    return be_awesome("Bob")


print(greet_bob(be_awesome))
