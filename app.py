from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import os
import logging
import threading
import signal
import sys
from modbus_client import ModbusClient
from config import Config
from names_manager import NamesManager

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize Modbus client and names manager
modbus_client = ModbusClient()
names_manager = NamesManager()

# Global variable to track server shutdown
server_shutdown = threading.Event()

def shutdown_server():
    """Function to gracefully shutdown the server"""
    server_shutdown.set()
    os._exit(0)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', config=Config)

@app.route('/api/connect', methods=['POST'])
def connect():
    """Connect to Modbus server"""
    try:
        data = request.json
        host = data.get('host', Config.DEFAULT_MODBUS_HOST)
        port = int(data.get('port', Config.DEFAULT_MODBUS_PORT))
        unit_id = int(data.get('unit_id', Config.DEFAULT_MODBUS_UNIT_ID))
        
        result = modbus_client.connect(host, port, unit_id)
        if result:
            return jsonify({'status': 'success', 'message': 'Connected successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to connect'})
    except Exception as e:
        logger.error(f"Connection error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    """Disconnect from Modbus server"""
    try:
        modbus_client.disconnect()
        return jsonify({'status': 'success', 'message': 'Disconnected successfully'})
    except Exception as e:
        logger.error(f"Disconnection error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/status')
def status():
    """Get connection status"""
    return jsonify({'connected': modbus_client.is_connected()})

@app.route('/api/read_inputs')
def read_inputs():
    """Read discrete inputs"""
    try:
        if not modbus_client.is_connected():
            return jsonify({'status': 'error', 'message': 'Not connected'})
        
        inputs = modbus_client.read_discrete_inputs()
        return jsonify({'status': 'success', 'data': inputs})
    except Exception as e:
        logger.error(f"Read inputs error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/read_coils')
def read_coils():
    """Read coils"""
    try:
        if not modbus_client.is_connected():
            return jsonify({'status': 'error', 'message': 'Not connected'})
        
        coils = modbus_client.read_coils()
        return jsonify({'status': 'success', 'data': coils})
    except Exception as e:
        logger.error(f"Read coils error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/read_holding_registers')
def read_holding_registers():
    """Read holding registers"""
    try:
        if not modbus_client.is_connected():
            return jsonify({'status': 'error', 'message': 'Not connected'})
        
        registers = modbus_client.read_holding_registers()
        return jsonify({'status': 'success', 'data': registers})
    except Exception as e:
        logger.error(f"Read holding registers error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/write_coil', methods=['POST'])
def write_coil():
    """Write to a coil"""
    try:
        if not modbus_client.is_connected():
            return jsonify({'status': 'error', 'message': 'Not connected'})
        
        data = request.json
        address = int(data.get('address'))
        value = bool(data.get('value'))
        
        result = modbus_client.write_coil(address, value)
        if result:
            return jsonify({'status': 'success', 'message': 'Coil written successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to write coil'})
    except Exception as e:
        logger.error(f"Write coil error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/write_register', methods=['POST'])
def write_register():
    """Write to a holding register"""
    try:
        if not modbus_client.is_connected():
            return jsonify({'status': 'error', 'message': 'Not connected'})
        
        data = request.json
        address = int(data.get('address'))
        value = int(data.get('value'))
        
        result = modbus_client.write_register(address, value)
        if result:
            return jsonify({'status': 'success', 'message': 'Register written successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to write register'})
    except Exception as e:
        logger.error(f"Write register error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

# Names Management API endpoints
@app.route('/api/get_names')
def get_names():
    """Get all custom names"""
    try:
        names = names_manager.get_all_names()
        return jsonify({'status': 'success', 'data': names})
    except Exception as e:
        logger.error(f"Get names error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/set_name', methods=['POST'])
def set_name():
    """Set name for a specific address"""
    try:
        data = request.json
        category = data.get('category')  # 'inputs', 'coils', or 'registers'
        address = int(data.get('address'))
        name = data.get('name', '')
        
        if not category or category not in ['inputs', 'coils', 'registers']:
            return jsonify({'status': 'error', 'message': 'Invalid category'})
        
        result = names_manager.set_name(category, address, name)
        if result:
            return jsonify({'status': 'success', 'message': 'Name saved successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save name'})
    except Exception as e:
        logger.error(f"Set name error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/save_names', methods=['POST'])
def save_names():
    """Save all names to binary file"""
    try:
        result = names_manager.save_names()
        if result:
            return jsonify({'status': 'success', 'message': 'Names saved successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save names'})
    except Exception as e:
        logger.error(f"Save names error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/load_names', methods=['POST'])
def load_names():
    """Load names from binary file"""
    try:
        result = names_manager.load_names()
        if result:
            names = names_manager.get_all_names()
            return jsonify({'status': 'success', 'message': 'Names loaded successfully', 'data': names})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to load names'})
    except Exception as e:
        logger.error(f"Load names error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/reset_names', methods=['POST'])
def reset_names():
    """Reset all names to defaults"""
    try:
        result = names_manager.reset_to_defaults()
        if result:
            names = names_manager.get_all_names()
            return jsonify({'status': 'success', 'message': 'Names reset to defaults', 'data': names})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to reset names'})
    except Exception as e:
        logger.error(f"Reset names error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/export_names')
def export_names():
    """Export names to JSON file"""
    try:
        filename = 'modbus_names_export.json'
        result = names_manager.export_to_json(filename)
        if result:
            return send_file(filename, as_attachment=True, download_name='modbus_names.json')
        else:
            return jsonify({'status': 'error', 'message': 'Failed to export names'})
    except Exception as e:
        logger.error(f"Export names error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/import_names', methods=['POST'])
def import_names():
    """Import names from uploaded JSON file"""
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'})
        
        if file and file.filename.endswith('.json'):
            # Save uploaded file temporarily
            temp_filename = 'temp_import.json'
            file.save(temp_filename)
            
            # Import names
            result = names_manager.import_from_json(temp_filename)
            
            # Clean up temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            
            if result:
                names = names_manager.get_all_names()
                return jsonify({'status': 'success', 'message': 'Names imported successfully', 'data': names})
            else:
                return jsonify({'status': 'error', 'message': 'Failed to import names'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid file format. Please upload a JSON file.'})
    except Exception as e:
        logger.error(f"Import names error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the server"""
    try:
        logger.info("Server shutdown requested from web interface")
        # Use a thread to shutdown after response is sent
        threading.Timer(1.0, shutdown_server).start()
        return jsonify({'status': 'success', 'message': 'Server shutting down...'})
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
