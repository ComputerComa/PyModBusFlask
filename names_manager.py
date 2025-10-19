import os
import pickle
import json
from typing import Dict, Optional

class NamesManager:
    """Manages custom names for Modbus addresses"""
    
    def __init__(self, names_file='modbus_names.bin'):
        self.names_file = names_file
        self.names = {
            'inputs': {},
            'coils': {},
            'registers': {}
        }
        self.load_names()
    
    def load_names(self) -> bool:
        """Load names from binary file"""
        try:
            if os.path.exists(self.names_file):
                with open(self.names_file, 'rb') as f:
                    self.names = pickle.load(f)
                return True
            else:
                # Initialize with default names if file doesn't exist
                self.initialize_default_names()
                return True
        except Exception as e:
            print(f"Error loading names: {e}")
            self.initialize_default_names()
            return False
    
    def save_names(self) -> bool:
        """Save names to binary file"""
        try:
            with open(self.names_file, 'wb') as f:
                pickle.dump(self.names, f)
            return True
        except Exception as e:
            print(f"Error saving names: {e}")
            return False
    
    def initialize_default_names(self):
        """Initialize with default names"""
        self.names = {
            'inputs': {i: f"Input_{i}" for i in range(16)},
            'coils': {i: f"Coil_{i}" for i in range(16)},
            'registers': {i: f"Register_{i}" for i in range(16)}
        }
    
    def get_name(self, category: str, address: int) -> str:
        """Get name for a specific address"""
        return self.names.get(category, {}).get(address, f"{category.title()}_{address}")
    
    def set_name(self, category: str, address: int, name: str) -> bool:
        """Set name for a specific address"""
        if category not in self.names:
            self.names[category] = {}
        
        self.names[category][address] = name
        return self.save_names()
    
    def get_all_names(self) -> Dict:
        """Get all names"""
        return self.names.copy()
    
    def set_all_names(self, names: Dict) -> bool:
        """Set all names at once"""
        self.names = names.copy()
        return self.save_names()
    
    def export_to_json(self, filename: str = 'modbus_names.json') -> bool:
        """Export names to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.names, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    def import_from_json(self, filename: str) -> bool:
        """Import names from JSON file"""
        try:
            with open(filename, 'r') as f:
                imported_names = json.load(f)
            
            # Validate structure
            if all(key in imported_names for key in ['inputs', 'coils', 'registers']):
                self.names = imported_names
                return self.save_names()
            else:
                print("Invalid JSON structure")
                return False
        except Exception as e:
            print(f"Error importing from JSON: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset all names to defaults"""
        self.initialize_default_names()
        return self.save_names()
    
    def add_address(self, category: str, address: int, name: str = None) -> bool:
        """Add a new address with optional name"""
        if name is None:
            name = f"{category.title()}_{address}"
        
        if category not in self.names:
            self.names[category] = {}
        
        self.names[category][address] = name
        return self.save_names()
    
    def remove_address(self, category: str, address: int) -> bool:
        """Remove an address"""
        if category in self.names and address in self.names[category]:
            del self.names[category][address]
            return self.save_names()
        return False
