import hashlib
import requests
from bs4 import BeautifulSoup, Tag
import time
import logging
from scapy.all import sniff
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WifiMonitor:
    def __init__(self, url, login_url, username, password, refresh_interval=5, packet_sniff_count=100):
        self.url = url
        self.login_url = login_url
        self.username = username
        self.password = password
        self.refresh_interval = refresh_interval
        self.packet_sniff_count = packet_sniff_count
        self.previous_data = {}
        self.total_data = {}
        self.device_names = {
            "e4:0d:36:de:d0:1e": "PC-raslen",
            "a8:41:f4:8f:92:9f": "PC-nader",
            "14:99:3e:c2:f0:38": "Phone-nader"
        }
        self.session = requests.Session()
        self.packet_size_bytes = 1500
        self.packet_count = 0
        self.total_packet_size = 0

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
            response = self.session.post(self.login_url, data=login_data, headers=headers, timeout=5)
            response.raise_for_status()
            if "window.location.href='index.htm'" in response.text:
                logging.info("Login successful.")
                return True
            else:
                logging.warning("Login failed. Check credentials.")
                return False
        except requests.RequestException as e:
            logging.error(f"Error logging in: {e}")
            return False

    def fetch_data(self):
        try:
            response = self.session.get(self.url, timeout=5)
            response.raise_for_status()
            if response.url == self.login_url:
                logging.info("Session expired. Re-authenticating...")
                if self.login():
                    return self.fetch_data()
                return None
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None

    def parse_data(self, html):
        try:
            soup = BeautifulSoup(html, "html.parser")
            rows = [row for row in soup.find_all("tr") if isinstance(row, Tag)][1:]
            users = []
            seen_macs = set()
            for row in rows:
                cols = [col for col in row.find_all("td") if isinstance(col, Tag)]
                if len(cols) < 3:
                    continue
                mac_address = cols[0].text.strip()
                if mac_address in seen_macs:
                    continue
                seen_macs.add(mac_address)
                try:
                    tx_packets = int(cols[1].text.strip())
                    rx_packets = int(cols[2].text.strip())
                except ValueError:
                    logging.warning(f"Invalid data for {mac_address}, skipping entry.")
                    continue
                users.append({"mac": mac_address, "tx": tx_packets, "rx": rx_packets})
            return users
        except Exception as e:
            logging.error(f"Error parsing data: {e}")
            return []

    def calculate_speed(self, current_data):
        speed_results = []
        new_previous_data = {}
        for user in current_data:
            mac = user["mac"]
            tx = user["tx"]
            rx = user["rx"]
            if mac in self.previous_data:
                tx_speed = (tx - self.previous_data[mac]["tx"]) / self.refresh_interval
                rx_speed = (rx - self.previous_data[mac]["rx"]) / self.refresh_interval
            else:
                tx_speed, rx_speed = 0, 0
            tx_mbps = (tx_speed * self.packet_size_bytes * 8) / (1024 * 1024)
            rx_mbps = (rx_speed * self.packet_size_bytes * 8) / (1024 * 1024)
            if mac not in self.total_data:
                self.total_data[mac] = {"tx": 0, "rx": 0}
            self.total_data[mac]["tx"] += tx_speed * self.packet_size_bytes / (1024 * 1024)
            self.total_data[mac]["rx"] += rx_speed * self.packet_size_bytes / (1024 * 1024)
            total_tx_mb = self.total_data[mac]["tx"]
            total_rx_mb = self.total_data[mac]["rx"]
            total_usage_mb = total_tx_mb + total_rx_mb
            speed_results.append({
                "mac": mac,
                "tx_speed": tx_mbps,
                "rx_speed": rx_mbps,
                "total_usage": total_usage_mb
            })
            new_previous_data[mac] = user
        self.previous_data = new_previous_data
        return speed_results

    def display_data(self, speed_data):
        logging.info("\nActive Users:")
        sorted_speed_data = sorted(speed_data, key=lambda x: x["total_usage"], reverse=True)
        print("{:<20} {:<20} {:<15} {:<15} {:<15}".format("Device Name", "MAC Address", "Download Speed (Mbps)", "Upload Speed (Mbps)", "Total Usage (MB)"))
        print("-" * 85)
        for user in sorted_speed_data:
            device_name = self.device_names.get(user["mac"], "unknown")
            print("{:<20} {:<20} {:<15} {:<15} {:<15}".format(
                device_name,
                user["mac"],
                round(user["tx_speed"], 2),
                round(user["rx_speed"], 2),
                round(user["total_usage"], 2)
            ))

    def packet_callback(self, packet):
        self.packet_count += 1
        self.total_packet_size += len(packet)
        self.packet_size_bytes = self.total_packet_size / self.packet_count
        logging.debug(f"Captured packet size: {len(packet)} bytes, Average packet size: {self.packet_size_bytes} bytes")

    def start_packet_sniffing(self):
        sniff(prn=self.packet_callback, count=self.packet_sniff_count)

    def run(self):
        if not self.login():
            logging.error("Initial login failed. Exiting.")
            return
        sniffing_thread = threading.Thread(target=self.start_packet_sniffing)
        sniffing_thread.start()
        while True:
            html = self.fetch_data()
            if html:
                users = self.parse_data(html)
                speed_data = self.calculate_speed(users)
                self.display_data(speed_data)
            time.sleep(self.refresh_interval)

if __name__ == "__main__":
    monitor = WifiMonitor(
        url="http://192.168.1.1/wlstatbl.htm",
        login_url="http://192.168.1.1/login.cgi",
        username="topadmin",
        password="topadmin"
    )
    monitor.run()
