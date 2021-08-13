import json
from json import JSONDecodeError
import global_libs.dictionaries as dict

def ParseCiscoASAConfig(configJSON):
	user_exec_config = []
	priv_exec_config = []
	global_config = []
	for key in dict.cisco_asa_keys:
		if key in configJSON:
			if key.lower() == "user_exec":
				user_exec_config = configJSON[key]

			if key.lower() == "priv_exec":
				priv_exec_config = configJSON[key]

			if key.lower() == "global_config":
				global_config = configJSON[key]

		else:
			pass

	return user_exec_config, priv_exec_config, global_config

