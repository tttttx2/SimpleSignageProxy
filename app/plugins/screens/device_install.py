import json
import os
import requests
import re


#todo input sanitization

def read(id=False): # GET
    if id == False or id == "":
        return {"text": "This is the Device onboarding script that you can run on e.g. a raspberry pi. <br> Nothing else to do here. <br>To get the installation script, use <br><br><a id=\"device_install_url\" href=\"/plugins/screens/device_install?id=\">THIS</a><script>document.getElementById(\"device_install_url\").href += window.location.hostname</script>"}
    else:
        script="""
apt install unclutter xdotool

mkdir -p /etc/chromium/policies/managed /etc/chromium/policies/recommended
mkdir -p /home/pi/.config/lxsession/LXDE-pi/


echo -ne '{{\\n"HomepageLocation":"http://'$(hostname)'.{0}",\\n"NewTabPageLocation":"http://'$(hostname)'.{0}",\\n"ShowHomeButton":true,\\n"RestoreOnStartup":5}}'>/etc/chromium/policies/managed/CHROME-GLOBAL.json

cat << EOF
#! /bin/bash
export XAUTHORITY=/home/pi/.Xauthority
export DISPLAY=:0
#xdotool search --onlyvisible --class chromium windowfocus key F5
xdotool search --onlyvisible --class chromium windowfocus key ctrl+t
sleep 2
xdotool search --onlyvisible --class chromium windowfocus key ctrl+Tab
sleep 30
xdotool search --onlyvisible --class chromium windowfocus key ctrl+w
EOF > /home/pi/refresh.sh

chmod +x /home/pi/refresh.sh
echo -ne "dtoverlay=disable-bt\\ndtoverlay=disable-wifi\\navoid_warnings=1" >> /boot/config.txt
echo -ne "dtoverlay=disable-bt\\ndtoverlay=disable-wifi\\navoid_warnings=1" >> /boot/config.txt


crontab -l -u pi > mycron
echo "*/5 * * * * /home/pi/refresh.sh >/dev/null 2>&1" >> mycron
crontab -u pi mycron
echo "@reboot dmesg -n 1\\n0 0 * * * reboot" > mycron
crontab -u root mycron
rm mycron


cat << EOF

# Bildschirmschoner deaktivieren
@xset s off
@xset -dpms
@xset s noblank

# Chromium automatisch im incognito- und Kiosk-Modus starten und eine Seite öffnen
@chromium-browser --kiosk http://$(hostname).{0} --kiosk --noerrdialogs --disable-infobars --no-first-run --enable-features=OverlayScrollbar --start-maximized
#switchtab = bash ~/switchtab.sh

# Mauszeiger deaktivieren
@unclutter

EOF > /home/pi/.config/lxsession/LXDE-pi/autostart

        """.format(id)
        return script
