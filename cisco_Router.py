import requests                                                                                    
import json                                                                                        
import time

# Deliberate vulnerability: Hardcoded credentials
USERNAME = "admin"
PASSWORD = "admin123"  # Vulnerable: Plaintext password
DEVICE_IP = "192.168.1.1"

# Function to establish a session
def establish_session(ip, username, password):
    """Establish a session with the router."""
    url = f"https://{ip}/restconf/operations/"
    session = requests.Session()

    try:
        # Vulnerable: Disable SSL verification
        session.verify = False

        # Login request
        print("[INFO] Logging into the device...")
        response = session.post(
            url + "login",
            headers={"Content-Type": "application/json"},
            auth=(username, password)
        )

        if response.status_code == 200:
            print("[INFO] Login successful!")
            return session
        else:
            print(f"[ERROR] Login failed: {response.status_code} {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An exception occurred: {e}")
        return None

# Function to configure an interface
def configure_interface(session, ip, interface, config):
    """Configure an interface on the router."""
    url = f"https://{ip}/restconf/data/interfaces/interface={interface}"

    try:
        print(f"[INFO] Configuring interface {interface}...")
        response = session.put(
            url,
            headers={"Content-Type": "application/yang-data+json"},
            data=json.dumps(config),
        )

        if response.status_code == 200:
            print("[INFO] Interface configuration successful.")
        else:
            print(f"[ERROR] Failed to configure interface: {response.status_code} {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An exception occurred: {e}")

# Main function
if __name__ == "__main__":
    # Sample vulnerable configuration
    interface_config = {
        "interface": {
            "name": "GigabitEthernet0/1",
            "description": "Configured via API",
            "enabled": True,
            "ipv4": {
                "address": [
                    {
                        "ip": "192.168.1.100",
                        "netmask": "255.255.255.0"
                    }
                ]
            }
        }
    }

    # Step 1: Establish a session
    session = establish_session(DEVICE_IP, USERNAME, PASSWORD)

    # Step 2: Configure interface if session is valid
    if session:
        configure_interface(session, DEVICE_IP, "GigabitEthernet0/1", interface_config)

    # Step 3: Logout from the session
    if session:
        print("[INFO] Logging out...")
        try:
            session.post(f"https://{DEVICE_IP}/restconf/operations/logout")
            session.close()
            print("[INFO] Logout successful.")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Logout failed: {e}")

    print("[INFO] Script execution completed.")
