import subprocess
import re

def is_target_reachable(target):
    """Check if the target IP is reachable."""
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

def main():
    target_ip = '8.8.8.8'  # Google's public DNS server, may be replaced with another IP in countries with ICMP restrictions.

    print("Checking target reachability...")
    if not is_target_reachable(target_ip):
        print("Target unreachable. Ensure your connection is working.")
        return

    print("Detecting optimal MTU...")
    optimal_mtu = find_optimal_mtu(target_ip)
    if optimal_mtu == 0:
        print("MTU detection failed. ICMP restrictions may affect results.")
        return

    ## Please modify the interface_name variable to match your network adapter
    interface_name = "Wi-Fi"
    if not interface_name:
        print("Failed to identify network interface. Run as administrator or check settings.")
        return

    print(f"Applying MTU {optimal_mtu} to {interface_name}")
    set_mtu(interface_name, optimal_mtu)

if __name__ == "__main__":
    main()