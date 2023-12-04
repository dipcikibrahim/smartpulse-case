import pika
from prometheus_client import start_http_server, Gauge
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# Create a Prometheus gauge metric
prometheus_metric = Gauge('rabbitmq_data', 'Data received from RabbitMQ', ['register'])
prometheus_time_metric = Gauge('rabbitmq_data_time', 'Data received from RabbitMQ', ['time'])

token = "RAlhlqCqwmGdeZj00UdyA5NAwDqZoJK6tufeoF6gN7W6ckhdjJ6bgreWgowS6JIAxQbDk4wAsgY_FN5SAV_qTw=="
org = "sp"
url = "http://influx-db:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="spb"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Function to process received messages and expose as Prometheus metrics
def consume_and_publish():
    try:
        # Connect to RabbitMQ server
        credentials = pika.PlainCredentials('smartpulse', 'WDb3#Je9h4q6l')
        parameters = pika.ConnectionParameters('rabbitmq-server', credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Declare a queue named 'modbus_data_queue' or exchange if using fanout
        # channel.queue_declare(queue='modbus_data_queue')
        # Bind to exchange if needed:
        # channel.exchange_declare(exchange='modbus_data_exchange', exchange_type='fanout')
        # channel.queue_bind(exchange='modbus_data_exchange', queue='modbus_data_queue')

        def callback(ch, method, properties, body):
            try:
                # Process the received JSON data
                data = json.loads(body)
                
                # Extract data and publish as Prometheus metrics
                timestamp = data['timestamp']
                registers = data['registers']
                for register, value in registers.items():
                    prometheus_metric.labels(register=register).set(value)
                    prometheus_time_metric.labels(time='timestamp').set(timestamp)
                    # Influx Export
                    point = (
                        Point("registers")
                        .tag("registerName", register)
                        .field("data", value)
                    )
                    write_api.write(bucket=bucket, org="sp", record=point)
                    print(f"Received from RabbitMQ: Register {register}, Value {value}, Timestamp {timestamp}")

            except Exception as e:
                print(f"Exception while processing RabbitMQ message: {e}")

        # Consume messages from the queue or exchange
        channel.basic_consume(queue='modbus_data_queue', on_message_callback=callback, auto_ack=True)
        # If using exchange instead:
        # channel.basic_consume(queue='modbus_data_queue', on_message_callback=callback, auto_ack=True)

        # Start Prometheus HTTP server to expose metrics
        start_http_server(8001)  # Expose metrics on port 8001

        print("RabbitMQ consumer started...")
        # Start consuming messages
        channel.start_consuming()
    except:
        # Can send data to centralized log analyzer such as Sentry.io
        print("Error occured!")

if __name__ == '__main__':
    # Run the consumer function
    consume_and_publish()
