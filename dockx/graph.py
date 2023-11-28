import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from collections import defaultdict
from itertools import count
import time
import numpy as np
import docker

# Function to generate random CPU usage data for containers
def generate_cpu_data(num_containers):
    '''cpu_data = defaultdict(list)
    for i in range(num_containers):
        cpu_data[f'Container {i+1}'] = [random.randint(0, 100)]
    '''
    # get cpu data for each conatiner from docker client
    cpu_data = {}
    containers = client.containers.list()
    for container in containers:
        stats = container.stats(stream=False)
        cpu_percent = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
        container_name = container.name
        if container_name not in cpu_data:
            cpu_data[container_name] = [cpu_percent * 100]
    
    return cpu_data

# Update the CPU usage data for each container
def update_cpu_data(cpu_data):
    for container in cpu_data:
        # Simulate CPU usage change for each container
        cpu_usage = cpu_data[container][-1] + random.randint(-10, 10)
        cpu_usage = max(0, min(cpu_usage, 100))  # Ensure CPU usage stays between 0 and 100
        cpu_data[container].append(cpu_usage)
    
# Function to smooth the CPU usage data using rolling averages
def smooth_data(cpu_data):
    smoothed_data = {}
    for container, usage in cpu_data.items():
        smoothed_data[container] = np.convolve(usage, np.ones(10) / 10, mode='valid')
    return smoothed_data

# Function to animate the real-time graph
def animate(i):
    update_cpu_data(cpu_data)
    smoothed_cpu_data = smooth_data(cpu_data)
    plt.cla()  # Clear the previous plot
    for container, usage in smoothed_cpu_data.items():
        plt.plot(usage, label=container)
    
    plt.ylim(0, 100)
    plt.xlabel('Time')
    plt.ylabel('Smoothed CPU Usage (%)')
    plt.title('Real-time Container CPU Statistics (Smoothed)')
    plt.legend(loc='upper left')
    plt.tight_layout()

# connect to docker client
client = docker.from_env()

# get no of running containters to monitor from docker client
num_containers = len(client.containers.list()) 
cpu_data = generate_cpu_data(num_containers)

# Set up the figure for plotting
plt.figure(figsize=(10, 6))

# Animate the plot
ani = FuncAnimation(plt.gcf(), animate, interval=1000)  # Update plot every second (1000 ms)
plt.show()
