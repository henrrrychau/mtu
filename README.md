# MTU Optimizer

Automatically detect and configure the optimal MTU (Maximum Transmission Unit) for your network interface using ICMP-based path MTU discovery.

## Overview

This repository contains two platform-specific scripts to optimize network performance by finding the ideal MTU size for your connection. The tools use ICMP echo requests with the "Don't Fragment" (DF) flag to determine the maximum packet size that can traverse your network path without fragmentation.

## Features

- **Binary Search Optimization**: Efficiently narrows down optimal MTU using binary search
- **Cross-Platform Support**: Separate implementations for Linux and Windows
- **Automatic Configuration**: Directly applies optimal MTU to network interface
- **Safety Checks**: Validates results against RFC 791 minimum MTU requirements

## Requirements

### Linux (`mtu_linux.py`)
- Python 3.x
- `iproute2` package (provides `ip` command)
- ICMP connectivity to target host

### Windows (`mtu_windows.py`)
- Python 3.x
- Administrative privileges (for `netsh` configuration)
- ICMP connectivity to target host

## Usage

### Linux
1. Clone the repository:
   ```bash
   git clone https://github.com/henrrrychau/mtu/
   cd mtu-optimizer
   ```
2. Make the script executable:
   ```bash
   chmod +x mtu_linux.py
   ```
3. Run the script:
   ```bash
   sudo ./mtu_linux.py
   ```

### Windows
1. Download the repository
2. Open Command Prompt as Administrator
3. Navigate to the repository folder
4. Run:
   ```cmd
   python mtu_windows.py
   ```

## Customization

### Target IP Address
Both scripts default to Google's public DNS (8.8.8.8). Modify the `target_ip` variable in the script if you need to use a different target (e.g., in regions with ICMP restrictions).

### Network Interface
- Linux: Change `interface_name` (e.g., `eth0`, `wlp3s0`)
- Windows: Change `interface_name` (e.g., "Wi-Fi", "Ethernet")

## Troubleshooting

| Issue                          | Solution                                                                 |
|--------------------------------|--------------------------------------------------------------------------|
| "Target unreachable"           | Check network connectivity and firewall settings                        |
| "Abnormally low MTU"           | Verify network configuration for misconfigured routers/proxies           |
| Permission denied              | Run with sudo (Linux) or as Administrator (Windows)                     |
| MTU detection failed           | Try a different target IP or check for ICMP blocking                    |

## Examples

### Linux
```bash
# Set MTU for wireless interface to optimal value
sudo python3 mtu_linux.py
```

### Windows
```cmd
python mtu_windows.py
```

## Important Notes

1. **Network Impact**: MTU changes can affect all traffic on the interface
2. **Safety First**: Test in a controlled environment before production use
3. **Backup Configuration**: Consider backing up original MTU settings
4. **Regional Restrictions**: Some networks block ICMP traffic - adjust target IP accordingly
