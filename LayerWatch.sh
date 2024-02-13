## Set up for flash to boot on system start

sudo cp flask.service /lib/systemd/system
sudo systemctl enable flask

## Sudo reboot yourself and go to http://172.22.166.50:5051