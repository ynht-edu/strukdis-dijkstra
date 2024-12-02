class Something:
    class_var = "test"
    def __init__(self, inst_var):
        self.inst_var = inst_var
    def method1(self):
        self.attr1 = "a"
        random = "blabla"
        print(random + self.attr1)
    def method2(self):
        self.attr2 = "test"

thing1 = Something("test1")
thing1.method1()
# thing1.method2()
thing1.class_var = "balbla"
thing2 = Something("test2")

print(thing1.attr2)

dict = {"blabla": "testsfs",
        "blibli": "tist"}

print(dict["blabla"])