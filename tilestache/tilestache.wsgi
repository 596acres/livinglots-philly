import sys
import os

# For TileStache
sys.path.append('/home/v2v/.virtualenvs/llphilly/lib/python2.7/site-packages/')

# For Mapnik
os.putenv('LD_LIBRARY_PATH', '/home/v2v/lib')
sys.path.append('/home/v2v/lib/python2.7/site-packages/')

import mapnik
import TileStache

application = TileStache.WSGITileServer('/home/v2v/webapps/tiles_gu/tilestache/config/production.cfg')
