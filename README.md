# Deployment project for EIDAWS routing

This project is related to the deployment at INGV only.

The upstream application repository can be found on GitHub:
* https://github.com/EIDA/routing

The service is modeled routhly after the FDSN standard (version, query). 
The API end point at INGV is 

* www.orfeus-eu.org/eidaws/routing/1/

It returns some basic documentation and a link to the specification of the 
service, `application.wadl` provides further details.

The undocumented method `localconfig` provides access to the local routes only.

* http://webservices.ingv.it/eidaws/routing/1/localconfig
 

## (New deployment Docker based deployment in preparation)

**(TODO)**

## Ad-hoc instance

At the moment the service is provided by an instance of the routing services 
on host `eida.ingv.it`. It is deployed in the directory `/srv/routing/1/` and
run by an outdated Apache server. Service version is `1.0.4`.

## Configuration

### Routing configuration helper script

File: `generate_eida_routing_xml.py`

This small helper script is used to generate the node specific routing 
information. The script is invoced as a cronjob.

Here the relevant crontab entry:

```
sysop@eida:~/soft$ crontab -l
[...]

# Generate routing.xml file
00 00 * * * /usr/bin/python /home/sysop/soft/generate_eida_routing_xml.py > /srv/eida/routing.xml 2> /home/sysop/log/generate_eida_routing_xml.log
```

The information is published under URL: http://eida.rm.ingv.it/routing.xml. 
At the moment these information are then aggregated be GFZ to feed the EIDA
routing service.


## Some additional informations relevant for EIDA routing


Updated on: 2019-06-19


### INGV's authoritative permanent networks

| Code | Description | start | end | no. station |
|---|---|---|---|---|
AC|Albanian Seismic Network|2002-01-01T00:00:00||5
BA|Universita della Basilicata Seismic Network|2005-01-01T00:00:00||1
GU|Regional Seismic Network of North Western Italy|1980-01-01T00:00:00||34
IV|Italian Seismic Network|1988-01-01T00:00:00||559
IX|Irpinia Seismic Network, AMRA s.c.a.r.l., Italy|2005-01-01T00:00:00||31
MN|Mediterranean Very Broadband Seismographic Network|1988-01-01T00:00:00||35
NI|North-East Italy Broadband Network|2002-01-01T00:00:00||14
OT|OTRIONS Local Seismic Network, Apulia, Italy|2013-04-01T00:00:00||13
OX|North-East Italy Seismic Network|2016-01-01T00:00:00||20
RF|Friuli Venezia Giulia Accelerometric Network, Italy|1993-01-01T00:00:00||1
SI|Sudtirol Network, Italy|2006-01-01T00:00:00||7
ST|Trentino Seismic Network, Italy|1981-01-01T00:00:00||8
TV|INGV Experiments Network|2008-01-01T00:00:00||66


### INGV's authoritative temporary networks

| Code | Description | start | end | no. station |
|---|---|---|---|---|
4A|Emersito Seismic Network for Site Effect Studies in L'Aquila town, Central Italy|2009-04-07T00:00:00|2009-12-31T23:59:59|12
3A|Seismic Microzonation Network, 2016 Central Italy|2016-09-19T00:00:00|2016-11-30T23:59:59|50
5J|The Sardinia Passive Array experiment|2014-07-16T00:00:00|2016-09-27T23:59:00|8
XO|EMERSITO Seismic Network, 2016 Central Italy|2016-08-24T00:00:00|2017-11-07T23:59:59|40
YD|Seismic Emergency for Molise-Italy by Sismiko|2018-08-17T00:00:00|2019-08-18T00:00:00|5
ZM|Seismic Emergency for Ischia by Sismiko|2017-08-26T00:00:00|2019-12-31T00:00:00|6


### INGV's defined virtual networks

 * _MOST
 * _MOST-ICO
 * _NFOIRPINA
 * _NFOTABOO


### Shared authoritativeness

These ones require station level entries

| Code | Description | start | end | no. station |
|---|---|---|---|---|
4C|NERA-JRA1 Argostoli basin experiment, Greece|2011-01-01T00:00:00|2014-12-31T23:59:00|16
Z3|AlpArray backbone temporary stations|2015-01-01T00:00:00|2020-07-01T00:00:00|16




.
