class Car:
    def color(self):
        pass

    def max_speed(self):
        pass


class Skoda(Car):
    def color(self):
        print('red')

    def max_speed(self):
        print(30)


class Audi(Car):
    def color(self):
        print('blue')

    def max_speed(self):
        print(31)

cars = [Skoda(), Audi()]
for car in cars:
    car.color()
    car.max_speed()
