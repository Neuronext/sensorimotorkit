import socket
import time
import csv

def get_glove_port_number(hand):
    if hand == "right":
        port_number = 53450
    else:
        port_number = 53451
    return port_number

def get_glove_ip():
    ip_address = "127.0.0.1"
    return ip_address

def get_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.1)
    return sock

def get_data(t, sock, ip, port):
    if t != time.time():
        message = '{"type":"ping"}'.encode()
        sock.sendto(message, (ip, port))
        t = time.time()
    # Receive a message from the target IP address and port
    try:
        data, address = sock.recvfrom(10000)
        decoded = data.decode()
        return decoded, t
    except Exception as e:
        return "nothing", t

def collect(seconds, save_path):

    # Set the IP address and port number to send to
    ip = get_glove_ip()
    hand = "right"
    port = get_glove_port_number(hand)

    # Create a UDP socket
    sock = get_socket()

    t = 0
    output = []
    # Set the duration for data collection (in seconds)
    collection_duration = seconds
    start_time = time.time()

    while time.time() - start_time < collection_duration:
        new_data, t = get_data(t, sock, ip, port)
        output.append(new_data)

    glove_file_name = "gloves.csv"
    glove_path = save_path + "/" + glove_file_name
    with open(glove_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in output:
            writer.writerow(row)
    print("saved glove data")
