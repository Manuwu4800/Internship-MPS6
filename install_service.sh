#!/bin/bash

SERVICE_NAME="valveserver"
SCRIPT_PATH="/home/smm/valveServer.py"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "Creating the $SERVICE_NAME service..."

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Valve control service via GPIO
After=network.target

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_PATH
User=root
Restart=always
WorkingDirectory=$(dirname $SCRIPT_PATH)
StandardOutput=inherit
StandardError=inherit

[Install]
WantedBy=multi-user.target
EOF

echo "Enabling the service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service
sudo systemctl start $SERVICE_NAME.service

echo "✅ Service $SERVICE_NAME installed and started automatically at boot."
