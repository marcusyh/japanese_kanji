import os
import subprocess
import argparse

def generate_service_file(args):
    service_content = f'''
[Unit]
Description=WebUI Service
After=network.target

[Service]
User={args.user}
ExecStart=/usr/bin/python3 {args.path}/webUI/http_server.py
WorkingDirectory={args.path}/webUI
Restart=always

[Install]
WantedBy=multi-user.target
'''
    
    with open('/etc/systemd/system/webui.service', 'w') as f:
        f.write(service_content)

def configure_ufw(port):
    try:
        subprocess.run(['sudo', 'ufw', 'allow', str(port)], check=True)
        print(f"UFW rule added for port {port}")
    except subprocess.CalledProcessError:
        print("Failed to add UFW rule. Make sure you have necessary permissions.")

def deploy_service(args):
    # Generate service file
    generate_service_file(args)
    print("Service file generated.")

    # Reload systemd
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
    print("Systemd reloaded.")

    # Enable and start the service
    subprocess.run(['sudo', 'systemctl', 'enable', 'webui.service'], check=True)
    subprocess.run(['sudo', 'systemctl', 'start', 'webui.service'], check=True)
    print("WebUI service enabled and started.")

    # Configure UFW
    configure_ufw(args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy WebUI service")
    parser.add_argument('--user', required=True, help="User to run the service")
    parser.add_argument('--path', required=True, help="Path to the WebUI directory")
    parser.add_argument('--port', type=int, default=8000, help="Port to allow in UFW")
    
    args = parser.parse_args()
    
    deploy_service(args)