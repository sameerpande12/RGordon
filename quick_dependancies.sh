export LANGUAGE="en_US.UTF-8"
echo 'LANGUAGE="en_US.UTF-8"' >> /etc/default/locale
echo 'LC_ALL="en_US.UTF-8"' >> /etc/default/locale
sudo apt-get update
sudo apt-get install -y python
sudo apt-get install -y python3
sudo apt-get install -y python3-pip

sudo apt install -y python3-pip
sudo pip3 install --upgrade pip

#pip3 install matplotlib
python3 -m pip install numpy
python3 -m pip install pandas
#python3 -m pip install matplotlib
#pip install --user matplotlib


sudo add-apt-repository ppa:keithw/mahimahi -y
sudo apt-get update
sudo apt-get install -y mahimahi
sudo dpkg-reconfigure -p critical dash
sudo sysctl -w net.ipv4.ip_forward=1
sudo apt-get install -y libnetfilter-queue-dev
sudo apt-get install screen

#apt-get install sudo -y   # for Docker

sudo apt-get install -y iputils-ping
sudo apt-get install -y wget
sudo apt-get install -y psmisc
sudo apt install -y net-tools

sudo apt-get install -y curl
sudo curl -sL https://deb.nodesource.com/setup_10.x | sudo bash
sudo apt-get install -y nodejs

npm install
