from pymodbus.client.sync import ModbusTcpClient
import pika
import time
import json

def send_to_rabbitmq(data):
    # RabbitMQ connection parameters with username and password
    credentials = pika.PlainCredentials('smartpulse', 'WDb3#Je9h4q6l')
    parameters = pika.ConnectionParameters('rabbitmq-server', credentials=credentials)
    
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare an exchange named 'modbus_data_exchange' of type 'fanout'
    #channel.exchange_declare(exchange='modbus_data_exchange', exchange_type='direct')

    # Publish the data to the exchange with timestamp as the routing key
    channel.basic_publish(exchange='modbus_data_exchange', routing_key='', body=json.dumps(data))
    print(f"Sent to RabbitMQ exchange: {data}")

    # Close the connection
    connection.close()

def read_registers_and_send():
    client = ModbusTcpClient('modbus-simulator-server', port=5020)

    try:
        client.connect()

        while True:
            starting_address = 0
            num_registers = 3

            try:
                response = client.read_holding_registers(starting_address, num_registers, unit=0x01)

                if not response.isError():
                    # Get current timestamp and format the data
                    timestamp = int(time.time())
                    registers_values = response.registers

                    # Prepare the JSON data with timestamp and registers separately
                    data = {
                        'timestamp': timestamp,
                        'registers': {
                            f'register_{i}': value for i, value in enumerate(registers_values, start=1)
                        }
                    }

                    # Send the data to RabbitMQ exchange
                    send_to_rabbitmq(data)

                else:
                    print("Modbus request failed:", response)

            except Exception as e:
                print("Exception during Modbus communication:", str(e))

            time.sleep(1)

    finally:
        client.close()

# Read registers and send to RabbitMQ exchange
read_registers_and_send()
