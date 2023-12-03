from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import random
import threading
import time

# Function to update holding registers with random values every second
def update_registers(context, register_address):
    while True:
        try:
            values = [random.randint(0, 100) for _ in range(3)]  # Generate 3 random values
            context[4].setValues(3, register_address, values)  # Update holding registers starting at address 0x00 (address 4 in pymodbus)
            time.sleep(1)
        except:
            print("Error occured while updating registers!") #Send the log to logger.

try:
    # Create a Modbus server context
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0]*3),
    )
    context = ModbusServerContext(slaves=store, single=True)

    # Start a thread to continuously update holding registers with random values
    update_thread = threading.Thread(target=update_registers, args=(context, 0), daemon=True)
    update_thread.start()

    # Start the Modbus TCP server
    server = StartTcpServer(context, address=("0.0.0.0", 5020))
except:
    print("Error occured while creating and starting the server!") #Send the log to logger.

# Keep the server running until manually stopped
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
