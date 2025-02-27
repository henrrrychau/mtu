import subprocess

def is_target_reachable(target):
    """Check if the target IP or domain name is reachable."""
    try:
        subprocess.check_output(['ping', '-n', '1', target], universal_newlines=True, stderr=subprocess.STDOUT)
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
        command = ['ping', '-n', '1', '-f', '-l', str(mid), target]
        try:
            output = subprocess.check_output(command, universal_newlines=True, stderr=subprocess.STDOUT)
            if "TTL=" in output:
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
    """Sets the MTU for the specified interface using netsh."""
    try:
        subprocess.run(
            f'netsh interface ipv4 set subinterface "{interface_name}" mtu={mtu_value} store=persistent',
            shell=True, check=True
        )
        print(f"Successfully set MTU to {mtu_value} on {interface_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set MTU: {e}")

def get_network_adapters():
    """Display the list of available network adapters."""
    try:
        output = subprocess.check_output(['netsh', 'interface', 'ipv4', 'show', 'interfaces'], universal_newlines=True)
        print("Available network adapters:")
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve network adapters: {e}")

def main():
    print("Welcome to the MTU Optimizer!")
    print("This script helps you find and set the optimal MTU for your network interface.")
    print("Please ensure you run this script as an administrator to avoid permission issues.\n")

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

    # Display available network adapters
    get_network_adapters()

    # Get user input for the adapter name
    interface_name = input("\nCopy and paste the name of the network adapter to apply the MTU to: ").strip()

    print(f"\nApplying MTU {optimal_mtu} to {interface_name}")
    set_mtu(interface_name, optimal_mtu)

if __name__ == "__main__":
    main()