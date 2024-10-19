import os
import socket
import threading
from queue import Queue
from network.network_info import get_local_network_ranges
import logging
import os

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/scan_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to perform pinging for a given IP
def ping_ip(ip, queue):
    response = os.system(f"ping -n 1 -w 300 {ip} > nul")  # Windows with timeout
    if response == 0:
        queue.put(ip)  # Put active IP into the queue

# Function to scan a port on a given IP
def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex((ip, port)) == 0:
            logging.info(f"Port {port} is open on {ip}")
            print(f"Port {port} is open on {ip}")

# Function to scan the local network
def scan_network(network_range):
    network, broadcast = network_range
    print(f"Scanning network: {network} - {broadcast}")
    
    threads = []
    queue = Queue()
    
    for i in range(1, 255):  # Scan through 1-254 for a class C network
        ip = f"{network.rsplit('.', 1)[0]}.{i}"  # Replace the last octet
        thread = threading.Thread(target=ping_ip, args=(ip, queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Collect results from the queue
    active_ips = []
    while not queue.empty():
        active_ip = queue.get()
        active_ips.append(active_ip)
        logging.info(f"Active IP found: {active_ip}")
        print(f"Active IP found: {active_ip}")

    # Port scanning on active IPs
    for ip in active_ips:
        for port in range(1, 1025):  # Scanning the first 1024 ports
            thread = threading.Thread(target=scan_port, args=(ip, port))
            thread.start()
            thread.join()  # You might want to adjust this for performance

# Function to start the scanning process
def start_scanning():
    network_ranges = get_local_network_ranges()  # Updated to match the function name
    if not network_ranges:
        print("Could not determine local network ranges.")
        return

    for network_range in network_ranges:
        scan_network(network_range)

if __name__ == "__main__":
    start_scanning()
