# simulation.py

import simpy
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
from drone import Drone
from mission import MissionEnvironment

NUM_DRONES = 5
SIMULATION_TIME = 100  # em unidades de tempo arbitrárias
COMMUNICATION_RANGE = 50  # alcance de comunicação
AREA_SIZE = 100  # tamanho da área (100x100)

def run_simulation():
    env = simpy.Environment()
    mission_env = MissionEnvironment(env, NUM_DRONES, AREA_SIZE, COMMUNICATION_RANGE)
    env.area_size = AREA_SIZE
    env.communication_range = COMMUNICATION_RANGE
    env.drones = mission_env.drones  # Lista de drones acessível pelos drones
    env.attack_active = True  
    env.mission_data_received = 0  # Dados recebidos pelo líder

    # Criar drones com posições e velocidades aleatórias
    for i in range(NUM_DRONES):
        position = [random.uniform(0, AREA_SIZE), random.uniform(0, AREA_SIZE)]
        speed = random.uniform(1, 5)
        leader = True if i == 0 else False  # Definindo o Drone 0 como líder
        drone = Drone(env, mission_env, i, position, speed, leader=leader)  # Passa mission_env
        mission_env.drones.append(drone)

    # Executar a simulação
    env.run(until=SIMULATION_TIME)

    # Verificar se a missão foi bem-sucedida
    mission_env.check_mission_success()

    return mission_env.drones

def animate_drones(drones):
    fig, ax = plt.subplots()
    ax.set_xlim(0, AREA_SIZE)
    ax.set_ylim(0, AREA_SIZE)
    ax.set_title('Movimento dos Drones ao Longo do Tempo')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    drone_points = []
    for drone in drones:
        point_style = 'o' if not drone.leader else 's'  # 'o' para drones comuns, 's' para o líder
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
                        # Definir cor: verde para sucesso, vermelho para falha
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
    drones = run_simulation()
    animate_drones(drones)
