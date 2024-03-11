class Test:
    def __init__(self, name):
        self.name = name

    def class_test_method(self):
        return 'Hello world from class test method'
    
    @classmethod # ye3ne static method. no need for instance
    def class_test_method_2(cls):
        return 'Hello world from class test method 2'

new_test = Test("Hello World")

print(new_test.name)

print(new_test.class_test_method())

print(Test.class_test_method_2())
