sudo apt-get update -y
sudo apt-get install -y python-software-properties
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo npm config set registry http://registry.npmjs.org/
sudo apt-get update -y
sudo apt-get install -y vim-nox build-essential git python-pip python-dev screen libpcre3-dev python-software-properties python g++ make nodejs git build-essential vim memcached libmysqlclient-dev libevent-dev libxml2-dev libxslt1-dev libmemcached-dev

sudo pip install virtualenvwrapper

echo '' >> $HOME/.bashrc
echo export WORKON_HOME=$HOME/.virtualenvs >> $HOME/.bashrc 
echo source /usr/local/bin/virtualenvwrapper.sh >> $HOME/.bashrc

export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv exhibiaenv
workon exhibiaenv

