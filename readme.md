This file shows how to get this app running on local

# Prepare

## Ubuntu

[TESTED on Ubuntu 12.04 64 bits]

1. sudo apt-get update
1. sudo apt-get install virtualenvwrapper git ipython sqlite3 python-dev libmemcached-dev nodejs npm memcached build-essential
1. source ~/.bashrc
1. mkvirtualenv exhibiaenv
1. git clone https://github.com/exhibia/exhibia.git Exhibiasrc
1. cd Exhibiasrc
   pip install -U pip
   pip install -r requirements.txt
6. copy Exhibiasrc/exhibia/nodeapp/app.js outside of exhibia or Exhibiasrc folders wherever you want
7. In the directory where you have app.js runs it
  npm install socket.io memcached
8. add 127.0.0.1 testing.exhibia.com        to your /etc/hosts file

## OS X
[TESTED on OS X 10.8.2]

```
# Clone the source if haven't
git clone https://github.com/exhibia/exhibia.git
# Install
# * libevent, used by Python's gevent
# * libmemcached, used by Python's pylibmc
brew install libevent libmemcached
# Go to wokring directory
cd exhibia/exhibia
# Update global dependencies
pip install -U pip
# Install local dependencies
sudo pip install -r requirements.txt
```

# Running server

## running web server

```
# Only on Ubunu
workon exhibiaenv
cd exhibia/exhibia
python manage.py runserver
```

## running daemon to update timers

```
# Only on Ubunu
workon exhibiaenv
cd exhibia/exhibia
python manage.py bidomatic
```

# Open in browser

http://localhost:8000/
```
username: U&7cO4^2
password: m9)E6*uU