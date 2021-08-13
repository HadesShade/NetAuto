import json
from json import JSONDecodeError
import dictionaries as dict
import cisco_ios_config_parser as IOSParser
import cisco_ios_process as IOSProcess

def ParseDeviceIdentity(deviceJSON):
	deviceIdentity = {}
	for key in dict.global_device_keys:
		if key not in deviceJSON:
			print ("Error! Please check device(s) identity in your JSON file!")
			exit()

	if deviceJSON['model'].lower() not in dict.models:
		print("Error! Device model is not supported!")
		exit()

	elif deviceJSON['remote-protocol'].lower() not in dict.remote_protocols:
		print("Error! Remote protocol is not supported!")
		exit()

	else:
		if deviceJSON['model'].lower() == "cisco_ios":
			deviceIdentity['device_type'] = (deviceJSON['model'].lower()+"_"+deviceJSON['remote-protocol']) if deviceJSON['remote-protocol'].lower() == "telnet" else deviceJSON['model'].lower()
			deviceIdentity['ip'] = deviceJSON['ip']
			AddOptionalDeviceIdentity(deviceJSON, deviceIdentity)
			IOSProcess.ProcessCiscoIOSCommands(deviceIdentity, IOSParser.ParseCiscoIOSConfig(deviceJSON))

		elif deviceJSON['model'].lower() == "mikrotik":
			#There will device identity generated for mikrotik device
			print ("Mikrotik not supported yet!")
			exit()

		else:
			print("Error! Device model is not supported!")
			exit()


def AddOptionalDeviceIdentity(deviceJSON, deviceIdentity):
	for key in dict.optional_device_keys:
		if key in deviceJSON:
			deviceIdentity[key] = deviceJSON[key]

		else:
			pass
