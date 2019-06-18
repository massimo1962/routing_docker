#
# EIDA Routing WS prototype
#
# (c) 2014 Javier Quinteros, GEOFON team
# <javier@gfz-potsdam.de>
#
# ----------------------------------------------------------------------

import sys
import os

directory = "/var/www/eidaws/routing/1"  #os.path.dirname(__file__)

sys.path.append(directory)
import routing

application = routing.application
