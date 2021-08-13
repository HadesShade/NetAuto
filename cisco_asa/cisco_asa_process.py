from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import global_libs.dictionaries as dict

def bypass_initial_configuration(prompt,conn):
	if "[yes/no]" in prompt or 'initial configuration' in prompt or 'please answer' in prompt:
		conn.send_command_timing("no\n")
		prompt = conn.find_prompt()
		print ('Bypassing Initial Configuration' + prompt)

def bypass_error_reporting(prompt,conn):
	if "[Y]es" in prompt or '[N]o' in prompt or '[A]sk' in prompt or 'anonymous error reporting' in prompt or 'the product' in prompt:
		conn.send_command_timing("A\n")
		prompt = conn.find_prompt()
		print ('Bypassing Error Reporting Configuration' + prompt)

def ProcessUserExecCommand(ConfigCommands,conn):
	for command in ConfigCommands:
		print (conn.send_command(command))

def ProcessPrivilegedExecCommand(ConfigCommands,conn):
	print (conn.enable('enable'))
	for command in ConfigCommands:
		print (conn.send_command(command))

def ProcessGlobalCommand(ConfigCommands,conn):
#	print (conn.enable('enable'))
#	print (conn.config_mode("configure terminal"))
	prompt = conn.find_prompt()
	bypass_error_reporting(prompt, conn)
	print (conn.send_config_set(ConfigCommands))

def ProcessCiscoASAWithSSH(DeviceIdentity, ConfigLists, count=0):
	try:
		if "port" in DeviceIdentity:
			print ("Connecting to "+DeviceIdentity['ip']+":"+DeviceIdentity['port'])

		else:
			if DeviceIdentity['device_type'].lower() == "cisco_asa":
				print ("Connecting to "+DeviceIdentity['ip']+":"+dict.default_remote_ports['ssh'])

			elif DeviceIdentity['device_type'].lower() == "cisco_asa_telnet":
				print ("Connecting to "+DeviceIdentity['ip']+":"+dict.default_remote_ports['telnet'])

			else:
				print ("Error! Remote protocol is not supported or port is not found!")
				exit()

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

	except ( NetmikoAuthenticationException, UnboundLocalError, ValueError, ConnectionRefused, SSHException) as Errors:
		print ("Error while trying to connect to "+DeviceIdentity['ip']+":"+DeviceIdentity['port'])
		print(Errors)

	except(NetmikoTimeoutException) as Error:
		print(Error)
		count = count +1
		if (count < 3):
			print("Retry....(call) " + count)
			ProccessCiscoIOSCommands(DEviceIdentity,ConfigLists,count)

	connection.disconnect()

def ProcessCiscoASACommands(DeviceIdentity, ConfigLists):
	if DeviceIdentity['device_type'].lower() == "cisco_asa":
		ProcessCiscoASAWithSSH(DeviceIdentity, ConfigLists)

	else:
		Print ("Only SSH still supported by this tool for Cisco ASA!")
		exit()






