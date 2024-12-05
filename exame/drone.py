# drone.py

import random

class Drone:
    def __init__(self, env, mission_env, drone_id, position, speed, leader=False):
        self.env = env
        self.mission_env = mission_env  # Adiciona referência ao mission_env
        self.id = drone_id
        self.position = position
        self.speed = speed
        self.neighbors = []
        self.data_collected = False
        self.leader = leader
        self.connected_to_leader = False
        self.action = env.process(self.run())
        self.positions_over_time = [position.copy()]
        self.communication_history = []

    def move(self):
        # Movimento simples em direção aleatória
        dx = random.uniform(-1, 1) * self.speed
        dy = random.uniform(-1, 1) * self.speed
        self.position[0] = (self.position[0] + dx) % self.env.area_size
        self.position[1] = (self.position[1] + dy) % self.env.area_size
        # Registrar posição atual
        self.positions_over_time.append(self.position.copy())

    def detect_neighbors(self, drones):
        self.neighbors = []
        for drone in drones:
            if drone.id != self.id:
                distance = ((self.position[0] - drone.position[0]) ** 2 +
                            (self.position[1] - drone.position[1]) ** 2) ** 0.5
                if distance <= self.env.communication_range:
                    self.neighbors.append(drone)

    def collect_data(self):
        # Suponha que o drone coleta dados no tempo 10
        if self.env.now == 10 and not self.data_collected:
            print(f"Drone {self.id} coletou dados no tempo {self.env.now}")
            self.data_collected = True

    def send_data_to_leader(self):
        if self.data_collected and self.connected_to_leader:
            print(f"Drone {self.id} enviou dados ao líder no tempo {self.env.now}")
            self.data_collected = False  # Dados enviados
            self.mission_env.mission_data_received += 1  # Incrementa o contador corretamente
        elif self.data_collected:
            print(f"Drone {self.id} ainda não está conectado ao líder no tempo {self.env.now}")

    def communicate(self):
        self.connected_to_leader = False
        successful_comms = []
        for neighbor in self.neighbors:
            if self.env.now >= 50 and self.env.attack_active and self.id == 0:
                print(f"Drone {self.id} não consegue comunicar com Drone {neighbor.id} devido ao ataque no tempo {self.env.now}")
                # Registrar a falha de comunicação
                successful_comms.append((neighbor.id, False))
            else:
                print(f"Drone {self.id} comunicando com Drone {neighbor.id} no tempo {self.env.now}")
                # Registrar comunicação bem-sucedida
                successful_comms.append((neighbor.id, True))
                if neighbor.leader or neighbor.connected_to_leader:
                    self.connected_to_leader = True
        # Adicionar as comunicações do tempo atual ao histórico
        self.communication_history.append(successful_comms)

    def run(self):
        while True:
            self.move()
            self.detect_neighbors(self.env.drones)
            self.communicate()
            self.collect_data()
            self.send_data_to_leader()
            yield self.env.timeout(1)  # avança o tempo em 1 unidade
