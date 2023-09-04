
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_data(data):
    # Estrai le informazioni necessarie
    num_data_points = len(data)
    time_seconds = np.arange(0, num_data_points * 4, 4)  # Creazione di un array di tempi in secondi

    avg_dispersion_values = [item['average_dispersion'] for item in data]
    var_dispersion_values = [item['dispersion_variance'] for item in data]
    avg_velocity_x = [item['average_velocity'][0] for item in data]
    avg_velocity_y = [item['average_velocity'][1] for item in data]
    var_velocity_x = [item['velocity_variance'][0] for item in data]
    var_velocity_y = [item['velocity_variance'][1] for item in data]

    # Crea il grafico 2D per l'average_dispersion
    plt.figure(figsize=(10, 4))
    plt.plot(time_seconds, avg_dispersion_values, marker='o', linestyle='-', color='blue')
    plt.title('Average Dispersion Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Average Dispersion')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Crea il grafico 2D per il var_dispersione
    plt.figure(figsize=(10, 4))
    plt.plot(time_seconds, var_dispersion_values, marker='o', linestyle='-', color='green')
    plt.title('Variance of Dispersion Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Variance of Dispersion')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Crea il grafico 3D per la velocità media
    fig_velocity = plt.figure(figsize=(8, 6))
    ax_velocity = fig_velocity.add_subplot(111, projection='3d')
    ax_velocity.scatter(avg_velocity_x, avg_velocity_y, time_seconds, c='b', marker='o')

    ax_velocity.set_xlabel('Average Velocity (X)')
    ax_velocity.set_ylabel('Average Velocity (Y)')
    ax_velocity.set_zlabel('Time (seconds)')
    ax_velocity.set_title('3D Plot - Average Velocity Over Time')
    
    plt.tight_layout()
    plt.show()

    # Crea il grafico 3D per la varianza della media della velocità
    fig_var_velocity = plt.figure(figsize=(8, 6))
    ax_var_velocity = fig_var_velocity.add_subplot(111, projection='3d')
    ax_var_velocity.scatter(var_velocity_x, var_velocity_y, time_seconds, c='r', marker='o')

    ax_var_velocity.set_xlabel('Variance of Velocity (X)')
    ax_var_velocity.set_ylabel('Variance of Velocity (Y)')
    ax_var_velocity.set_zlabel('Time (seconds)')
    ax_var_velocity.set_title('3D Plot - Variance of Velocity Over Time')
    
    plt.tight_layout()
    plt.show()







