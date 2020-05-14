#!/usr/bin/env python2.7
"""
Generats XML routing output according to the content provided by FDSN station
webservice. It obtain network and station inventories in text format.
This script does not handle "priorities", every network gets #1 priority.
"""

from urllib.request import urlopen

# FDSN webservice URL base address
URL_BASE = "http://webservices.ingv.it/"

URL_ws_endpoint = dict(station=URL_BASE + "fdsnws/station/1/",
                       dataselect=URL_BASE + "fdsnws/dataselect/1/",
                       wfcatalog=URL_BASE + "eidaws/wfcatalog/1/",
                       )

# Query for getting network level information
NETWORKS_URL = URL_ws_endpoint["station"] + \
               "query?level=network&format=text"

# Query for getting station level information
STATIONS_URL = URL_ws_endpoint["station"] + \
               "query?level=station&format=text&network={network}"

services = ("station", "dataselect", "wfcatalog")

# Networks that need station-level declaration, ie. one declaration for
# each station in the network). This is necessary in particular for
# shared networks code in EIDA.
# All others networks get a simple network-level declaration (station="*")
show_stations = ('Z3', '4C')

# skip these networks while generating XML
ignore_networks = []

# temporary solution to get virtual networks
vnetworks = ("_MOST",
             "_MOST-ICO",
             "_NFOIRPINA",
             "_NFOTABOO",
             )

XML_level0 = """\
<?xml version="1.0" encoding="utf-8"?>
<ns0:routing xmlns:ns0="http://geofon.gfz-potsdam.de/ns/Routing/1.0/">

{routing}
{vnetworks}
</ns0:routing>\
"""

XML_route_spec = """\
    <ns0:{ws_name} address="{ws_endpoint}query" priority="1" \
start="{start}" end="{end}" />
"""

XML_route_net = """\
  <ns0:route networkCode="{network}" stationCode="*" \
locationCode="*" streamCode="*">
{specs}\
  </ns0:route>
"""

# template for station level declaration
XML_route_sta = """\
  <ns0:route networkCode="{network}" stationCode="{station}" \
locationCode="*" streamCode="*">
{specs}\
  </ns0:route>
"""

XML_vnet = """\
  <ns0:vnetwork networkCode="{vnetwork}">
{streams}\
  </ns0:vnetwork>
"""

XML_vnet_stream = """\
    <ns0:stream networkCode="{network}" stationCode="{station}" \
locationCode="*" streamCode="*" \
start="{start}" end="{end}"/>
"""


def get_xml_route_specs(kv):
    """
    generate XML for route specifications
    """

    xml = ""
    for service in services:
        kv.update({"ws_name": service,
                   "ws_endpoint": URL_ws_endpoint[service]}
                  )
        xml += XML_route_spec.format(**kv)

    return xml


def get_xml_station_level(network):
    """
    generate XML for station-level routing
    """

    f = urlopen(STATIONS_URL.format(**{"network": network}))
    # skip first line (comment)
    f.readline()

    xml = ""
    # for each station...
    for line in f:
        keys = ("network", "station",
                "latitude", "longitude", "elevation", "name",
                "start", "end")
        values = (line.decode('utf8').strip().split('|'))
        kv = dict(zip(keys, values))

        specs = get_xml_route_specs(kv)
        kv.update({"specs": specs})

        xml += XML_route_sta.format(**kv)

    return xml


def get_xml_network_level(kv):

    specs = get_xml_route_specs(kv)
    kv.update({"specs": specs})

    xml = XML_route_net.format(**kv)
    return xml


def get_xml_routing():
    """
    generate XML for networks
    """

    # get networks
    f = urlopen(NETWORKS_URL)
    # skip first line (comment)
    f.readline()

    #
    

    xml = ""
    # process regular networks
    # with urlopen(NETWORKS_URL, 'rb') as f:
    #    lines = [x.decode('utf8').strip() for x in f.readlines()]

    for line in f:    
        keys = ("network", "description", "start", "end", "total")
        values = (line.decode('utf8').strip().split('|'))
       
        kv = dict(zip(keys, values))
        kv.update(URL_ws_endpoint)

        network = kv["network"]

        # skip some networks
        if network in ignore_networks:
            continue

        if network in show_stations:
            # XML for station level
            xml += get_xml_station_level(network)
        else:
            # XML for network level
            xml += get_xml_network_level(kv)

    return xml


def get_xml_vnetwork_streams(vnetwork):
    """
    generate XML for vnetwork streams
    """

    # get virtual network definition
    f = urlopen(STATIONS_URL.format(**{"network": vnetwork}))
    # skip first line (comment)
    f.readline()

    xml = ""
    # for each station...
    for line in f:
        keys = ("network", "station",
                "latitude", "longitude", "elevation", "name",
                "start", "end")
        values = (line.decode('utf8').strip().split('|'))
        kv = dict(zip(keys, values))

        xml += XML_vnet_stream.format(**kv)

    return xml


def get_xml_vnetworks():
    # process Virtual networks
    xml = ""
    for vnetwork in vnetworks:
        xml += XML_vnet.format(
            **{"vnetwork": vnetwork,
               "streams": get_xml_vnetwork_streams(vnetwork)}
            )

    return xml


if __name__ == '__main__':

    # add XML header and footer
    xml = XML_level0.format(**{"routing": get_xml_routing(),
                               "vnetworks": get_xml_vnetworks(),
                               }
                            )

    print(xml)

