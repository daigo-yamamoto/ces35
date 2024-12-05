# mission.py

class MissionEnvironment:
    def __init__(self, simpy_env, num_drones, area_size, communication_range):
        self.env = simpy_env
        self.num_drones = num_drones
        self.area_size = area_size
        self.communication_range = communication_range
        self.drones = []
        self.attack_active = True  # Controle do ataque
        self.mission_data_required = num_drones - 1  # Todos os drones, exceto o líder, devem enviar dados
        self.mission_data_received = 0  # Contador de dados recebidos pelo líder
        self.now = 0  # Tempo atual da simulação

    def update_time(self):
        self.now = self.env.now

    def check_mission_success(self):
        if self.mission_data_received >= self.mission_data_required:
            print("Missão concluída com sucesso!")
            return True
        else:
            print("A missão falhou.")
            return False
