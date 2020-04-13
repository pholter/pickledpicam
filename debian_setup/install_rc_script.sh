# Install the rc_script
echo "Copying rc_script to init.d folder"
sudo cp -v pickledpicam_rc /etc/init.d
echo "Chmodding script"
sudo chmod -v 755 /etc/init.d/pickledpicam_rc
