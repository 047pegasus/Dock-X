import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import docker
import time

# Function to fetch CPU usage data for containers using Docker API
def get_cpu_data(client):
    cpu_data = {}
    containers = client.containers.list()
    for container in containers:
        stats = container.stats(stream=False)
        cpu_percent = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
        container_name = container.name
        if container_name not in cpu_data:
            cpu_data[container_name] = {'x': [], 'y': []}
        cpu_data[container_name]['x'].append(time.time())  # Adding timestamp
        cpu_data[container_name]['y'].append(cpu_percent * 100)  # Convert to percentage by multiplying with 100
    return cpu_data

# Function to animate the real-time graph
def animate(i):
    cpu_data = get_cpu_data(client)
    plt.clf()  # Clear the previous plot
    for container, data in cpu_data.items():
        if len(data['x']) > 1:
            time_diff = [(t - data['x'][0]) for t in data['x']]
            plt.plot(time_diff, data['y'], label=container)  # Normalize time to start from 0
    
    plt.ylim(0, 100)
    plt.xlabel('Time (seconds)')
    plt.ylabel('CPU Usage (%)')
    plt.title('Real-time Container CPU Statistics')
    plt.legend(loc='upper left')  # Display legend with container names
    plt.tight_layout()

# Set up Docker client
client = docker.from_env()

# Set up the figure for plotting
plt.figure(figsize=(10, 6))

# Animate the plot
ani = FuncAnimation(plt.gcf(), animate, interval=5000)  # Update plot every 5 seconds (5000 ms)
plt.show()
