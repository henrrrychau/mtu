import subprocess

def is_target_reachable(target):
    """Check if the target IP is reachable."""
    try:
        subprocess.run(['ping', '-c', '1', target], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def find_optimal_mtu(target):
    """Finds the optimal MTU using the ping method with the DF flag."""
    min_size = 40    # Minimum ICMP payload size (68 - 28 headers)
    max_size = 8972  # Maximum possible payload (Jumbo Frame MTU - 28 headers)
    optimal_payload = 0

    while min_size <= max_size:
        mid = (min_size + max_size) // 2
        try:
            # Run ping with DF flag and specified payload size
            subprocess.run(
                ['ping', '-c', '1', '-M', 'do', '-s', str(mid), target],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
            # If successful, try a larger payload
            optimal_payload = mid
            min_size = mid + 1
        except subprocess.CalledProcessError as e:
            # Check if the error is due to fragmentation or other issues
            error_msg = e.stderr.lower()
            if "message too long" in error_msg or "fragmentation needed" in error_msg:
                max_size = mid - 1
            else:
                # Other error, adjust max_size downwards
                max_size = mid - 1

    return optimal_payload + 28  # Add headers to get MTU

def set_mtu(interface, mtu):
    """Sets the MTU for the specified interface using iproute2."""
    try:
        # Execute ip link command to set MTU
        subprocess.run(
            ['ip', 'link', 'set', 'dev', interface, 'mtu', str(mtu)],
            check=True
        )
        print(f"Successfully set MTU to {mtu} on {interface}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set MTU: {e}")

def main():
    target_ip = '8.8.8.8'  # Adjust if needed for ICMP restrictions

    print("Checking target reachability...")
    if not is_target_reachable(target_ip):
        print("Target unreachable. Ensure your connection is working and ICMP is allowed.")
        return

    print("Detecting optimal MTU...")
    optimal_mtu = find_optimal_mtu(target_ip)
    if optimal_mtu < 68:  # Ensure MTU meets RFC 791 minimum
        print("Abnormally low MTU detected. Check network configuration.")
        return

    # Set your interface name here (e.g., eth0, enp0s3, wlp0s20f3)
    interface_name = "eth0"
    if not interface_name:
        print("Network interface not specified. Set the interface_name variable.")
        return

    print(f"Applying MTU {optimal_mtu} to {interface_name}")
    set_mtu(interface_name, optimal_mtu)

if __name__ == "__main__":
    main()