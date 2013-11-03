homework-05
===========

my 5th software homework


requirments
===========
*  python 2.7.x
*  simplejson



usage
===========
*  set server host: change `host = ""` in goldserver.py to your host. If you test it on localhost, you can leave it blank.
*  set client host: change `host = ""` in goldclient.py to the server's host. If you test it on localhost, you can leave it blank.
*  change the html to fit the host: you should find all host settings on the html and change them to the server's host.
*  start server: `$ python goldserver.py 1`, note that 1 is the first type of game, you can also set it to 2.
*  start client: `$ python goldclient username password`. If you want to **auto play**, you can run `$ python auto_play.py`, this will read user infomation from all_user_data.txt and auto connect them to the server.
*  double click to open the **result.html**, you will see the dynamic result.
*  stop the game by stop the server, clients will stop by themselves.

License
===========
Based on [WTFPL](http://en.wikipedia.org/wiki/WTFPL).
