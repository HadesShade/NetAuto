from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

def bypass_initial_configuration(prompt,conn):
	if "[yes/no]" in prompt or 'initial configuration' in prompt or 'please answer' in prompt:
		conn.send_command_timing("no\n")
		prompt = conn.find_prompt()
		print ('Bypassing Initial Configuration' + prompt)

def ProcessUserExecCommand(ConfigCommands,conn):
	for command in ConfigCommands:
		print (conn.send_command(command))

def ProcessPrivilegedExecCommand(ConfigCommands,conn):
	print (conn.enable('enable'))
	for command in ConfigCommands:
		print (conn.send_command(command))

def ProcessGlobalCommand(ConfigCommands,conn):
	print (conn.enable('enable'))
	print (conn.config_mode("configure terminal"))
	print (conn.send_config_set(ConfigCommands))

def ProcessCiscoIOSCommands(DeviceIdentity, ConfigLists,count=0):
	try:
		print ("Connecting to "+DeviceIdentity['ip']+":"+DeviceIdentity['port'])
		connection = ConnectHandler(**DeviceIdentity)

		prompt = connection.find_prompt()
		bypass_initial_configuration(prompt, connection)

		GlobalConfig = ConfigLists[2]
		UserExec = ConfigLists[0]
		PrivilegedExec = ConfigLists[1]

		if len(GlobalConfig) != 0:
			ProcessGlobalCommand(GlobalConfig, connection)

		if len(PrivilegedExec) != 0:
			ProcessPrivilegedExecCommand(PrivilegedExec, connection)

		if len(UserExec) != 0:
			ProcessUserExecCommand(UserExec, connection)

	except ( NetmikoAuthenticationException, UnboundLocalError, ValueError, ConnectionRefused) as Errors:
		print ("Error while trying to connect to "+DeviceIdentity['ip']+":"+DeviceIdentity['port'])
		print(Errors)

	except(NetmikoTimeoutException) as Error:
		print(Error)
		count = count +1
		if (count < 3):
			print("Retry....(call) " + count)
			ProccessCiscoIOSCommands(DEviceIdentity,ConfigLists,count)

	connection.disconnect()






