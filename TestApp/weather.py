#!/usr/bin/env python

from urllib.request import urlopen
import json
#import matplotlib
#import matplotlib.pyplot as plt
import datetime
import dateutil.parser
#import numpy

import pytz

import time

#Gislaved Station
stationCode = 73170
#uppsalaFlygplatsStationCode = 97530
myLat = 57.244515
myLong = 13.651272

_tz = pytz.timezone('Europe/Stockholm')

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.
	
    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def create24hForecastData():
	url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{}/lat/{}/data.json".format(myLong,myLat)

	fcstData = get_jsonparsed_data(url)
	timeStamps = []
	temps = []
	for i in fcstData["timeSeries"]:
		timeStamps.append(int(dateutil.parser.parse(i["validTime"]).timestamp()))
		#timeStamps.append(i["validTime"])
		#timeStamps.append(dateutil.parser.parse(i["validTime"]))
		for j in i["parameters"]:
			if j["name"]=="t":
				temps.append(j["values"][0])

	timeStamps24h = timeStamps[0:44]
	timeStamps24h = [timeStamps24h[i] - timeStamps24h[0] for i in range(44)]
	temps24h = temps[0:44]

	result = [{ "x": timeStamps24h[i], "y": temps24h[i] } for i in range(44)]

	return result

def setUrl(data):
	url = "https://opendata-download-metobs.smhi.se/api/version/{urlData[version]}/parameter/{urlData[parameter]}/station/{urlData[station]}/period/{urlData[period]}/data.json".format(urlData=data)
	return url

def printWithIndex(list):
	for i in range(0, len(list)-1):
		print((i, list))

def printWeatherData(data):
	print(
"""Lufttemperatur: {d[temperature]} \u00b0C
Vindhastighet: {d[wind]} m/s
Barometertryck: {d[pressure]} hPa
Luftfuktighet: {d[humidity]} %
Effektiv temperatur: {d[effectiveTemperature]} \u00b0C 
Mätningar gjorda {d[date]}""".format(d=data))

def getWeatherData(parameter,stationCode=stationCode):
	urlData ={
			"version":"latest",
			"parameter":parameter, 
			"station":stationCode,
			"period":"latest-hour"}
	result = get_jsonparsed_data(setUrl(urlData))
	return result

def effectiveTemperature(temp,wind):
	if wind < 0.5:
		return temp
	else:
		return int(13.126667 + 0.6215*temp - 13.924748*(wind**0.16) + 0.4875195*temp*(wind**0.16))

def getSunTimes():
	url = "https://api.sunrise-sunset.org/json?lat={}&lng={}&formatted=0&ddatetime=today".format(myLat,myLong)
	data = get_jsonparsed_data(url)

	sunriseISO = data['results']['sunrise']
	sunriseUTC = datetime.datetime.fromisoformat(sunriseISO)
	sunrise = datetime_from_utc_to_local(sunriseUTC)

	sunsetISO = data['results']['sunset']
	sunsetUTC = datetime.datetime.fromisoformat(sunsetISO)
	sunset = datetime_from_utc_to_local(sunsetUTC)

	return {
			'sunrise' : sunrise, 
			'sunset' : sunset, 
			'current' : datetime_from_utc_to_local(datetime.datetime.utcnow())
			}

def datetime_from_utc_to_local(utc_datetime):
	return utc_datetime.replace(tzinfo=datetime.timezone.utc).astimezone(tz=_tz)

def getCurrentWeather():
	'''
	this is some real bullshit because dad lives in the sticks far from any actual observations.
	'''
	url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{}/lat/{}/data.json".format(myLong,myLat)
	fcstData = get_jsonparsed_data(url)

	date = dateutil.parser.parse(fcstData['timeSeries'][0]['validTime'])
	date = datetime_from_utc_to_local(date).ctime()

	for i in fcstData['timeSeries'][0]['parameters']:
		if i['name'] == 't':
			temp = i['values'][0]
			break
	

	weatherData = {"temperature":temp,
				   "date":date
				   }

	return weatherData

def plotLatLong():
	urlAllStations = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/4.json"
	dataAllStations = get_jsonparsed_data(urlAllStations)
	points = dataAllStations["station"]

	lat = [i["latitude"] for i in points]
	long = [i["longitude"] for i in points]

	plt.ylabel("latitud")
	plt.xlabel("longitud")

	plt.scatter(long,lat)

	plt.show()

codeData = {
   "0": {
      "description": "Molnens utveckling har icke kunnat observeras eller icke observerats"
   },
   "1": {
      "description": "Moln har upplösts helt eller avtagit i utsträckning, i mäktighet eller i täthet"
   },
   "2": {
      "description": "Molnhimlen i stort sett oförändrad"
   },
   "3": {
      "description": "Moln har bildats eller tilltagit i utsträckning, i mäktighet eller i täthet"
   },
   "4": {
      "description": "Sikten nedsatt av brandrök eller fabriksrök"
   },
   "5": {
      "description": "Torrdis (solrök)"
   },
   "6": {
      "description": "Stoft svävar i luften, men uppvirvlas ej av vinden vid observationsterminen ."
   },
   "7": {
      "description": "Stoft eller sand uppvirvlas av vinden men ingen utpräglad sandvirvel och ingen sandstorm inom synhåll"
   },
   "8": {
      "description": "Utpräglad stoft- eller sandvirvel vid obsterminen eller under senaste timmen meningen sandstorm"
   },
   "9": {
      "description": "Sandstorm under senaste timmen eller inom synhåll vid obs-terminen"
   },
   "10": {
      "description": "Fuktdis med sikt 1-10 km"
   },
   "11": {
      "description": "Låg dimma i bankar på stationen, skiktets mäktighet överstiger ej 2 m på land eller 10 m till sjöss"
   },
   "12": {
      "description": "Mer eller mindre sammanhängande låg dimma på stationen, skiktets mäktighet överstiger ej 2 m på land eller 10 m till sjöss"
   },
   "13": {
      "description": "Kornblixt"
   },
   "14": {
      "description": "Nederbörd inom synhåll, som ej når marken eller havsytan (fallstrimmor)"
   },
   "15": {
      "description": "Nederbörd, som når marken eller havsytaninom synhåll på ett avstånd större än 5 km från stationen"
   },
   "16": {
      "description": "Nederbörd, som når marken eller havsytan inom synhåll på ett avstånd mindre än 5 km, men ej på stationen"
   },
   "17": {
      "description": "Åska vid observationsterminen men ingen nederbörd på stationen"
   },
   "18": {
      "description": "Utpräglade starka vindbyar på stationen eller inom synhåll vid obs-terminen eller under senaste timmen"
   },
   "19": {
      "description": "Skydrag eller tromb på stationen eller inom synhåll vid obs-terminen eller under senaste timmen"
   },
   "20": {
      "description": "Duggregn eller kornsnö under senaste timmen men ej vid observationsterterminen"
   },
   "21": {
      "description": "Regn under senaste timmen men ej vid observationsterterminen"
   },
   "22": {
      "description": "Snöfall under senaste timmen men ej vid observationsterterminen"
   },
   "23": {
      "description": "Snöblandat regn eller iskorn under senaste timmen men ej vid observationsterterminen"
   },
   "24": {
      "description": "Underkylt regn eller duggregn under senaste timmen men ej vid observationsterterminen"
   },
   "25": {
      "description": "Regnskura runder senaste timmen men ej vid observationsterterminen"
   },
   "26": {
      "description": "Byar av snö eller snöblandat regn under senaste timmen men ej vid observationsterterminen"
   },
   "27": {
      "description": "Byar av hagel med eller utan regn under senaste timmen men ej vid observationsterterminen"
   },
   "28": {
      "description": "Dimma under senaste timmen men ej vid observationsterterminen"
   },
   "29": {
      "description": "Åska (med eller utan nederbörd) under senaste timmen men ej vid observationsterterminen"
   },
   "30": {
      "description": "Lätt eller måttlig sandstorm har avtagit istyrka under senaste timmen"
   },
   "31": {
      "description": "Lätt eller måttlig sandstorm utan märkbar förändring under senaste timmen"
   },
   "32": {
      "description": "Lätt eller måttlig sandstorm har börjat eller tilltagit i styrka under senaste timmen"
   },
   "33": {
      "description": "Kraftig sandstorm har avtagit i styrka under senaste timmen"
   },
   "34": {
      "description": "Kraftig sandstorm utan märkbar förändring under senaste timmen"
   },
   "35": {
      "description": "Kraftig sandstorm har börjat eller tilltagit i styrka under senaste timmen"
   },
   "36": {
      "description": "Lågt och lätt eller måttligt snödrev"
   },
   "37": {
      "description": "Lågt men tätt snödrev"
   },
   "38": {
      "description": "Högt men lätt eller måttligt snödrev"
   },
   "39": {
      "description": "Högt och tätt snödrev"
   },
   "40": {
      "description": "Dimma inom synhåll vid observationsterminen, nående över ögonhöjd (dock ej dimma på stationen under senaste timmen) (VV ?10)"
   },
   "41": {
      "description": "Dimma i bankar på stationen (VV< 10)"
   },
   "42": {
      "description": "Dimma, med skymt av himlen, har blivit lättare under senaste timmen"
   },
   "43": {
      "description": "Dimma, utan skymt av himlen, har blivit lättare under senaste timmen"
   },
   "44": {
      "description": "Dimma, med skymt av himlen, oförändrad under senaste timmen"
   },
   "45": {
      "description": "Dimma, utan skymt av himlen, oförändrad under senaste timmen"
   },
   "46": {
      "description": "Dimma, med skymt av himlen, har börjat eller tätnat under senaste timmen"
   },
   "47": {
      "description": "Dimma, utan skymt av himlen, har börjat eller tätnat under senaste timmen"
   },
   "48": {
      "description": "Underkyld dimma, med skymt av himlen"
   },
   "49": {
      "description": "Underkyld dimma, utan skymt av himlen"
   },
   "50": {
      "description": "Lätt duggregn med avbrott"
   },
   "51": {
      "description": "Lätt duggregn, ihållande"
   },
   "52": {
      "description": "Måttligt duggregn med avbrott"
   },
   "53": {
      "description": "Måttligt duggregn, ihållande"
   },
   "54": {
      "description": "Tätt duggregn med avbrott"
   },
   "55": {
      "description": "Tätt duggregn, ihållande"
   },
   "56": {
      "description": "Lätt underkylt duggregn"
   },
   "57": {
      "description": "Måttligt eller tätt underkylt duggregn"
   },
   "58": {
      "description": "Lätt duggregn tillsammans med regn"
   },
   "59": {
      "description": "Måttligt eller tätt duggregn tillsammans med regn"
   },
   "60": {
      "description": "Lätt regn med avbrott"
   },
   "61": {
      "description": "Lätt regn, ihållande"
   },
   "62": {
      "description": "Måttligt regn med avbrott"
   },
   "63": {
      "description": "Måttligt regn, ihållande"
   },
   "64": {
      "description": "Starkt regn med avbrott"
   },
   "65": {
      "description": "Starkt regn ihållande"
   },
   "66": {
      "description": "Lätt underkylt regn"
   },
   "67": {
      "description": "Måttligt eller starkt underkylt regn"
   },
   "68": {
      "description": "Lätt regn eller duggregn tillsammans med snö"
   },
   "69": {
      "description": "Måttligt eller starkt regn eller duggregn tillsammans med snö"
   },
   "70": {
      "description": "Lätt snöfall med avbrott"
   },
   "71": {
      "description": "Lätt snöfall, ihållande"
   },
   "72": {
      "description": "Måttligt snöfall med avbrott"
   },
   "73": {
      "description": "Måttligt snöfall, ihållande"
   },
   "74": {
      "description": "Tätt snöfall med avbrott"
   },
   "75": {
      "description": "Tätt snöfall, ihållande"
   },
   "76": {
      "description": "Isnålar (med el. utan dimma)"
   },
   "77": {
      "description": "Kornsnö (med el. utan dimma)"
   },
   "78": {
      "description": "Enstaka snöstjärnor (med el. utan dimma)"
   },
   "79": {
      "description": "Iskorn"
   },
   "80": {
      "description": "Lätta regnskurar"
   },
   "81": {
      "description": "Måttliga eller kraftiga regnskurar"
   },
   "82": {
      "description": "Mycket kraftiga regnskurar (skyfall)"
   },
   "83": {
      "description": "Lätt snöblandat regn i byar"
   },
   "84": {
      "description": "Måttligt eller kraftigt snöblandat regn i byar"
   },
   "85": {
      "description": "Lätta snöbyar"
   },
   "86": {
      "description": "Måttliga eller kraftiga snöbyar"
   },
   "87": {
      "description": "Lätta byar av småhagel eller snöhagel (trindsnö) med eller utan regn eller snöblandat regn"
   },
   "88": {
      "description": "Måttliga eller kraftiga byar av småhagel eller snöhagel (trindsnö) med eller utan regn eller snöblandat regn"
   },
   "89": {
      "description": "Lätta byar av ishagel med eller utan regn eller snöblandat regn, utan åska"
   },
   "90": {
      "description": "Måttliga eller kraftiga byar av ishagel med eller utan regn eller snöblandat regn, utan åska"
   },
   "91": {
      "description": "Lätt regn vid observationsterminen, åskväder under senaste timmen men ej vid observationsterminen"
   },
   "92": {
      "description": "Måttligt el. starkt regn vid observationsterminen, åskväder under senaste timmen men ej vid observationsterminen"
   },
   "93": {
      "description": "Lätt snöfall, snöblandat regn eller hagel vid observationsterminen, åskväder under senaste timmen men ej vid observationsterminen"
   },
   "94": {
      "description": "Måttligt el. starkt snöfall, snöblandat regn eller hagel vid observationsterminen, åskväder under senaste timmen men ej vid observationsterminen"
   },
   "95": {
      "description": "Svagt eller måttligt åskväder vid observationsterminen utan hagel men med regn eller snö"
   },
   "96": {
      "description": "Svagt eller måttligt åskväder vid observationsterminen med hagel"
   },
   "97": {
      "description": "Kraftigt åskväder vid observationsterminen utan hagel men med regn eller snö"
   },
   "98": {
      "description": "Kraftigt åskväder vid observationsterminen med sandstorm"
   },
   "99": {
      "description": "Kraftigt åskväder vid observationsterminen med hagel"
   },
   "100": {
      "description": "Inget signifikant väder observerat"
   },
   "101": {
      "description": "Moln har upplösts helt eller avtagit i utsträckning, i mäktighet eller i täthet, under senste timmen"
   },
   "102": {
      "description": "Molnhimlen i stort sett oförändrad under senste timmen"
   },
   "103": {
      "description": "Moln har bildats eller tilltagit i utsträckning, i mäktighet eller i täthet, under senste timmen"
   },
   "104": {
      "description": "Dis eller rök, eller stoft som är spritt i luften, sikt större eller lika med 1 km"
   },
   "105": {
      "description": "Dis eller rök, eller stoft som är spritt i luften, sikt mindre än 1 km"
   },
   "110": {
      "description": "Fuktdis med sikt 1-10 km"
   },
   "111": {
      "description": "Isnålar"
   },
   "112": {
      "description": "Blixt på avstånd"
   },
   "118": {
      "description": "Utpräglade starka vindbyar"
   },
   "120": {
      "description": "Dimma"
   },
   "121": {
      "description": "Nederbörd"
   },
   "122": {
      "description": "Duggregn eller kornsnö"
   },
   "123": {
      "description": "Regn"
   },
   "124": {
      "description": "Snöfall"
   },
   "125": {
      "description": "Underkylt duggregn eller regn"
   },
   "126": {
      "description": "Åskväder (med eller utan nederbörd)"
   },
   "127": {
      "description": "Snödrev eller sandstorm"
   },
   "128": {
      "description": "Snödrev eller sandstorm, sikt större eller lika med 1 km"
   },
   "129": {
      "description": "Snödrev eller sandstorm, sikt mindre än 1 km"
   },
   "130": {
      "description": "Dimma"
   },
   "131": {
      "description": "Dimma i bankar på stationen"
   },
   "132": {
      "description": "Dimma, har blivit lättare under senaste timmen"
   },
   "133": {
      "description": "Dimma, oförändrad under senaste timmen"
   },
   "134": {
      "description": "Dimma, har börjat eller tätnat under senaste timmen"
   },
   "135": {
      "description": "Underkyld dimma"
   },
   "140": {
      "description": "Nederbörd"
   },
   "141": {
      "description": "Lätt eller måttlig nederbörd"
   },
   "142": {
      "description": "Kraftig nederbörd"
   },
   "143": {
      "description": "Flytande nederbörd, lätt eller måttlig"
   },
   "144": {
      "description": "Flytande nederbörd, kraftig"
   },
   "145": {
      "description": "Fast nederbörd, lätt eller måttlig"
   },
   "146": {
      "description": "Fast nederbörd, kraftig"
   },
   "147": {
      "description": "Lätt eller måttlig underkyld nederbörd"
   },
   "148": {
      "description": "Kraftig underkyld nederbörd"
   },
   "150": {
      "description": "Duggregn"
   },
   "151": {
      "description": "Lätt duggregn"
   },
   "152": {
      "description": "Måttligt duggregn"
   },
   "153": {
      "description": "Tätt duggregn"
   },
   "154": {
      "description": "Lätt underkylt duggregn"
   },
   "155": {
      "description": "Måttligt underkylt duggregn"
   },
   "156": {
      "description": "Tätt duggregn"
   },
   "157": {
      "description": "Lätt duggregn tillsammans med regn"
   },
   "158": {
      "description": "Måttligt eller tätt duggregn tillsammans med regn"
   },
   "160": {
      "description": "Regn"
   },
   "161": {
      "description": "Lätt regn"
   },
   "162": {
      "description": "Måttligt regn"
   },
   "163": {
      "description": "Starkt regn"
   },
   "164": {
      "description": "Lätt underkylt regn"
   },
   "165": {
      "description": "Måttligt underkylt regn"
   },
   "166": {
      "description": "Starkt underkylt regn"
   },
   "167": {
      "description": "Lätt regn eller duggregn tillsammans med snö"
   },
   "168": {
      "description": "Måttligt eller starkt regn eller duggregn tillsammans med snö"
   },
   "170": {
      "description": "Snöfall"
   },
   "171": {
      "description": "Lätt snöfall"
   },
   "172": {
      "description": "Måttligt snöfall"
   },
   "173": {
      "description": "Tätt snöfall"
   },
   "174": {
      "description": "Lätt småhagel"
   },
   "175": {
      "description": "Måttligt småhagel"
   },
   "176": {
      "description": "Kraftigt småhagel"
   },
   "177": {
      "description": "Kornsnö"
   },
   "178": {
      "description": "Isnålar"
   },
   "180": {
      "description": "Regnskurar"
   },
   "181": {
      "description": "Lätta regnskurar"
   },
   "182": {
      "description": "Måttliga regnskurar"
   },
   "183": {
      "description": "Kraftiga regnskurar"
   },
   "184": {
      "description": "Mycket kraftiga regnskurar (skyfall)"
   },
   "185": {
      "description": "Lätta snöbyar"
   },
   "186": {
      "description": "Måttliga snöbyar"
   },
   "187": {
      "description": "Kraftiga snöbyar"
   },
   "189": {
      "description": "Hagel"
   },
   "190": {
      "description": "Åskväder"
   },
   "191": {
      "description": "Svagt eller måttligt åskväder utan nederbörd"
   },
   "192": {
      "description": "Svagt eller måttligt åskväder med regnskurar eller snöbyar"
   },
   "193": {
      "description": "Svagt eller måttligt åskväder med hagel"
   },
   "194": {
      "description": "Kraftigt åskväder utan nederbörd"
   },
   "195": {
      "description": "Kraftigt åskväder med regnskurar eller snöbyar"
   },
   "196": {
      "description": "Kraftigt åskväder med hagel"
   },
   "199": {
      "description": "Tromb eller Tornado"
   },
   "204": {
      "description": "Vulkanaska som spridits högt upp i luften"
   },
   "206": {
      "description": "Tjockt stoftdis, sikt mindre än 1 km"
   },
   "207": {
      "description": "Vattenstänk vid station pga blåst"
   },
   "208": {
      "description": "Drivande stoft (eller sand)"
   },
   "209": {
      "description": "Kraftig stoft- eller sandstorm på avstånd (Haboob)"
   },
   "210": {
      "description": "Snödis"
   },
   "211": {
      "description": "Snöstorm eller kraftigt snödrev som ger extremt dålig sikt"
   },
   "213": {
      "description": "Blixt mellan moln och marken"
   },
   "217": {
      "description": "Åska utan regnskur"
   },
   "219": {
      "description": "Tromb eller tornado (förödande) vid stationen eller inom synhåll under den senaste timmen"
   },
   "220": {
      "description": "Avlagring av vulkanaska"
   },
   "221": {
      "description": "Avlagring av stoft eller sand"
   },
   "222": {
      "description": "Dagg"
   },
   "223": {
      "description": "Utfällning av blöt snö"
   },
   "224": {
      "description": "Lätt eller måttlig dimfrost"
   },
   "225": {
      "description": "Kraftig dimfrost"
   },
   "226": {
      "description": "Rimfrost"
   },
   "227": {
      "description": "Kraftig isbeläggning pga underkyld nederbörd"
   },
   "228": {
      "description": "Isskorpa"
   },
   "230": {
      "description": "Stoft- eller sandstorm med temperatur under fryspunkten"
   },
   "239": {
      "description": "Kraftigt snödrev och/eller snöfall"
   },
   "241": {
      "description": "Dimma till havs"
   },
   "242": {
      "description": "Dimma i dalgång"
   },
   "243": {
      "description": "Sjörök i Arktis eller vid Antarktis"
   },
   "244": {
      "description": "Advektionsdimma (över vatten)"
   },
   "245": {
      "description": "Advektionsdimma (över land)"
   },
   "246": {
      "description": "Dimma över is eller snö"
   },
   "247": {
      "description": "Tät dimma, sikt 60-90 m"
   },
   "248": {
      "description": "Tät dimma, sikt 30-60 m"
   },
   "249": {
      "description": "Tät dimma, sikt mindre än 30 m"
   },
   "250": {
      "description": "Duggregn, intensitet mindre än 0,10 mm/timme"
   },
   "251": {
      "description": "Duggregn, intensitet 0,10-0,19 mm/timme"
   },
   "252": {
      "description": "Duggregn, intensitet 0,20-0,39 mm/timme"
   },
   "253": {
      "description": "Duggregn, intensitet 0,40-0,79 mm/timme"
   },
   "254": {
      "description": "Duggregn, intensitet 0,80-1,59 mm/timme"
   },
   "255": {
      "description": "Duggregn, intensitet 1,60-3,19 mm/timme"
   },
   "256": {
      "description": "Duggregn, intensitet 3,20-6,39 mm/timme"
   },
   "257": {
      "description": "Duggregn, intensitet större än 6,40 mm/timme"
   },
   "259": {
      "description": "Duggregn och snöfall"
   },
   "260": {
      "description": "Regn, intensitet mindre än 1,0 mm/timme"
   },
   "261": {
      "description": "Regn, intensitet 1,0-1,9 mm/timme"
   },
   "262": {
      "description": "Regn, intensitet 2,0-3,9 mm/timme"
   },
   "263": {
      "description": "Regn, intensitet 4,0-7,9 mm/timme"
   },
   "264": {
      "description": "Regn, intensitet 8,0-15,9 mm/timme"
   },
   "265": {
      "description": "Regn, intensitet 16,0-31,9 mm/timme"
   },
   "266": {
      "description": "Regn, intensitet 32,0-63,9 mm/timme"
   },
   "267": {
      "description": "Regn, intensitet större än 64,0 mm/timme"
   },
   "270": {
      "description": "Snö, intensitet mindre än 1,0 cm/timme"
   },
   "271": {
      "description": "Snö, intensitet 1,0-1,9 cm/timme"
   },
   "272": {
      "description": "Snö, intensitet 2,0-3,9 cm/timme"
   },
   "273": {
      "description": "Snö, intensitet 4,0-7,9 cm/timme"
   },
   "274": {
      "description": "Snö, intensitet 8,0-15,9 cm/timme"
   },
   "275": {
      "description": "Snö, intensitet 16,0-31,9 cm/timme"
   },
   "276": {
      "description": "Snö, intensitet 32,0-63,9 cm/timme"
   },
   "277": {
      "description": "Snö, intensitet större än 64,0 cm/timme"
   },
   "278": {
      "description": "Snöfall eller isnålar från en klar himmel"
   },
   "279": {
      "description": "Frysande blötsnö"
   },
   "280": {
      "description": "Regn"
   },
   "281": {
      "description": "Underkylt regn"
   },
   "282": {
      "description": "Snöblandat regn"
   },
   "283": {
      "description": "Snöfall"
   },
   "284": {
      "description": "Småhagel eller snöhagel"
   },
   "285": {
      "description": "Småhagel eller snöhagel tillsammans med regn"
   },
   "286": {
      "description": "Småhagel eller snöhagel tillsammans med snöblandat regn"
   },
   "287": {
      "description": "Småhagel eller snöhagel tillsammans med snö"
   },
   "288": {
      "description": "Hagel"
   },
   "289": {
      "description": "Hagel tillsammans med regn"
   },
   "290": {
      "description": "Hagel tillsammans med snöblandat regn"
   },
   "291": {
      "description": "Hagel tillsammans med snö"
   },
   "292": {
      "description": "Skurar eller åska till havs"
   },
   "293": {
      "description": "Skurar eller åska över berg"
   },
   "508": {
      "description": "Inga signifikanta fenomen att rapportera, rådande och gammalt väder utelämnas"
   },
   "509": {
      "description": "Ingen observation, data ej tillgängligt, rådande och gammalt väder utelämnas"
   },
   "510": {
      "description": "Rådande och gammalt väder saknas men förväntades."
   },
   "511": {
      "description": "Saknat värde"
   }
}