import numpy as np
import random


class Car:

    def __init__(self, car_id, rd, veh_size=5, follow_dist=1, max_speed=33,
                 accel=2.0):
        self.id = car_id
        self.speed = 0
        self.position = 0
        self.road = rd
        self.veh_size = veh_size
        self.follow_dist = follow_dist
        self.max_speed = max_speed
        self.accel = accel

    def move(self, car2):
        # distance_between = self.\
        meters = self.get_distance_between(self.position, car2.position)

        if meters > (self.speed*self.follow_dist + self.accel):
            self.speed_up()
        else:
            if meters > car2.speed:
                self.speed = car2.speed
            else:
                self.stop()

        self.next_position()

    def get_distance_between(self, pos1, pos2):

        if pos1 > pos2:
            dist = ((pos2 - self.veh_size/2) + self.road.total_len-1) - pos1
        else:
            dist = (pos2 - self.veh_size/2) - pos1

        return dist

    def next_position(self):
        self.position = (self.position + self.speed) % self.road.total_len

    def slow_down(self):
        if self.speed >= 2:
            self.speed -= 2
        else:
            self.speed = 0

    def speed_up(self):
        # depending on the section of road we are on - we may slow
        # instead of speeding up
        if random.randint(1, 100) <= \
                self.road.get_chance_to_slow(self.position):
            self.slow_down()
        else:
            if self.speed < self.max_speed:
                self.speed += self.accel

    def stop(self):
        self.speed = 0

    def __str__(self):
        return ('the car id{} speed{} position{}'.format(self.id,
                                                         self.speed,
                                                         self.position))


class Road:

    def __init__(self, r_len):
        self.total_len = r_len
        self.chance_to_slow = 10

    def get_chance_to_slow(self, position):
        if position <= 999 or \
           2000 <= position <= 2999 or \
           4000 <= position <= 4999 or \
           6000 <= position <= 6999:
            self.chance_to_slow = 10
        elif 1000 <= position <= 1999:
            self.chance_to_slow = 40
        elif 3000 <= position <= 3999:
            self.chance_to_slow = 100
        elif 5000 <= position <= 5999:
            self.chance_to_slow = 20

        return self.chance_to_slow


class Simulation:
    # keeps track of the road in a 1000 length list/array
    # get the ave speed of cars after 60 secs

    def __init__(self, number_cars, car_loc_list, s_time, rd, d_types=False):
        self.num_cars = number_cars
        self.sim_time = s_time
        self.cars = []

        if not d_types:
            self.cars = [Car(x, rd) for x in range(0, number_cars)]
        else:
            for x in range(0, number_cars):
                driver_t = random.randint(1, 100)

                # 10% of drivers are aggressive
                if 1 <= driver_t <= 10:
                    self.cars.append(Car(x, rd, max_speed=140, accel=5))
                # check for 15% commercial vehicles
                elif 20 <= driver_t <= 35:
                    # this is the commercial vehicle
                    self.cars.append(Car(x, rd, 25, 2, 100, 1.5))
                # all other cars are normal drivers
                else:
                    self.cars.append(Car(x, rd))

        self.cars_per_s = []

        # set the starting position in each car object
        for i in range(len(self.cars)):
            self.cars[i].position = car_loc_list[i]

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
            locations = []
            for each in self.cars:
                # speeds.append((each.speed, each.position))
                speeds.append(each.speed)
                locations.append(each.position)

            if time == 1:
                self.cars_per_s = np.array([locations])
            else:
                self.cars_per_s = \
                    np.append(self.cars_per_s, [locations], axis=0)

        # after 1 min return the speed of all the cars
        return speeds

    def get_np_array(self):
        return self.cars_per_s


if __name__ == '__main__':

    # first thing to do is make a road and a car or a list of cars
    time_car_trials = []
    num_cars = 30
    sim_time = 60
    road_length = 1000
    driver_types = True
    car_position_arr = np.linspace(0, road_length-1, num=num_cars, dtype=int)

    road = Road(road_length)
    sim = Simulation(num_cars, car_position_arr, sim_time, road, driver_types)
    time_car_trials = sim.run()
    print(time_car_trials)

    # sim.get_np_array()
