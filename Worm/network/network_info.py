import psutil

def get_local_network_ranges():
    # Get all network interface addresses
    addresses = psutil.net_if_addrs()
    network_ranges = []

    print("Available Network Interfaces:")
    for interface_name, interface_addresses in addresses.items():
        for address in interface_addresses:
            print(f"{interface_name}: {address.address}, Family: {address.family}, Netmask: {address.netmask}")

            if address.family == 2:  # Check for IPv4
                ip = address.address
                netmask = address.netmask

                # Calculate the network address using the IP and Netmask
                ip_parts = list(map(int, ip.split('.')))
                netmask_parts = list(map(int, netmask.split('.')))
                
                # Calculate the network address
                network = '.'.join(str(ip_parts[i] & netmask_parts[i]) for i in range(4))
                
                # Calculate broadcast address
                broadcast = '.'.join(str(ip_parts[i] | (255 - netmask_parts[i])) for i in range(4))
                
                # Add the network and broadcast to the list
                network_ranges.append((network, broadcast))

    print("Calculated Network Ranges:", network_ranges)
    return network_ranges  # Return a list of valid network ranges
