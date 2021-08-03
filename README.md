# zhaga-hackathon
A Machine Vision approach to the Zhaga Sensor Hackathon 2021

## Update Service
First stop the hackathon service from running
```
sudo systemctl stop hackathon.service
```

To update the service command. Edit the `hacktahon.service` file. Then iniside the project folder run:
```
sudo cp hackathon.service /etc/systemd/system/hackathon.service
```

Then reload the daemon:
```
sudo systemctl daemon-reload
```

And start the service
```
sudo systemctl start hackathon.service
```

## Service Output
to see live data feed from the service run
```
journalctl -f -o cat _SYSTEMD_UNIT=hackathon.service
```

## WiFi AP Details
```
IP address: 10.3.141.1
Username: admin
Password: secret
DHCP range: 10.3.141.50 — 10.3.141.255
```