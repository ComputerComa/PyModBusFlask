class ModbusWebClient {
    constructor() {
        this.connected = false;
        this.autoRefreshInterval = null;
        this.refreshInterval = 5000; // 5 seconds
        this.lastManualWrite = null; // Track last manual write time
        this.writeDelay = 2000; // 2 seconds delay before allowing auto-refresh
        this.names = { inputs: {}, coils: {}, registers: {} };
        this.nameEditingMode = { inputs: false, coils: false, registers: false };
        
        this.initializeEventListeners();
        this.checkConnectionStatus();
        this.loadNames();
    }

    initializeEventListeners() {
        // Connection buttons
        document.getElementById('connect-btn').addEventListener('click', () => this.connect());
        document.getElementById('disconnect-btn').addEventListener('click', () => this.disconnect());
        
        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', () => this.refreshAll());
        
        // Auto refresh toggle
        document.getElementById('auto-refresh').addEventListener('change', (e) => {
            if (e.target.checked) {
                this.startAutoRefresh();
            } else {
                this.stopAutoRefresh();
            }
        });
        
        // Names management buttons
        document.getElementById('save-names-btn').addEventListener('click', () => this.saveNames());
        document.getElementById('load-names-btn').addEventListener('click', () => this.loadNames());
        document.getElementById('reset-names-btn').addEventListener('click', () => this.resetNames());
        document.getElementById('export-names-btn').addEventListener('click', () => this.exportNames());
        document.getElementById('import-names-btn').addEventListener('click', () => document.getElementById('import-file-input').click());
        document.getElementById('import-file-input').addEventListener('change', (e) => this.importNames(e));
        
        // Start auto refresh if enabled
        if (document.getElementById('auto-refresh').checked) {
            this.startAutoRefresh();
        }
    }

    async connect() {
        const host = document.getElementById('host').value;
        const port = document.getElementById('port').value;
        const unitId = document.getElementById('unit-id').value;

        if (!host || !port || !unitId) {
            this.showToast('Please fill in all connection fields', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/connect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    host: host,
                    port: parseInt(port),
                    unit_id: parseInt(unitId)
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.connected = true;
                this.updateConnectionStatus();
                this.showToast('Connected successfully!', 'success');
                this.refreshAll();
            } else {
                this.showToast(result.message, 'error');
            }
        } catch (error) {
            this.showToast('Connection failed: ' + error.message, 'error');
        }
    }

    async disconnect() {
        try {
            const response = await fetch('/api/disconnect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.connected = false;
                this.updateConnectionStatus();
                this.showToast('Disconnected successfully!', 'info');
                this.clearData();
            } else {
                this.showToast(result.message, 'error');
            }
        } catch (error) {
            this.showToast('Disconnection failed: ' + error.message, 'error');
        }
    }

    async checkConnectionStatus() {
        try {
            const response = await fetch('/api/status');
            const result = await response.json();
            
            this.connected = result.connected;
            this.updateConnectionStatus();
        } catch (error) {
            console.error('Status check failed:', error);
        }
    }

    updateConnectionStatus() {
        const statusElement = document.getElementById('connection-status');
        const connectBtn = document.getElementById('connect-btn');
        const disconnectBtn = document.getElementById('disconnect-btn');
        
        if (this.connected) {
            statusElement.textContent = 'Connected';
            statusElement.className = 'badge bg-success ms-2';
            connectBtn.disabled = true;
            disconnectBtn.disabled = false;
        } else {
            statusElement.textContent = 'Disconnected';
            statusElement.className = 'badge bg-secondary ms-2';
            connectBtn.disabled = false;
            disconnectBtn.disabled = true;
            this.stopAutoRefresh();
        }
    }

    async refreshAll() {
        if (!this.connected) return;

        // Don't auto-refresh if we just made a manual write
        if (this.lastManualWrite && (Date.now() - this.lastManualWrite) < this.writeDelay) {
            console.log('Skipping auto-refresh due to recent manual write');
            return;
        }

        try {
            await Promise.all([
                this.refreshInputs(),
                this.refreshCoils(),
                this.refreshRegisters()
            ]);
            
            this.updateLastRefreshTime();
        } catch (error) {
            console.error('Refresh failed:', error);
            this.showToast('Refresh failed: ' + error.message, 'error');
        }
    }

    async refreshInputs() {
        try {
            const response = await fetch('/api/read_inputs');
            const result = await response.json();
            
            if (result.status === 'success') {
                this.displayInputs(result.data);
            } else {
                console.error('Failed to read inputs:', result.message);
            }
        } catch (error) {
            console.error('Input refresh error:', error);
        }
    }

    async refreshCoils() {
        try {
            const response = await fetch('/api/read_coils');
            const result = await response.json();
            
            if (result.status === 'success') {
                this.displayCoils(result.data);
            } else {
                console.error('Failed to read coils:', result.message);
            }
        } catch (error) {
            console.error('Coil refresh error:', error);
        }
    }

    async refreshRegisters() {
        try {
            const response = await fetch('/api/read_holding_registers');
            const result = await response.json();
            
            if (result.status === 'success') {
                this.displayRegisters(result.data);
            } else {
                console.error('Failed to read registers:', result.message);
            }
        } catch (error) {
            console.error('Register refresh error:', error);
        }
    }

    displayInputs(inputs) {
        const container = document.getElementById('inputs-container');
        container.innerHTML = '';
        
        for (const [address, value] of Object.entries(inputs)) {
            const div = document.createElement('div');
            div.className = 'd-flex justify-content-between align-items-center mb-2';
            
            const name = this.names.inputs[address] || `Input_${address}`;
            const nameElement = this.nameEditingMode.inputs ? 
                `<input type="text" class="form-control form-control-sm" value="${name}" 
                        onchange="modbusClient.setName('inputs', ${address}, this.value)"
                        style="width: 120px;">` :
                `<span>${name}:</span>`;
            
            div.innerHTML = `
                ${nameElement}
                <span class="badge ${value ? 'bg-success' : 'bg-secondary'}">${value ? 'ON' : 'OFF'}</span>
            `;
            container.appendChild(div);
        }
    }

    displayCoils(coils) {
        const container = document.getElementById('coils-container');
        container.innerHTML = '';
        
        for (const [address, value] of Object.entries(coils)) {
            const div = document.createElement('div');
            div.className = 'd-flex justify-content-between align-items-center mb-2';
            
            const name = this.names.coils[address] || `Coil_${address}`;
            const nameElement = this.nameEditingMode.coils ? 
                `<input type="text" class="form-control form-control-sm" value="${name}" 
                        onchange="modbusClient.setName('coils', ${address}, this.value)"
                        style="width: 120px;">` :
                `<span>${name}:</span>`;
            
            div.innerHTML = `
                ${nameElement}
                <label class="toggle-switch">
                    <input type="checkbox" ${value ? 'checked' : ''} onchange="modbusClient.writeCoil(${address}, this.checked)">
                    <span class="slider"></span>
                </label>
            `;
            container.appendChild(div);
        }
    }

    displayRegisters(registers) {
        const container = document.getElementById('registers-container');
        container.innerHTML = '';
        
        for (const [address, value] of Object.entries(registers)) {
            const div = document.createElement('div');
            div.className = 'd-flex justify-content-between align-items-center mb-2';
            
            const name = this.names.registers[address] || `Register_${address}`;
            const nameElement = this.nameEditingMode.registers ? 
                `<input type="text" class="form-control form-control-sm" value="${name}" 
                        onchange="modbusClient.setName('registers', ${address}, this.value)"
                        style="width: 120px;">` :
                `<span>${name}:</span>`;
            
            div.innerHTML = `
                ${nameElement}
                <div class="input-group" style="width: 150px;">
                    <input type="number" class="form-control register-input" value="${value}" 
                           onchange="modbusClient.writeRegister(${address}, parseInt(this.value))">
                    <button class="btn btn-outline-secondary" type="button" 
                            onclick="modbusClient.writeRegister(${address}, parseInt(this.previousElementSibling.value))">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            `;
            container.appendChild(div);
        }
    }

    async writeCoil(address, value) {
        try {
            // Record the time of manual write
            this.lastManualWrite = Date.now();
            
            const response = await fetch('/api/write_coil', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    address: address,
                    value: value
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showToast(`Coil ${address} set to ${value ? 'ON' : 'OFF'}`, 'success');
                // Manual refresh after successful write to show updated state
                setTimeout(() => {
                    this.refreshCoils();
                }, 500);
            } else {
                this.showToast(result.message, 'error');
                // Refresh to get current state
                this.refreshCoils();
            }
        } catch (error) {
            this.showToast('Write failed: ' + error.message, 'error');
            // Refresh to get current state
            this.refreshCoils();
        }
    }

    async writeRegister(address, value) {
        try {
            // Record the time of manual write
            this.lastManualWrite = Date.now();
            
            const response = await fetch('/api/write_register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    address: address,
                    value: value
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showToast(`Register ${address} set to ${value}`, 'success');
                // Manual refresh after successful write to show updated state
                setTimeout(() => {
                    this.refreshRegisters();
                }, 500);
            } else {
                this.showToast(result.message, 'error');
                // Refresh to get current state
                this.refreshRegisters();
            }
        } catch (error) {
            this.showToast('Write failed: ' + error.message, 'error');
            // Refresh to get current state
            this.refreshRegisters();
        }
    }

    clearData() {
        document.getElementById('inputs-container').innerHTML = '<p class="text-muted">Connect to view inputs</p>';
        document.getElementById('coils-container').innerHTML = '<p class="text-muted">Connect to view coils</p>';
        document.getElementById('registers-container').innerHTML = '<p class="text-muted">Connect to view registers</p>';
    }

    startAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
        
        this.autoRefreshInterval = setInterval(() => {
            if (this.connected) {
                this.refreshAll();
            }
        }, this.refreshInterval);
    }

    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
    }

    updateLastRefreshTime() {
        const now = new Date();
        document.getElementById('last-update').textContent = now.toLocaleTimeString();
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const toastBody = document.getElementById('toast-body');
        const toastHeader = toast.querySelector('.toast-header');
        
        // Set message
        toastBody.textContent = message;
        
        // Set icon and color based on type
        const icon = toastHeader.querySelector('i');
        icon.className = `fas ${this.getToastIcon(type)} me-2`;
        
        toast.className = `toast ${this.getToastClass(type)}`;
        
        // Show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    getToastIcon(type) {
        switch (type) {
            case 'success': return 'fa-check-circle';
            case 'error': return 'fa-exclamation-circle';
            case 'warning': return 'fa-exclamation-triangle';
            default: return 'fa-info-circle';
        }
    }

    getToastClass(type) {
        switch (type) {
            case 'success': return 'bg-success text-white';
            case 'error': return 'bg-danger text-white';
            case 'warning': return 'bg-warning text-dark';
            default: return '';
        }
    }

    // Names Management Functions
    async loadNames() {
        try {
            const response = await fetch('/api/get_names');
            const result = await response.json();
            
            if (result.status === 'success') {
                this.names = result.data;
            }
        } catch (error) {
            console.error('Failed to load names:', error);
        }
    }

    async setName(category, address, name) {
        try {
            const response = await fetch('/api/set_name', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: category,
                    address: parseInt(address),
                    name: name
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.names[category][address] = name;
                this.showToast(`Name for ${category} ${address} updated`, 'success');
            } else {
                this.showToast(result.message, 'error');
            }
        } catch (error) {
            this.showToast('Failed to set name: ' + error.message, 'error');
        }
    }

    async saveNames() {
        try {
            const response = await fetch('/api/save_names', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();
            this.showToast(result.message, result.status === 'success' ? 'success' : 'error');
        } catch (error) {
            this.showToast('Failed to save names: ' + error.message, 'error');
        }
    }

    async resetNames() {
        if (confirm('Are you sure you want to reset all names to defaults?')) {
            try {
                const response = await fetch('/api/reset_names', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const result = await response.json();
                
                if (result.status === 'success') {
                    this.names = result.data;
                    this.showToast(result.message, 'success');
                    this.refreshAll(); // Refresh display to show new names
                } else {
                    this.showToast(result.message, 'error');
                }
            } catch (error) {
                this.showToast('Failed to reset names: ' + error.message, 'error');
            }
        }
    }

    async exportNames() {
        try {
            window.location.href = '/api/export_names';
            this.showToast('Names exported successfully', 'success');
        } catch (error) {
            this.showToast('Failed to export names: ' + error.message, 'error');
        }
    }

    async importNames(event) {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/import_names', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.names = result.data;
                this.showToast(result.message, 'success');
                this.refreshAll(); // Refresh display to show new names
            } else {
                this.showToast(result.message, 'error');
            }
        } catch (error) {
            this.showToast('Failed to import names: ' + error.message, 'error');
        }

        // Clear file input
        event.target.value = '';
    }
}

// Global function for name editing toggle
function toggleNameEditing(category) {
    modbusClient.nameEditingMode[category] = !modbusClient.nameEditingMode[category];
    
    // Update button text
    const button = event.target;
    const isEditing = modbusClient.nameEditingMode[category];
    button.innerHTML = isEditing ? '<i class="fas fa-check"></i> Done' : '<i class="fas fa-edit"></i> Edit Names';
    button.className = isEditing ? 'btn btn-sm btn-success' : 'btn btn-sm btn-outline-primary';
    
    // Refresh the display to show/hide edit fields
    if (modbusClient.connected) {
        modbusClient.refreshAll();
    }
}

// Initialize the application
const modbusClient = new ModbusWebClient();
