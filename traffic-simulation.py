import numpy

class Car(self):
    self.car_length = 5
    self.des_speed = 120
    self.accel = 2
    self.decel = 2

    def __init__(self, speed, dist):
        self.current_speed = speed
        self.dist_to_next_car = dist


    def dist_to_next_car(self):



class Road(self):

    def __init__(self, t_len):
        self.total_len = t_len

class Simulation(self, road, car):

    def __init__(self, road, car):


if __name__ == '__main__':

    # first thing to do is make a road and a car or a list of cars
    num_cars = 30
    road_length = 1000
    car_arr = np.linspace(0, num_cars, road_length)
    road = Road(road_length)
    sim = Simulation(road, car_arr)