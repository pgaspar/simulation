import random
import csv

DURATION = 540

class Restroom:
    def __init__(self, num_facilities = 3):
        self.queue = []
        self.facilities = [Facility() for _ in range(0, num_facilities)]

    def enter(self, person):
        unoccupied = filter(lambda x: not x.occupied, self.facilities)
        if unoccupied:
            unoccupied[0].occupy(person)
        else:
            self.queue.append(person)

    def tick(self):
        for f in self.facilities:
            f.tick()

class Facility:
    def __init__(self):
        self.duration = 0
        self.occupier = None

    def occupy(self, person):
        if not self.occupied():
            self.occupier = person
            self.duration = 1
            Person.population.remove(person)
            return True
        else:
            return False

    def occupied(self):
        return self.occupier != None

    def vacate(self):
        Person.population.append(self.occupier)
        self.occupier = None

    def tick(self):
        if self.occupied() and self.duration > self.occupier.use_duration:
            self.vacate()
            self.duration = 0
        elif self.occupied():
            self.duration += 1

class Person:
    population = []

    def __init__(self, frequency = 4, use_duration = 1):
        self.frequency = frequency
        self.use_duration = use_duration

    def need_to_go(self):
        return random.randint(1, DURATION) <= self.frequency


frequency = 3
facilities_per_restroom = 3
use_duration = 1
population_range = range(10, 601, 10)
data = {}

for population_size in population_range:
    Person.population = [Person(frequency, use_duration) for _ in range(0, population_size)]
    data[population_size] = []
    restroom = Restroom(facilities_per_restroom)
    for _ in range(0, DURATION):
        data[population_size].append(len(restroom.queue))
        queue = restroom.queue[:]
        restroom.queue = []
        if queue:
            restroom.enter(queue.pop(0))
        for person in Person.population:
            if person.need_to_go():
                restroom.enter(person)
        restroom.tick()

c = csv.writer(open("simulation1.csv", "wb"))
lbl = population_range[:]
c.writerow(lbl)

for t in range(0, DURATION):
    row = []
    for population_size in population_range:
        row.append(data[population_size][t])
    c.writerow(row)

