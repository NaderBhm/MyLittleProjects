import sys
import hashlib
import requests
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QSizePolicy, QDialog, QInputDialog
from PyQt6.QtCore import QTimer, Qt
from bs4 import BeautifulSoup, Tag

class WifiMonitorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.monitoring = False
        self.refresh_interval = 1250  # Twice the speed (1.25 seconds)
        self.url = "http://192.168.1.1/wlstatbl.htm"
        self.login_url = "http://192.168.1.1/login.cgi"
        self.username = "topadmin"
        self.password = "topadmin"
        self.session = requests.Session()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.previous_data = {}
        self.total_data = {}
        self.device_names = self.load_device_names()
        self.packet_size_bytes = 1500

    def md5_hash(self, string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def login(self):
        hashed_username = self.md5_hash(self.username)
        hashed_password = self.md5_hash(self.password)
        
        login_data = {
            'username': self.username,
            'password': self.password,
            'usernameEncrypt': hashed_username,
            'passwordEncrypt': hashed_password,
            'submit.htm?login.htm': '0'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://192.168.1.1/login.htm',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }

        try:
            response = self.session.post(self.login_url, data=login_data, headers=headers)
            response.raise_for_status()
            if "window.location.href='index.htm'" in response.text:
                return True
            else:
                self.status_label.setText("Status: Login Failed - Check Credentials")
                return False
        except requests.RequestException as e:
            self.status_label.setText(f"Status: Login Error - {e}")
            return False

    def fetch_data(self):
        try:
            response = self.session.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.status_label.setText(f"Status: Fetch Error - {e}")
            return None
    
    def parse_data(self, html):
        soup = BeautifulSoup(html, "html.parser")
        rows = [row for row in soup.find_all("tr") if isinstance(row, Tag)][1:]
        data = []
        for row in rows:
            cols = [col for col in row.find_all("td") if isinstance(col, Tag)]
            if len(cols) < 3:
                continue
            mac = cols[0].text.strip()
            try:
                tx = int(cols[1].text.strip())
                rx = int(cols[2].text.strip())
                data.append([mac, tx, rx])
            except ValueError:
                continue
        return data
    
    def calculate_speed(self, current_data):
        speed_results = []
        new_previous_data = {}
        for user in current_data:
            mac = user[0]
            tx = user[1]
            rx = user[2]
            if mac in self.previous_data:
                tx_speed = (tx - self.previous_data[mac]["tx"]) / (self.refresh_interval / 1000)
                rx_speed = (rx - self.previous_data[mac]["rx"]) / (self.refresh_interval / 1000)
            else:
                tx_speed, rx_speed = 0, 0
            tx_mbps = (tx_speed * self.packet_size_bytes * 8) / (1024 * 1024)
            rx_mbps = (rx_speed * self.packet_size_bytes * 8) / (1024 * 1024)
            if mac not in self.total_data:
                self.total_data[mac] = {"tx": 0, "rx": 0}
            self.total_data[mac]["tx"] += tx_speed * self.packet_size_bytes / (1024 * 1024)
            self.total_data[mac]["rx"] += rx_speed * self.packet_size_bytes / (1024 * 1024)
            total_usage_mb = self.total_data[mac]["tx"] + self.total_data[mac]["rx"]
            speed_results.append([mac, tx_mbps, rx_mbps, total_usage_mb])
            new_previous_data[mac] = {"tx": tx, "rx": rx}
        self.previous_data = new_previous_data
        speed_results.sort(key=lambda x: x[3], reverse=True)  # Sort by total usage (4th column)
        return speed_results
    
    def update_data(self):
        if not self.monitoring:
            return
        html = self.fetch_data()
        if html:
            users = self.parse_data(html)
            speed_data = self.calculate_speed(users)
            self.table.setRowCount(len(speed_data))
            for row_idx, user in enumerate(speed_data):
                device_name = self.device_names.get(user[0], "Unknown")
                row_data = [device_name] + user
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(round(value, 2) if isinstance(value, float) else value)))
    
    def start_monitoring(self):
        if not self.login():
            self.status_label.setText("Status: Login Failed")
            return
        self.monitoring = True
        self.timer.start(self.refresh_interval)
        self.status_label.setText("Status: Monitoring...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    
    def stop_monitoring(self):
        self.monitoring = False
        self.timer.stop()
        self.status_label.setText("Status: Stopped")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def open_device_manager(self):
        self.device_manager_dialog = DeviceManagerDialog(self.device_names, self)
        self.device_manager_dialog.exec()
        self.save_device_names()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Stopped")
        layout.addWidget(self.status_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Device Name", "MAC Address", "Download (Mbps)", "Upload (Mbps)", "Total Usage (MB)"])
        
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.horizontalHeader().setStyleSheet("background-color: #4CAF50; color: white;")
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.table)
        
        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.start_monitoring)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Monitoring")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)
        
        self.device_manager_button = QPushButton("Manage Devices")
        self.device_manager_button.clicked.connect(self.open_device_manager)
        layout.addWidget(self.device_manager_button)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
                font-size: 12px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
            QTableWidget {
                border: 1px solid #ccc;
                background-color: white;
                color: #333;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                margin: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                margin: 5px;
            }
        """)
        
        self.setLayout(layout)
        self.setWindowTitle("WiFi Monitor")
        self.resize(600, 400)

    def save_device_names(self):
        with open("device_names.json", "w") as file:
            json.dump(self.device_names, file)

    def load_device_names(self):
        try:
            with open("device_names.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

class DeviceManagerDialog(QDialog):
    def __init__(self, device_names, parent=None):
        super().__init__(parent)
        self.device_names = device_names
        self.setWindowTitle("Device Manager")
        self.setGeometry(300, 300, 400, 300)
        self.layout = QVBoxLayout()

        self.device_list_widget = QTableWidget()
        self.device_list_widget.setColumnCount(2)
        self.device_list_widget.setHorizontalHeaderLabels(["MAC Address", "Device Name"])
        self.device_list_widget.horizontalHeader().setStyleSheet("background-color: #2980b9; color: white;")
        self.device_list_widget.verticalHeader().setStyleSheet("background-color: #2980b9; color: white;")
        self.update_device_list()

        self.layout.addWidget(self.device_list_widget)
        
        self.add_button = QPushButton("Add Device")
        self.add_button.clicked.connect(self.add_device)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected Device")
        self.remove_button.clicked.connect(self.remove_device)
        self.layout.addWidget(self.remove_button)
        
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                font-family: Arial, sans-serif;
                color: white;
            }
            QTableWidget {
                background-color: #34495e;
                color: white;
                border: 1px solid #7f8c8d;
            }
            QTableWidget::item {
                padding: 8px;
                border: 1px solid #7f8c8d;
            }
            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                padding: 5px;
            }
            QPushButton {
                background-color: #16a085;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                margin: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
            QLineEdit {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                font-size: 14px;
                margin: 5px;
            }
        """)

    def update_device_list(self):
        self.device_list_widget.setRowCount(len(self.device_names))
        for row_idx, (mac, name) in enumerate(self.device_names.items()):
            self.device_list_widget.setItem(row_idx, 0, QTableWidgetItem(mac))
            self.device_list_widget.setItem(row_idx, 1, QTableWidgetItem(name))

    def add_device(self):
        mac, ok = QInputDialog.getText(self, "Enter MAC Address", "MAC Address:")
        if ok:
            name, ok = QInputDialog.getText(self, "Enter Device Name", "Device Name:")
            if ok:
                self.device_names[mac] = name
                self.update_device_list()

    def remove_device(self):
        selected_row = self.device_list_widget.currentRow()
        if selected_row >= 0:
            mac_item = self.device_list_widget.item(selected_row, 0)
            mac = mac_item.text()
            del self.device_names[mac]
            self.update_device_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WifiMonitorGUI()
    window.show()
    sys.exit(app.exec())
