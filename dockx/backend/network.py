# Write a python backend to get network information from docker inspect for each running container and send it to socket 47475 on localhost

import docker
import time
import socket
import pickle

def get_container_network():
    client = docker.from_env()
    containers = client.containers.list()
    network_list = []

    for container in containers:
        inspect = client.api.inspect_container(container.id)
        container_network =[
            container.id,
            container.name,
            inspect['NetworkSettings']['Networks']['bridge']['IPAddress'],
            inspect['NetworkSettings']['Networks']['bridge']['MacAddress'],
        ]
        network_list.append(container_network)

    return network_list

def send_network_snapshot():
    # Create a socket and connect to the receiver
    host = 'localhost'
    port = 47475
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    try:
        # Continuously send the network snapshot
        while True:
            # Get the network snapshot
            network_snapshot = get_container_network()

            # Serialize the network snapshot using pickle
            serialized_data = pickle.dumps(network_snapshot)

            # Send the serialized data
            sock.sendall(serialized_data)
            
            print(network_snapshot)
            # Wait for a specified time interval before sending the next snapshot
            time.sleep(1)
            
    finally:
        # Close the socket connection in the finally block to ensure it's closed even if an exception occurs
        sock.close()

if __name__ == '__main__':
    while True:
        send_network_snapshot()
        time.sleep(0.2)

        
