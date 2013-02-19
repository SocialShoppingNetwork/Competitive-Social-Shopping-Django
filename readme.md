
[TESTED in Ubuntu 12.04 64 bits]

1. sudo apt-get update
2. sudo apt-get install virtualenvwrapper git ipython sqlite3 python-dev libmemcached-dev nodejs npm memcached build-essential

3. source ~/.bashrc

4. mkvirtualenv exhibiaenv


5. git clone https://github.com/exhibia/exhibia.git Exhibiasrc

6. cd Exhibiasrc
   pip install -U pip
   pip install -r requirements_local.txt

6. copy Exhibiasrc/exhibia/nodeapp/app.js outside of exhibia or Exhibiasrc folders wherever you want

7. In the directory where you have app.js runs it
  npm install socket.io memcached

8. add 127.0.0.1 testing.exhibia.com        to your /etc/hosts file


##### TO RUN Exhibia ######

running web server 

1 workon exhibiaenv

2 cd  Exhibiasrc/exhibia

3 python manage.py runserver


running daemon to update timers

1. workon exhibiaenv

2. cd Exhibiasrc/exhibia

3. python manage.py bidomatic


running timers server

1. go to to directory where you copy app.'s

2. node app.js


