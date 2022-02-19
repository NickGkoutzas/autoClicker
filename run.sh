sudo apt update -y && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt autoclean -y;
sudo apt install -y python3-pip && pip install selenium;cd autoClicker;
tar -xvf geckodriver-v0.30.0-linux64.tar.gz && sudo mv geckodriver /usr/local/bin;
export PATH=$PATH:/usr/local/bin/geckodriver && sudo apt install -y firefox;clear;
