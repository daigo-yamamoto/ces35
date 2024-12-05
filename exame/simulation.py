# simulation.py

import simpy
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
# import numpy as np  # Não é mais necessário se não usamos o numpy
import matplotlib.image as mpimg  # Para carregar a imagem de fundo
from drone import Drone
from mission import MissionEnvironment

NUM_DRONES = 5
SIMULATION_TIME = 100
COMMUNICATION_RANGE = 30
AREA_SIZE = 100

def run_simulation():
    env = simpy.Environment()
    mission_env = MissionEnvironment(env, NUM_DRONES, AREA_SIZE, COMMUNICATION_RANGE)
    env.area_size = AREA_SIZE
    env.communication_range = COMMUNICATION_RANGE
    env.drones = mission_env.drones
    env.attack_active = True
    env.attack_time = 30

    for i in range(NUM_DRONES):
        if i == 0:
            position = [AREA_SIZE / 2, AREA_SIZE / 2]
            speed = 0
            leader = True
        else:
            position = [random.uniform(0, AREA_SIZE), random.uniform(0, AREA_SIZE)]
            speed = random.uniform(1, 3)
            leader = False
        drone = Drone(env, mission_env, i, position, speed, leader=leader)
        mission_env.drones.append(drone)

    env.run(until=SIMULATION_TIME)
    mission_env.check_mission_success()
    return mission_env.drones, mission_env

def animate_drones(drones):
    fig, ax = plt.subplots()
    ax.set_xlim(0, AREA_SIZE)
    ax.set_ylim(0, AREA_SIZE)
    ax.set_title('Movimento dos Drones')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Carregar a imagem de fundo
    background_image = plt.imread('background.png')  # Substitua pelo caminho da sua imagem
    ax.imshow(background_image, extent=[0, AREA_SIZE, 0, AREA_SIZE], origin='upper')

    drone_points = []
    for drone in drones:
        point_style = 'o' if not drone.leader else 's'
        point, = ax.plot([], [], point_style, label=f'Drone {drone.id}')
        drone_points.append(point)
    ax.legend()

    # Cria uma coleção de linhas para as comunicações
    comm_lines = LineCollection([], linewidths=1.5)
    ax.add_collection(comm_lines)

    # Adiciona um texto para exibir o tempo
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, color='blue')

    def update(frame):
        positions = {}
        for idx, drone in enumerate(drones):
            if frame < len(drone.positions_over_time):
                x, y = drone.positions_over_time[frame]
                drone_points[idx].set_data([x], [y])
                positions[drone.id] = (x, y)
            else:
                positions[drone.id] = (None, None)

        # Atualizar as linhas de comunicação
        lines = []
        colors = []
        for drone in drones:
            if frame < len(drone.communication_history):
                comms = drone.communication_history[frame]
                drone_pos = positions[drone.id]
                for neighbor_id, success in comms:
                    neighbor_pos = positions.get(neighbor_id, (None, None))
                    if None not in drone_pos and None not in neighbor_pos:
                        line = [drone_pos, neighbor_pos]
                        lines.append(line)
                        color = 'green' if success else 'red'
                        colors.append(color)
        comm_lines.set_segments(lines)
        comm_lines.set_color(colors)

        # Atualizar o texto com o tempo
        time_text.set_text(f'Tempo: {frame}')

        return drone_points + [comm_lines, time_text]

    ani = animation.FuncAnimation(fig, update, frames=SIMULATION_TIME, interval=300, blit=True)
    plt.show()

if __name__ == '__main__':
    drones, mission_env = run_simulation()
    animate_drones(drones)
