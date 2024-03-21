class Test:
    def __init__(self, name):
        self.name = name

    def class_test_method(self):
        return 'Hello from class method'

    @classmethod
    def class_test_method2(cls):
        return 'Hello from class method2'

new_test = Test('Hello World')

print(new_test.class_test_method())

print(Test.class_test_method2())