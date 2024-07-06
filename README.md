## Complete Port Scanner with Threading (Python)

This repository contains a Python script for comprehensive port scanning with multithreading.

**What it Does**

This script scans a target IP address for open ports using a specified range or a list of ports. It leverages multithreading for faster execution by scanning multiple ports concurrently.

**Concepts Used**

- **Sockets:** Used for network communication to establish connections with ports on the target IP.
- **Threading:** Used to run multiple port scans simultaneously, improving performance.
- **Command-Line Arguments (argparse):** Allows users to customize the scan through command-line options.
- **Logging:** Provides informative messages about the scan configuration, progress, and results.

**Running the Script**

1. **Prerequisites:**
   - Python 3 with the following libraries installed:
     ```bash
     pip install socket argparse
     ```
2. **Download/Clone:** Download or clone this repository.
3. **Command-Line:** Open a terminal in the project directory.
4. **Run with Arguments:** Execute the script with desired options:

   ```bash
   python3 port_scanner.py <target_ip> [options]

   Options:
   -p, --ports (default: 1-1024): Comma-separated list of ports to scan (e.g., -p 22,80,443)
   -t, --timeout (default: 1): Timeout in seconds for socket connections
   -c, --concurrency (default: 100): Number of concurrent threads for scanning
   -o, --output (default: scan_results.txt): Output file for scan results
   ```

   Example: Scan ports 22, 80, and 443 on 192.168.1.1 with a 2-second timeout and save results to scan_output.txt:

   ```bash
   python3 port_scanner.py 192.168.1.1 -p 22,80,443 -t 2 -o scan_output.txt
   ```

**Output**

- The script logs informative messages about the scan configuration to the console.
- It writes information about open ports to the specified output file (default: scan_results.txt).
- Each line in the output file represents an open port, formatted as `IP:port is open`.

