import socket
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os

# Define the IP and port to listen on
server_address = ('0.0.0.0', 514)

# Create a dictionary to store unique source-destination pairs
unique_connections = {}

# Create a socket to listen for incoming syslog messages
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

# Configure logging
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)

log_formatter = logging.Formatter('%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_handler = RotatingFileHandler(
    os.path.join(log_directory, f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_vas3k-l2tp.log"),
    maxBytes=10 * 1024 * 1024,
    backupCount=5
)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

while True:
    data, client_address = server_socket.recvfrom(4096)

    # Extract the source and destination IP addresses from the message
    message = data.decode('utf-8')
    src_ip = message.split("->")[0].split(",")[-1].split(":")[0]
    dst_info = message.split("->")[1].split(",")[0].strip().split(":")
    dst_ip = dst_info[0]
    dst_port = dst_info[1]
    user_secret = message.split("in:<")[1].split(">")[0]  # Extract data field

    # Construct a unique key based on source and destination IP addresses
    src_dst_key = (src_ip, dst_ip)

    # Update the unique_connections dictionary with the new message
    if src_dst_key not in unique_connections:
        unique_connections[src_dst_key] = []

    unique_connections[src_dst_key].append((user_secret, message))

    # Check if the current message is the first one for the source-destination pair
    if len(unique_connections[src_dst_key]) == 1:
        datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log data to the rotating log file
        logger.info(f"{datetime_now}, {user_secret},{src_ip}->{dst_ip}:{dst_port}")

server_socket.close()
