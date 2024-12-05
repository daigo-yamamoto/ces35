# drone.py

import random
import math

class Drone:
    def __init__(self, env, mission_env, drone_id, position, speed, leader=False):
        self.env = env
        self.mission_env = mission_env
        self.id = drone_id
        self.position = position
        self.speed = speed
        self.neighbors = []
        self.leader = leader
        self.action = env.process(self.run())
        self.positions_over_time = [position.copy()]
        self.communication_history = []
        self.direction = random.uniform(0, 2 * math.pi)

    def move(self):
        if not self.leader:
            self.direction += random.uniform(-math.pi/4, math.pi/4)
            dx = math.cos(self.direction) * self.speed
            dy = math.sin(self.direction) * self.speed
            self.position[0] = (self.position[0] + dx) % self.env.area_size
            self.position[1] = (self.position[1] + dy) % self.env.area_size
            self.positions_over_time.append(self.position.copy())
            self.mission_env.mark_area(self.position)
        else:
            self.positions_over_time.append(self.position.copy())

    def detect_neighbors(self, drones):
        self.neighbors = []
        for drone in drones:
            if drone.id != self.id:
                distance = ((self.position[0] - drone.position[0]) ** 2 +
                            (self.position[1] - drone.position[1]) ** 2) ** 0.5
                if distance <= self.env.communication_range:
                    self.neighbors.append(drone)

    def communicate(self):
        successful_comms = []
        for neighbor in self.neighbors:
            if self.env.attack_active and self.env.now >= self.env.attack_time:
                failure_probability = 0.5  # 50% de chance de falha
                if random.random() < failure_probability:
                    print(f"Drone {self.id} falhou ao comunicar com Drone {neighbor.id} devido ao ataque no tempo {self.env.now}")
                    successful_comms.append((neighbor.id, False))
                else:
                    print(f"Drone {self.id} comunicando com Drone {neighbor.id} no tempo {self.env.now}")
                    successful_comms.append((neighbor.id, True))
            else:
                print(f"Drone {self.id} comunicando com Drone {neighbor.id} no tempo {self.env.now}")
                successful_comms.append((neighbor.id, True))
        self.communication_history.append(successful_comms)

    def run(self):
        while True:
            self.move()
            self.detect_neighbors(self.env.drones)
            self.communicate()
            yield self.env.timeout(1)
