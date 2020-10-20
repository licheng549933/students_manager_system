from class_02 import Car


class Animal(Car):

    def __init__(self):
        super().__init__()
        self.ssd = "licheng_ssd"

    def dog(self):
        self.foot = "i have a foot"
        head = "i had a head"

    def cat(self):
        d = Animal()
        print(d)
        print(d.foot)
        print("test")
        print(self.foot)

    def human(self):
        a = "i can speek"
        print(a)


animal = Animal()
animal.cat()
