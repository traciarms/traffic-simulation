import numpy as np
import random


class Car:

    def __init__(self, id):
        self.id = id
        self.speed = 0
        self.position = 0
        self.accel = 2

    def move(self, car2):
        # distance_between = self.\
        meters = self.get_distance_between(self.position, car2.position)

        if meters > (self.speed + self.accel):
            self.speed_up()
        else:
            if meters > car2.speed:
                self.speed = car2.speed
            else:
                self.stop()

        self.next_position()
        # if self.position > (car2.position%200):
        #     print('car 1 position{}     car 2 position{}'.format(self.position,
        #                                                          car2.position))
        #     print('BOOM')

    def get_distance_between(self, pos1, pos2):
        if pos1 > pos2:
            dist = (pos2 + 999) - pos1
        else:
            dist = pos2 - pos1

        return dist

    def next_position(self):
        self.position = (self.position + self.speed) % 1000

    def slow_down(self):
        if self.speed >= 2:
            self.speed -= 2
        else:
            self.speed = 0

    def speed_up(self):
        # 10 % of the time randomly slow down
        if random.randint(1, 100) < 10:
            self.slow_down()
        else:
            self.speed += 2

    def stop(self):
        self.speed = 0

    def __str__(self):
        return ('the car id{} speed{} position{}'.format(self.id,
                                                         self.speed,
                                                         self.position))


class Road:

    def __init__(self, r_len):
        self.total_len = r_len


class Simulation:
    # keeps track of the road in a 1000 length list/array
    # get the ave speed of cars after 60 secs

    def __init__(self, num_cars, car_location_list, sim_time, road_len):
        self.num_cars = num_cars
        self.sim_time = sim_time
        self.cars = [Car(x) for x in range(0, num_cars)]
        self.cars_per_s = []
        road = Road(road_len)

        # set the starting position in each car object
        for i in range(len(self.cars)):
            self.cars[i].position = car_location_list[i]

    def step(self):
        # for each car on the road check to see if they can advance
        # taking into consideration their speed and the distance of the
        # next car in front of them
        if self.num_cars > 1:
            for each in self.cars:
                first_ind = self.cars.index(each) % len(self.cars)
                second_ind = (first_ind + 1) % len(self.cars)

                self.cars[first_ind].move(self.cars[second_ind])

        # if there is no second car just do it here
        else:
            self.cars[0].speed_up()
            self.cars[0].next_position()

    def run(self, time=0):

        # return - this will be the ave speed of cars for 60 s
        while time < self.sim_time:
            self.step()
            time += 1

            speeds = []
            for each in self.cars:
                #speeds.append((each.speed, each.position))
                speeds.append(each.speed)

            if time == 1:
                self.cars_per_s = np.array([speeds])
            else:
                self.cars_per_s = np.append(self.cars_per_s, [speeds], axis=0)

        print(self.cars_per_s)
        # after 1 min record the speed of all the cars
        return speeds

    def get_np_array(self):
        return self.cars_per_s

    def __str__(self):
        #return 'the (speed, position): {}'.format(self.results)
        return 'the speed {}'.format(self.results)


if __name__ == '__main__':

    # first thing to do is make a road and a car or a list of cars
    num_cars = 30
    sim_time = 60
    road_length = 1000
    car_position_arr = np.linspace(0, road_length-1, num=num_cars, dtype=int)

    sim = Simulation(num_cars, car_position_arr, sim_time, road_length)
    time_car_trials = sim.run()
    print(time_car_trials)

    sim.get_np_array()
