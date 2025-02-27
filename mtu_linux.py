import subprocess

import re



def is_target_reachable(target):

    """Check if the target IP or domain name is reachable."""

    try:

        subprocess.check_output(['ping', '-c', '1', target], universal_newlines=True, stderr=subprocess.STDOUT)

        return True

    except subprocess.CalledProcessError:

        return False



def find_optimal_mtu(target):

    """Finds the optimal MTU using the ping method with the DF flag."""

    optimal_mtu = 0

    min_size = 40  # Minimum ICMP packet size (header only, 68 - 28)

    max_size = 8972 # Maximum Ethernet MTU (Jumbo Frames, 9000 - 28)

    optimal_data = 0



    while min_size <= max_size:

        mid = (min_size + max_size) // 2

        command = ['ping', '-c', '1', '-M', 'do', '-s', str(mid), target]

        try:

            output = subprocess.check_output(command, universal_newlines=True, stderr=subprocess.STDOUT)

            if "bytes from" in output:

                optimal_data = mid

                min_size = mid + 1

            else:

                max_size = mid - 1

        except subprocess.CalledProcessError as e:

            error_output = e.output.lower()

            if "fragment" in error_output:

                max_size = mid - 1

            else:

                max_size = mid - 1



    optimal_mtu = optimal_data + 28  # Add IP and ICMP headers

    return optimal_mtu



def set_mtu(interface_name, mtu_value):

    """Sets the MTU for the specified interface."""

    try:

        subprocess.run(['sudo', 'ip', 'link', 'set', interface_name, 'mtu', str(mtu_value)], check=True)

        print(f"Successfully set MTU to {mtu_value} on {interface_name}")

    except subprocess.CalledProcessError as e:

        print(f"Failed to set MTU: {e}")



def get_network_interfaces():

    """Get a list of available network interfaces."""

    try:

        output = subprocess.check_output(['ip', 'link', 'show'], universal_newlines=True)

        interfaces = re.findall(r'^\d+:\s+(\S+):', output, re.MULTILINE)

        return interfaces

    except subprocess.CalledProcessError as e:

        print(f"Failed to retrieve network interfaces: {e}")

        return []



def main():

    print("Welcome to the MTU Optimizer for Linux!")

    print("This script helps you find and set the optimal MTU for your network interface.")

    print("Please ensure you run this script with sudo privileges to avoid permission issues.\n")



    # Get target IP or domain name from user with a default value

    target_ip = input("Enter the target IP address or domain name (default: 8.8.8.8): ").strip()

    if not target_ip:

        target_ip = "8.8.8.8"  # Default value



    print("\nChecking target reachability...")

    if not is_target_reachable(target_ip):

        print("Target unreachable. Ensure your connection is working and the target is correct.")

        return



    print("Detecting optimal MTU...")

    optimal_mtu = find_optimal_mtu(target_ip)

    if optimal_mtu == 0:

        print("MTU detection failed. ICMP restrictions may affect results.")

        return



    # List available network interfaces

    interfaces = get_network_interfaces()

    if not interfaces:

        print("No network interfaces found. Please check your network settings.")

        return



    print("\nAvailable network interfaces:")

    for idx, interface in enumerate(interfaces, start=1):

        print(f"{idx}. {interface}")



    # Get user choice

    while True:

        try:

            choice = int(input("\nSelect the number of the network interface to apply the MTU to: "))

            if 1 <= choice <= len(interfaces):

                interface_name = interfaces[choice - 1]

                break

            else:

                print("Invalid choice. Please enter a valid number.")

        except ValueError:

            print("Invalid input. Please enter a number.")



    print(f"\nApplying MTU {optimal_mtu} to {interface_name}")

    set_mtu(interface_name, optimal_mtu)



if __name__ == "__main__":

    main()