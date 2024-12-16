#!/bin/bash
echo "Updating system packages and installing Poppler..."
apt-get update
apt-get install -y poppler-utils
