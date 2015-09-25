from pycountries import *

print ""
print "testing from country name"
germany = Country(name="United States")
print germany

print ""
print "testing geojson"
print str(germany.__geo_interface__)[:200]
import pyagg
canvas = pyagg.Canvas(600,300)
canvas.geographic_space()
canvas.draw_geojson(germany.__geo_interface__)

print ""
print "testing flag image"
img = pyagg.load(germany.flag).resize(60,30)
canvas.paste(img, canvas.coord2pixel(*germany.point))
canvas.view()

print ""
print "testing neighbours and hierarchy"
print germany.neighbours
print germany.region
print germany.continent

print ""
print "testing flexible country name search"
for country in search_countryname("Korea"):
    print country

print ""
print "testing continent"
for continent in all_continents():
    print continent
africa = Continent("Africa")
print africa
for region in africa.regions:
    print "\t%s" %region
for country in africa:
    print "\t\t%s" %country

print ""
print "testing region"
for region in all_regions():
    print region
westafrica = Region("Northern Africa")
print westafrica

import pyagg
canvas = pyagg.Canvas(600,300)
canvas.geographic_space()

for country in westafrica:
    print "\t%s" %country
    canvas.draw_geojson(country.__geo_interface__)
    img = pyagg.load(country.flag).resize(30,15)
    canvas.paste(img, canvas.coord2pixel(*country.point), anchor="center")
canvas.view()

print ""
print "testing region/continent attribute aggregation"
### test aggregate list attributes:
print westafrica.timezones
print westafrica.languages
print westafrica.currencies
print westafrica.webdomains
print westafrica.callcodes
### test aggregate plural name attributes
print westafrica.localnames
print westafrica.capitals
print westafrica.demonyms
print westafrica.points
### test aggregate values attributes
print westafrica.population
print westafrica.area
### test fails
try: print westafrica.translations
except Exception as err: print err
try: print westafrica.othernames
except Exception as err: print err
try: print westafrica.gini
except Exception as err: print err

