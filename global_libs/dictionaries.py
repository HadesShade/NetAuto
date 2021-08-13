global_device_keys = [
			'model',
			'remote-protocol',
			'ip'
]

additional_device_keys = [
				'port',
				'username',
				'password',
				'secret',
				'verbose'
]

cisco_ios_keys = [
			'user_exec',
			'priv_exec',
			'global_config'
]

cisco_asa_keys = [
			'user_exec',
			'priv_exec',
			'global_config'
]

models = [
		'cisco_ios',
		'cisco_asa',
		'mikrotik'
]

remote_protocols = [
			"telnet",
			"ssh"
]

default_remote_ports = {
	"telnet" : "23",
	"ssh" : "22"
}



