Name: liman-ssh
Version: %VERSION%
Release: 0
License: MIT
Requires: novnc, python39, python3-paramiko, python3-tornado, python3-websockify, openssl
Prefix: /liman
Summary: Liman SSH and NoVNC Service
BuildArch: x86_64

%description
Liman SSH and NoVNC Service

%pre

%prep

%build

%install
cp -rfa %{_app_dir} %{buildroot}

%post -p /bin/bash
mkdir -p /liman/webssh

rm -rf /liman/keys/vnc
mkdir -p /liman/keys/vnc
chmod 700 /liman/keys/vnc
touch /liman/keys/vnc/config
chown liman:liman /liman/keys/vnc /liman/keys/vnc/config
chmod 700 /liman/keys/vnc/config

chown -R liman:liman /liman/webssh

# Create Systemd Service
if [ -f "/etc/systemd/system/liman-ssh.service" ]; then
    echo "Liman SSH Terminal Service Already Added.";
else
    echo """
[Unit]
Description=Liman SSH Terminal Service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=liman
ExecStart=/usr/bin/python3 /liman/webssh/run.py
[Install]
WantedBy=multi-user.target
    """ > /etc/systemd/system/liman-ssh.service
fi

# Create Systemd Service
if [ -f "/etc/systemd/system/liman-novnc.service" ]; then
    echo "Liman NoVNC Service Already Added.";
else
    echo """
[Unit]
Description=Liman NoVNC Service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=liman
ExecStart=/usr/bin/websockify --web=/usr/share/novnc 6080 --cert=/liman/certs/liman.crt --key=/liman/certs/liman.key --token-plugin TokenFile --token-source /liman/keys/vnc/config
[Install]
WantedBy=multi-user.target
    """ > /etc/systemd/system/liman-novnc.service
fi

systemctl daemon-reload

systemctl disable liman-webssh 2>/dev/null
systemctl enable liman-ssh 2>/dev/null

systemctl restart liman-ssh 2>/dev/null

systemctl disable liman-vnc 2>/dev/null
systemctl enable liman-novnc 2>/dev/null

systemctl restart liman-novnc 2>/dev/null

%clean

%files
/liman/webssh/*

%define _unpackaged_files_terminate_build 0
