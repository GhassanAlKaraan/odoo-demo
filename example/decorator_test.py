def decorator(func):
    def wrapper():
        print("Something is happening before the function is called")
        func()
        print("Something is happening after the function is called")
    return wrapper

@decorator #noice
def say_whee():
    print("Whee!")
    
    
say_whee()
# whee = decorator(say_whee)
# whee()

