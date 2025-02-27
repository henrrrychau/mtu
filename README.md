# MTU Optimizer: Simplified Guide

**What is MTU?**  
MTU stands for Maximum Transmission Unit. It’s the largest packet size your network can handle without breaking it into smaller pieces. A well-configured MTU improves internet speed and reliability.

**What Does This Tool Do?**  
This tool automatically finds the best MTU for your network and sets it up for you. It works on both Linux and Windows.

---

## Key Features
- **Finds the Ideal MTU**: Uses a smart search method (binary search) to quickly pinpoint the best MTU.
- **Works on Multiple Systems**: Separate scripts for Linux and Windows.
- **Sets Up Automatically**: Applies the optimal MTU to your network settings.
- **Safe to Use**: Checks if the MTU meets internet standards (RFC 791).

---

## What You Need
### Linux (`mtu_linux.py`)
- Python 3
- `iproute2` (comes with the `ip` command)
- Ability to send ICMP requests (ping) to a target host

### Windows (`mtu_windows.py`)
- Python 3
- Administrative rights (to change network settings)
- Ability to send ICMP requests (ping) to a target host

---

## How to Use

### For Linux Users
1. **Get the Tool**:
   ```bash
   git clone https://github.com/henrrrychau/mtu/
   cd mtu-optimizer
   ```
2. **Make the Script Runable**:
   ```bash
   chmod +x mtu_linux.py
   ```
3. **Run the Script**:
   ```bash
   sudo ./mtu_linux.py
   ```

### For Windows Users
1. **Download the Tool**:
   - Save the repository files to your computer.
2. **Open Command Prompt as Administrator**:
   - Search for “Command Prompt,” right-click it, and select “Run as administrator.”
3. **Navigate to the Tool’s Folder**:
   - Use the `cd` command to go to the folder where you saved the files.
4. **Run the Script**:
   ```cmd
   python mtu_windows.py
   ```

---

## Customization Options

### Change the Target IP Address
- The tool uses Google’s DNS (8.8.8.8) by default. If your network blocks ICMP traffic, change the `target_ip` in the script to another address (e.g., your router’s IP).

### Select a Network Interface
- **Linux**: Change `interface_name` to your network interface (e.g., `eth0` for wired, `wlp3s0` for wireless).
- **Windows**: Change `interface_name` to your network adapter name (e.g., “Wi-Fi” or “Ethernet”).

---

## Troubleshooting
| **Problem**               | **Solution**                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| “Target unreachable”       | Check your internet connection and firewall settings.                       |
| “MTU too low”             | Ensure your router or network settings are not causing issues.              |
| “Permission denied”       | Run the script with `sudo` (Linux) or as Administrator (Windows).           |
| “MTU detection failed”    | Try a different target IP or check if ICMP is blocked by your network.      |

---

## Examples

### Linux
```bash
# Optimize MTU for your wireless network
sudo python3 mtu_linux.py
```

### Windows
```cmd
# Optimize MTU for your Wi-Fi connection
python mtu_windows.py
```

---

## Important Notes
1. **Impact on Network**: Changing the MTU affects all traffic on the selected network interface.
2. **Test First**: Try the tool in a safe environment before using it in production.
3. **Backup Settings**: Keep a record of your original MTU in case you need to revert.
4. **Regional Restrictions**: Some networks block ICMP traffic. Use a different target IP if needed.
