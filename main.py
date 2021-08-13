#!/usr/bin/python3

import json, sys, os
import device_parser as DevPar
from os import path
from art import *
from json import JSONDecodeError


def CheckFile(path):
	if os.path.exists(path):
		return True
	else:
		return False

def ParseJSONFile(file):
	try:
		JSONFile = open(file,'r')
		JSONData = json.load(JSONFile)
		return JSONData

	except JSONDecodeError:
		print ("Error! Check your JSON File!")
		exit()

def main():
	tprint("NetAuto")

	if len(sys.argv) != 2:
		print("Usage : NetAuto <JSON file to read>")
		exit()
	else:
		if CheckFile(sys.argv[1]):
			JSONConfig = ParseJSONFile(sys.argv[1])
			for device in JSONConfig['devices']:
				DevPar.ParseDeviceIdentity(device)

		else:
			print ("Error! Cannot Parse the File given!")


if __name__ == "__main__":
	main()
