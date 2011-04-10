from lxml import etree
from urllib import urlopen

class Weather:
	""" class to get the current weather condition, return a dictionary """

	def __init__(self, partner_id, key, location_id):

		url="http://xoap.weather.com/weather/local/"+location_id+"?cc=*&dayf=1&link=xoap&prod=xoap&par="+partner_id+"&key="+key
		tree = etree.parse(urlopen(url))

		loc = tree.find("loc")
		id = loc.attrib['id']
		location = loc.findtext('dnam')

		kilometers = float(1.609344)
		
		cc = tree.find('cc')

		cc_time = cc.findtext('lsup')

		cc_fahrenheit = cc.findtext('tmp')
		cc_celsius = ((float(cc_fahrenheit)-32)*5)/9
		cc_celsius_rounded = round(cc_celsius,1)
		cc_flik_fahrenheit = cc.findtext('flik')
		cc_flik_celsius = ((float(cc_fahrenheit)-32)*5)/9
		cc_flik_celsius_rounded = round(cc_flik_celsius,1)
		cc_description = cc.findtext('t')

		cc_icon = cc.findtext('icon')
		cc_icon = "weather.com/icons/61x61/"+cc_icon+".png"

		cc_wind = cc.find('wind')
		cc_wind_text = cc_wind.findtext('s')
		if isinstance(cc_wind_text, (int, long, float, complex)):
			cc_wind_strength = float(float(cc_wind_text('s'))*kilometers)
			cc_wind_strength_rounded = round(cc_wind_strength, 1)
		else:
			cc_wind_strength_rounded = cc_wind_text
		cc_wind_direction = cc_wind.findtext('t')

		cc_uv = cc.find('uv')
		cc_uv_index = cc_uv.findtext('i')
		cc_uv_description = cc_uv.findtext('t')

		self.rt = {	'locid': 		id, 
			'location': 		location, 
			'time': 		cc_time, 
			'temp': 		str(cc_celsius_rounded),
			'flik': 		str(cc_flik_celsius_rounded),
			'description': 		cc_description,
			'icon': 		cc_icon,
			'wind': 		cc_wind_strength_rounded,
			'wind_direction': 	cc_wind_direction,
			'uv_index': 		cc_uv_index,
			'uv_description': 	cc_uv_description
		}
