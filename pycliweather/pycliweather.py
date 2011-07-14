# flask stuff
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# flask config
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# ---- Config ----

# set our default location
# location can be one of (zipcode|airport code| city name) or anything that Wunderground supports for search.
# if you're calling this script with the location as an arg, it has to be one word, so
default_location = 48104

# The functions could probably be a lot better, but I didn't write them.
# Credit/blame goes to http://nonplatonic.com/ben.php?title=python_xml_to_dict_bow_to_my_recursive_g&more=1&c=1&tb=1&pb=1
# :) thanks!

# ---- Functions ----

def xmltodict(xmlstring):
	doc = xml.dom.minidom.parseString(xmlstring)
	remove_whilespace_nodes(doc.documentElement)
	return elementtodict(doc.documentElement)

def elementtodict(parent):
	child = parent.firstChild
	if (not child):
		return None
	elif (child.nodeType == xml.dom.minidom.Node.TEXT_NODE):
		return child.nodeValue
	
	d={}
	while child is not None:
		if (child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE):
			try:
				d[child.tagName]
			except KeyError:
				d[child.tagName]=[]
			d[child.tagName].append(elementtodict(child))
		child = child.nextSibling
	return d

def remove_whilespace_nodes(node, unlink=True):
	remove_list = []
	for child in node.childNodes:
		if child.nodeType == xml.dom.Node.TEXT_NODE and not child.data.strip():
			remove_list.append(child)
		elif child.hasChildNodes():
			remove_whilespace_nodes(child, unlink)
	for node in remove_list:
		node.parentNode.removeChild(node)
		if unlink:
			node.unlink()

def getFullWeather(someLocation):
    # open our XML feed URL from wunderground.  Our query=default_location is already encoded in default_location.
    feed = urllib2.urlopen('http://api.wunderground.com/auto/wui/geo/ForecastXML/index.xml?query=' + str(someLocation))

    # read the feed into a huge string.  the -1 means we're getting all the bytes, so we don't have to guess / calculate
    feedxml = feed.read(-1)

    # call the xmltodict on our huge XML string
    return xmltodict(feedxml)

@app.route('/')
def showIndex():
    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def getWeather():
    # change our default location to the first arg passed to our script, if one is passed.
    # if not, it'll throw an index or value error, which we catch and proceed to just use the default location.
    try:
        location = request.form['location']
	print location
        location = ' '.join(location)
    # ghetto hack instead of urlencode because urlencode sucks in this case
        location = location.replace(' ', '+')
    except (IndexError, ValueError):
        print "Invalid location passed; using default location:", default_location
        location = default_location
        pass

    fullweather = getFullWeather(location)
    # this gets you up to each day.  After that, have to dig into each to get whatever data you want.
    try:
        weather = fullweather['simpleforecast'][0]['forecastday']
    except (TypeError):
        if len(location) > 0:
            print "Invalid location passed; using default location:", default_location
        location = default_location
        fullweather = getFullWeather(location)
        weather = fullweather['simpleforecast'][0]['forecastday']
        pass


    # range(len(weather)) iterates through each day.  The rest should be self-explanatory.
    # yes, the schema is confusing and stupid.  XML sucks for simple stuff like this; use JSON for your APIs!

    sunrise_hour = fullweather['moon_phase'][0]['sunrise'][0]['hour'][0]
    sunrise_minute = fullweather['moon_phase'][0]['sunrise'][0]['minute'][0]
    sunset_hour = fullweather['moon_phase'][0]['sunset'][0]['hour'][0]
    sunset_minute = fullweather['moon_phase'][0]['sunset'][0]['minute'][0]
    moon = fullweather['moon_phase'][0]['percentIlluminated'][0]

    toret['sunrise'] = sunrise_hour + ':' + sunrise_minute
    toret['sunset'] = sunset_hour + ':' + sunset_minute
    toret['moon'] = moon + '%'
    
    for i in range(len(weather)):
        toret['conditions'] = weather[i]['conditions'][0]
        toret['dayname'] = weather[i]['date'][0]['weekday'][0]
        toret['high'] = weather[i]['high'][0]['fahrenheit'][0]
        toret['low'] = weather[i]['low'][0]['fahrenheit'][0]
        toret['precip'] = weather[i]['pop'][0]
        #print dayname, '-', conditions, '-', low + 'F to', high + 'F -', precip + '% chance of rain'
    return render_template('weather.html', weather=toret)

# ---- Main ----
if __name__ == "__main__":
    import xml.dom.minidom
    import urllib2
    import sys
    app.run()
    getWeather()
