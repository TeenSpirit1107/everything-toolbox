#!/bin/bash

echo "==== SSH Host Setup for Ubuntu ===="
echo "==== Author: Yimeng (Rosalind) ===="
echo "==== Github Profile: https://github.com/TeenSpirit1107 ===="
echo "==== Email: yimengteng@link.cuhk.edu.cn ===="

# Ensure root privileges
if [ "$(id -u)" -ne 0 ]; then
  echo "Please run this script as root (e.g., using sudo)"
  exit 1
fi

echo "Enabling UFW firewall (if not already enabled)..."
ufw enable

# Check if openssh-server is installed
echo "Have you installed openssh-server on this machine? If not sure, choose n. [Y/n]"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    if dpkg -l | grep -q openssh-server; then
    echo "OpenSSH Server is already installed."
    else
        echo "Installing OpenSSH Server..."
        apt update
        apt install -y openssh-server
    fi
fi

echo "Enabling and starting SSH service..."
systemctl enable ssh
systemctl start ssh

# Ask user whether to enable secure mode
read -p "Do you want to enable secure mode (only allow specific IP to connect)? [y/N] " SECURE_MODE

if [[ "$SECURE_MODE" =~ ^[Yy]$ ]]; then
    echo "Please run the following command on the CLIENT machine to get the IP address."
    echo "   hostname -I | awk '{print \$1}'"
    echo "Enter the CLIENT's IP address here:"
    read -r ALLOWED_IP
    echo "Allowing SSH access only from IP: $ALLOWED_IP"
    ufw allow from "$ALLOWED_IP" to any port 22 proto tcp
else
    echo "Allowing SSH access from any IP address..."
    ufw allow ssh
fi

HOST_USERNAME=$(whoami)
HOST_IP=$(hostname -I | awk '{print $1}')

echo "SSH setup is complete. You can use the CLIENT device to connect by running:"
echo "   ssh $HOST_USERNAME@$HOST_IP"
echo "After that, you can close this terminal."

