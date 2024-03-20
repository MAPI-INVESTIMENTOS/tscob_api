import socket
import json
import time

def run_server(host='0.0.0.0', port=2023):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")

        # Send a response after the client connects
        response_data = json.dumps({"message": "Connected to server"}).encode()
        client_socket.send(response_data)

        try:
            login_data = client_socket.recv(1024).decode()
            login_command = json.loads(login_data)
            print(login_data)

            if login_command.get("FunctionCode") == "LOGIN":
                print(f"Received LOGIN command from {address}")

                # Extract the valve ID from the login request
                valve_id = login_command.get("valve_id")
                print(f"Valve ID: {valve_id}")

                commands = [

                    {"FunctionCode": "CLOSE_VALVE", "valve_id": valve_id},
                             ]

                for command in commands:
                    command_json = json.dumps(command)
                    client_socket.send(command_json.encode())
                    time.sleep(5)  # Wait for 5 seconds before sending the next command

                    # Read the response from the client
                    response_data = client_socket.recv(1024).decode()
                    print(f"Response from {address}: {response_data}")

            else:
                print(f"Received command from {address}")

                commands = [
                    {"FunctionCode": "CLOSE_VALVE", "valve_id": "867542052735696"},
                    {"FunctionCode": "OPEN_VALVE", "valve_id": "867542052735696"},
                    {"FunctionCode": "CHECK_VALVE_STATUS", "valve_id": "867542052735696"},
                    {"FunctionCode": "GET_TEMPERATURE", "valve_id": "867542052735696"},
                    {"FunctionCode": "GET_PRESSURE", "valve_id": "867542052735696"},
                    {"FunctionCode": "FLOW_MEASUREMENT", "valve_id": "867542052735696"}
                ]

                for command in commands:
                    command_json = json.dumps(command)
                    client_socket.send(command_json.encode())
                    time.sleep(5)  # Wait for 5 seconds before sending the next command

                    # Read the response from the client
                    response_data = client_socket.recv(1024).decode()
                    print(f"Response from {address}: {response_data}")

        except ConnectionResetError:
            print("Client disconnected")
            client_socket.close()

if __name__ == "__main__":
    run_server()
