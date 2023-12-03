from pymodbus.client.sync import ModbusTcpClient
import time

def read_all_registers():
    # Connect to the Modbus TCP slave server
    client = ModbusTcpClient('localhost', port=5020)

    try:
        # Open connection
        client.connect()

        while True:
            # Read all holding registers (for example, 100 registers)
            starting_address = 0
            num_registers = 3  # Adjust this value according to the number of registers you want to read

            try:
                response = client.read_holding_registers(starting_address, num_registers, unit=0x01)

                if not response.isError():
                    # Print the values read from the holding registers
                    print("Holding register values:", response.registers)
                else:
                    print("Modbus request failed:", response)

            except Exception as e:
                print("Exception during Modbus communication:", str(e))

            time.sleep(1)  # Wait for 1 second before the next read

    finally:
        # Close connection
        client.close()

# Call the function to continuously read all holding registers
read_all_registers()
