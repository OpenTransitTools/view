APACHE config:
==============

RewriteEngine On
#RewriteLogLevel 3

<Location /got >
    AllowOverride All
</Location>

RedirectMatch ^/qr/(.*) http://dev.trimet.org/ride/stop.html?source=QR_code&stop_id=$1



Redirected URLs:
================

1) QR Codes:    http://trimet.org/qr/00046


2) Stop Info Page from Timetables: http://trimet.org/schedules/w/t1100_1.htm

http://trimet.org/go/cgi-bin/cstops.pl?action=entry&Loc=8368&date=07-13-2014
http://trimet.org/ride/stop.html?action=entry&Loc=8368&date=07-13-2014

3) Other stop pages … see #2 (timetable) above…

a) Stop page from support emails:
http://trimet.org/go/cgi-bin/stop_info.pl?lang=en&y1=-122.575291&Id=902&date=06-29-2014&acode1=OR&locID=1068&x1=45.322748

4) Stop schedule pages



5) Trip planner requests

Board Meetings url: http://dev.trimet.org/got/cgi-bin/plantrip.cgi?to=1800+SW+First+Portland
                    http://dev.trimet.org/got/cgi-bin/plantrip.cgi?to=1800+SW+1st+Ave
                    http://dev.trimet.org/got/cgi-bin/plantrip.cgi?to=9955+NW+St+Helens+Rd+Portland
                    http://dev.trimet.org/got/cgi-bin/plantrip.cgi?to=9955+NE+Glisan+St+Portland

6) Full Trips: 
  http://trimet.org/go/cgi-bin/plantrip.cgi?lang=t&from=3736%20SE%20165TH%20AVE,PO&to=345%20E%20COLUMBIA%20RIVER%20HIGHWAY,TR&after=9:35%20am&on=06/30/14&min=T&walk=0.9999&mode=A&xo=45.495550&yo=-122.493885&xd=&yd=&id=15825&where=345%20E%20COLUMBIA%20RIVER%20HIGHWAY,TR
  http://dev.trimet.org/got/cgi-bin/plantrip.cgi?lang=t&from=3736%20SE%20165TH%20AVE,PO&to=345%20E%20COLUMBIA%20RIVER%20HIGHWAY,TR&after=9:35%20am&on=06/30/14&min=T&walk=0.9999&mode=A&xo=45.495550&yo=-122.493885&xd=&yd=&id=15825&where=345%20E%20COLUMBIA%20RIVER%20HIGHWAY,TR