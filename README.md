# Modbus TCP Client with Flask Web Interface

A Python-based Modbus TCP client with a modern web interface built using Flask. This application allows you to connect to Modbus TCP servers, monitor discrete inputs, and control coils and holding registers through a user-friendly web interface.

## Features

- **Modbus TCP Client**: Connect to Modbus TCP servers
- **Real-time Monitoring**: Monitor discrete inputs in real-time
- **Control Interface**: Toggle coils and modify holding registers
- **Custom Names**: Edit custom names for inputs, coils, and registers
- **Save/Restore**: Save and restore custom names to/from binary files
- **Import/Export**: Import and export names as JSON files
- **Modern Web UI**: Bootstrap-based responsive interface
- **Auto Refresh**: Automatic data refresh with configurable intervals
- **Error Handling**: Comprehensive error handling and logging
- **Configuration Management**: Easy configuration through environment variables

## Requirements

- Python 3.7+
- pip (Python package installer)

## Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd PyModBusFlask
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application** (optional)
   
   Create a `.env` file in the project root with your preferred settings:
   ```env
   MODBUS_HOST=localhost
   MODBUS_PORT=502
   MODBUS_UNIT_ID=1
   FLASK_DEBUG=True
   LOG_LEVEL=INFO
   ```

## Usage

### Starting the Application

1. **Run the Flask application**
   ```bash
   python app.py
   ```

2. **Open your web browser**
   
   Navigate to `http://localhost:5000` to access the web interface.

### Using the Web Interface

1. **Connection Settings**
   - Enter the Modbus server IP address or hostname
   - Set the port (default: 502)
   - Set the Unit ID (default: 1)
   - Click "Connect" to establish connection

2. **Monitoring Data**
   - **Discrete Inputs**: Read-only display of input states
   - **Coils**: Toggle switches for controlling coil states
   - **Holding Registers**: Input fields for modifying register values

3. **Auto Refresh**
   - Enable/disable automatic data refresh
   - Set refresh interval (default: 5 seconds)
   - Manual refresh button available

4. **Names Management**
   - **Edit Names**: Click "Edit Names" button on any section to customize names
   - **Save Names**: Save custom names to binary file (`modbus_names.bin`)
   - **Load Names**: Load previously saved names from binary file
   - **Reset Names**: Reset all names to default values
   - **Export Names**: Export names to JSON file for backup/sharing
   - **Import Names**: Import names from JSON file

### Modbus Address Ranges

The application reads from the following default address ranges:
- **Discrete Inputs**: 0-15 (16 inputs)
- **Coils**: 0-15 (16 coils)
- **Holding Registers**: 0-15 (16 registers)

You can modify these ranges by editing the `ModbusClient` class in `modbus_client.py`.

## API Endpoints

The application provides the following REST API endpoints:

### Modbus Operations
- `POST /api/connect` - Connect to Modbus server
- `POST /api/disconnect` - Disconnect from Modbus server
- `GET /api/status` - Get connection status
- `GET /api/read_inputs` - Read discrete inputs
- `GET /api/read_coils` - Read coils
- `GET /api/read_holding_registers` - Read holding registers
- `POST /api/write_coil` - Write to a coil
- `POST /api/write_register` - Write to a holding register

### Names Management
- `GET /api/get_names` - Get all custom names
- `POST /api/set_name` - Set name for a specific address
- `POST /api/save_names` - Save all names to binary file
- `POST /api/load_names` - Load names from binary file
- `POST /api/reset_names` - Reset all names to defaults
- `GET /api/export_names` - Export names to JSON file
- `POST /api/import_names` - Import names from JSON file

## Project Structure

```
PyModBusFlask/
├── app.py                 # Main Flask application
├── modbus_client.py       # Modbus TCP client implementation
├── names_manager.py       # Names management functionality
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── test_installation.py   # Installation test script
├── example.env            # Example environment configuration
├── README.md             # This file
├── templates/
│   └── index.html        # Main web interface template
└── static/
    └── app.js            # JavaScript for web interface
```

## Configuration

### Environment Variables

- `MODBUS_HOST`: Default Modbus server host (default: localhost)
- `MODBUS_PORT`: Default Modbus server port (default: 502)
- `MODBUS_UNIT_ID`: Default Modbus unit ID (default: 1)
- `FLASK_DEBUG`: Enable Flask debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)

### Modifying Address Ranges

To change the address ranges for reading Modbus data, modify the following variables in `modbus_client.py`:

```python
self.input_start = 0      # Starting address for discrete inputs
self.input_count = 16     # Number of discrete inputs to read
self.coil_start = 0       # Starting address for coils
self.coil_count = 16      # Number of coils to read
self.register_start = 0   # Starting address for holding registers
self.register_count = 16  # Number of holding registers to read
```

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify the Modbus server is running and accessible
   - Check firewall settings
   - Ensure the correct IP address and port are used

2. **Permission Denied**
   - Some Modbus servers require specific unit IDs
   - Check if the server allows writes to coils and registers

3. **Timeout Errors**
   - Network latency issues
   - Server may be overloaded
   - Try increasing timeout values in the Modbus client

### Logging

The application logs important events and errors. Check the console output for detailed information about connection status and any errors that occur.

## Development

### Adding New Features

1. **New API Endpoints**: Add routes in `app.py`
2. **Modbus Functions**: Extend `modbus_client.py` with new Modbus operations
3. **UI Components**: Modify `templates/index.html` and `static/app.js`

### Testing

You can test the application with a Modbus TCP simulator such as:
- ModbusPal
- QModMaster
- SimpleModbusMaster

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
