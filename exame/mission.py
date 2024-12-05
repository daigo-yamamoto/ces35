# mission.py

import numpy as np

class MissionEnvironment:
    def __init__(self, simpy_env, num_drones, area_size, communication_range):
        self.env = simpy_env
        self.num_drones = num_drones
        self.area_size = area_size
        self.communication_range = communication_range
        self.drones = []
        self.attack_active = True
        self.grid_size = 10  # Grade de 10x10 para quadrados de 10 unidades
        self.area_grid = np.zeros((self.grid_size, self.grid_size))

    def mark_area(self, position):
        x_idx = int(position[0] // (self.area_size / self.grid_size))
        y_idx = int(position[1] // (self.area_size / self.grid_size))
        # Garantir que os índices estão dentro dos limites
        x_idx = min(x_idx, self.grid_size - 1)
        y_idx = min(y_idx, self.grid_size - 1)
        self.area_grid[y_idx, x_idx] = 1  # Marcar a posição como reconhecida

    def check_mission_success(self):
        total_cells = self.grid_size * self.grid_size
        recognized_cells = np.count_nonzero(self.area_grid)
        recognized_percentage = (recognized_cells / total_cells) * 100
        print(f"Área reconhecida: {recognized_percentage:.2f}%")
        if recognized_percentage >= 65.0:
            print("Missão concluída com sucesso!")
            return True
        else:
            print("A missão falhou.")
            return False
