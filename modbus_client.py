from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import logging

logger = logging.getLogger(__name__)

class ModbusClient:
    def __init__(self):
        self.client = None
        self.host = None
        self.port = None
        self.unit_id = None
        self.connected = False
        
        # Default ranges for reading
        self.input_start = 0
        self.input_count = 16
        self.coil_start = 0
        self.coil_count = 16
        self.register_start = 0
        self.register_count = 16
    
    def connect(self, host='localhost', port=502, unit_id=1):
        """
        Connect to Modbus TCP server
        
        Args:
            host (str): IP address or hostname
            port (int): Port number (default 502)
            unit_id (int): Unit ID (default 1)
        
        Returns:
            bool: True if connected successfully, False otherwise
        """
        try:
            if self.connected:
                self.disconnect()
            
            self.client = ModbusTcpClient(host, port)
            self.host = host
            self.port = port
            self.unit_id = unit_id
            
            if self.client.connect():
                self.connected = True
                logger.info(f"Connected to Modbus server at {host}:{port}")
                return True
            else:
                logger.error(f"Failed to connect to Modbus server at {host}:{port}")
                return False
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from Modbus server"""
        try:
            if self.client:
                self.client.close()
                self.client = None
            self.connected = False
            logger.info("Disconnected from Modbus server")
        except Exception as e:
            logger.error(f"Disconnection error: {e}")
    
    def is_connected(self):
        """Check if client is connected"""
        return self.connected and self.client is not None
    
    def read_discrete_inputs(self, start=None, count=None):
        """
        Read discrete inputs
        
        Args:
            start (int): Starting address
            count (int): Number of inputs to read
        
        Returns:
            dict: Dictionary with input addresses and values
        """
        if not self.is_connected():
            raise Exception("Not connected to Modbus server")
        
        start = start if start is not None else self.input_start
        count = count if count is not None else self.input_count
        
        try:
            result = self.client.read_discrete_inputs(start, count, unit=self.unit_id)
            if result.isError():
                raise ModbusException(f"Error reading discrete inputs: {result}")
            
            inputs = {}
            for i, value in enumerate(result.bits):
                inputs[start + i] = bool(value)
            
            return inputs
            
        except Exception as e:
            logger.error(f"Error reading discrete inputs: {e}")
            raise
    
    def read_coils(self, start=None, count=None):
        """
        Read coils
        
        Args:
            start (int): Starting address
            count (int): Number of coils to read
        
        Returns:
            dict: Dictionary with coil addresses and values
        """
        if not self.is_connected():
            raise Exception("Not connected to Modbus server")
        
        start = start if start is not None else self.coil_start
        count = count if count is not None else self.coil_count
        
        try:
            result = self.client.read_coils(start, count, unit=self.unit_id)
            if result.isError():
                raise ModbusException(f"Error reading coils: {result}")
            
            coils = {}
            for i, value in enumerate(result.bits):
                coils[start + i] = bool(value)
            
            return coils
            
        except Exception as e:
            logger.error(f"Error reading coils: {e}")
            raise
    
    def read_holding_registers(self, start=None, count=None):
        """
        Read holding registers
        
        Args:
            start (int): Starting address
            count (int): Number of registers to read
        
        Returns:
            dict: Dictionary with register addresses and values
        """
        if not self.is_connected():
            raise Exception("Not connected to Modbus server")
        
        start = start if start is not None else self.register_start
        count = count if count is not None else self.register_count
        
        try:
            result = self.client.read_holding_registers(start, count, unit=self.unit_id)
            if result.isError():
                raise ModbusException(f"Error reading holding registers: {result}")
            
            registers = {}
            for i, value in enumerate(result.registers):
                registers[start + i] = value
            
            return registers
            
        except Exception as e:
            logger.error(f"Error reading holding registers: {e}")
            raise
    
    def write_coil(self, address, value):
        """
        Write to a coil
        
        Args:
            address (int): Coil address
            value (bool): Value to write
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected():
            raise Exception("Not connected to Modbus server")
        
        try:
            result = self.client.write_coil(address, value, unit=self.unit_id)
            if result.isError():
                logger.error(f"Error writing coil {address}: {result}")
                return False
            
            logger.info(f"Coil {address} set to {value}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing coil {address}: {e}")
            return False
    
    def write_register(self, address, value):
        """
        Write to a holding register
        
        Args:
            address (int): Register address
            value (int): Value to write
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected():
            raise Exception("Not connected to Modbus server")
        
        try:
            result = self.client.write_register(address, value, unit=self.unit_id)
            if result.isError():
                logger.error(f"Error writing register {address}: {result}")
                return False
            
            logger.info(f"Register {address} set to {value}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing register {address}: {e}")
            return False
    
    def set_read_ranges(self, input_start=None, input_count=None, 
                       coil_start=None, coil_count=None,
                       register_start=None, register_count=None):
        """
        Set the ranges for reading operations
        
        Args:
            input_start (int): Starting address for discrete inputs
            input_count (int): Number of discrete inputs to read
            coil_start (int): Starting address for coils
            coil_count (int): Number of coils to read
            register_start (int): Starting address for holding registers
            register_count (int): Number of holding registers to read
        """
        if input_start is not None:
            self.input_start = input_start
        if input_count is not None:
            self.input_count = input_count
        if coil_start is not None:
            self.coil_start = coil_start
        if coil_count is not None:
            self.coil_count = coil_count
        if register_start is not None:
            self.register_start = register_start
        if register_count is not None:
            self.register_count = register_count
