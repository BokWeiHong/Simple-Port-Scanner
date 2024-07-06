#!/usr/bin/python3
import socket
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def set_socket_timeout(timeout):
    # Set the default timeout for all socket operations
    socket.setdefaulttimeout(timeout)

def scan_port(ip, port):
    try:
        # Create a new socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set a 1-second timeout for this specific connection attempt
            result = sock.connect_ex((ip, port))  # Attempt to connect to the ip:port
            if result == 0:
                return True  # Port is open if the connection was successful
    except Exception as e:
        logging.error(f'Error scanning {ip} on port {port}: {e}')
    return False  # Port is closed or an error occurred

def scan_ports(ip, ports, concurrency, timeout):
    set_socket_timeout(timeout)
    open_ports = []
    # Use ThreadPoolExecutor for concurrent port scanning
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit scan_port function for each port to the executor
        future_to_port = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    open_ports.append(port)
                    logging.info(f'[ + ] {ip}:{port} is open')
                else:
                    logging.info(f'[ - ] {ip}:{port} is closed')
            except Exception as e:
                logging.error(f'Error scanning port {port}: {e}')
    return open_ports

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Complete Port Scanner')
    parser.add_argument('ip', type=str, help='Target IP address')
    parser.add_argument('-p', '--ports', type=int, nargs='+', default=range(1, 1025), help='List of ports to scan (default: 1-1024)')
    parser.add_argument('-t', '--timeout', type=int, default=1, help='Timeout for socket connections (default: 1 second)')
    parser.add_argument('-c', '--concurrency', type=int, default=100, help='Number of concurrent threads (default: 100)')
    parser.add_argument('-o', '--output', type=str, default='scan_results.txt', help='Output file for scan results (default: scan_results.txt)')
    args = parser.parse_args()

    # Log the start of the scan with the provided parameters
    logging.info(f'Starting port scan for {args.ip} on ports {min(args.ports)}-{max(args.ports)} with timeout {args.timeout}s and concurrency {args.concurrency}')

    # Perform the port scan
    open_ports = scan_ports(args.ip, args.ports, args.concurrency, args.timeout)

    # Write the results to the output file
    with open(args.output, 'w') as f:
        for port in open_ports:
            f.write(f'{args.ip}:{port} is open\n')
    
    logging.info(f'Port scan completed. Results saved to {args.output}')

if __name__ == '__main__':
    main()