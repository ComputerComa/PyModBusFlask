import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Modbus TCP Client Flask app"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Modbus Default Configuration
    DEFAULT_MODBUS_HOST = os.environ.get('MODBUS_HOST', 'localhost')
    DEFAULT_MODBUS_PORT = int(os.environ.get('MODBUS_PORT', '502'))
    DEFAULT_MODBUS_UNIT_ID = int(os.environ.get('MODBUS_UNIT_ID', '1'))
    
    # Reading Ranges
    DEFAULT_INPUT_START = 0
    DEFAULT_INPUT_COUNT = 16
    DEFAULT_COIL_START = 0
    DEFAULT_COIL_COUNT = 16
    DEFAULT_REGISTER_START = 0
    DEFAULT_REGISTER_COUNT = 16
    
    # Auto Refresh Settings
    DEFAULT_REFRESH_INTERVAL = 5000  # 5 seconds
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def get_modbus_config():
        """Get default Modbus configuration"""
        return {
            'host': Config.DEFAULT_MODBUS_HOST,
            'port': Config.DEFAULT_MODBUS_PORT,
            'unit_id': Config.DEFAULT_MODBUS_UNIT_ID
        }
