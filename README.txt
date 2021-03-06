The problem: I want to look up the weather from wunderground from my terminal without opening up a web browser. I figured "hey, this should be easy / fun to do using Python!" -- WRONG! XML is always a pain to work with, and there is no *easy* way to get XML schema into a dict. Most people don't even use XML correctly; you should use JSON if you just have strings inside of XML tags and nothing more. Every API I've ever seen / worked with uses XML in this way, and so they could all replace it with the *much* easier to parse JSON.

Update: You can now pass in the location as the first argument to the script. 

Update 2: You can use *any* location search format that wunderground supports; this includes zipcode, airport code, city name and state, etc.
If Wunderground returns valid XML for your query, pycliweather will parse it; the searches are limited only by the Wunderground API.

In the example below, I'm using 'dallas texas'. There is also a default specified in the code should a location not be passed.

Anyway, here is what should come out when you run this:

likwid@helios pycliweather(master)$ weather dallas texas
Location: dallas+texas
Sunrise: 6:18
Sunset: 20:37
Moon visible: 95% 

Friday - Partly Cloudy - 79F to 99F - 0% chance of rain
Saturday - Partly Cloudy - 79F to 104F - 10% chance of rain
Sunday - Partly Cloudy - 79F to 101F - 10% chance of rain
Monday - Partly Cloudy - 77F to 99F - 10% chance of rain
Tuesday - Chance of a Thunderstorm - 77F to 95F - 20% chance of rain
Wednesday - Chance of a Thunderstorm - 76F to 92F - 30% chance of rain



