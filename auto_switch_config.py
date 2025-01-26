from netmiko import ConnectHandler
import threading

switches = [
    {
        'connection': {'device_type': 'cisco_ios_telnet', 'host': '', 'username': '', 'password': '', 'secret': '', 'port': 32769, 'timeout': 60}, # change values as needed
        "hostname": 'Switch01',
        "domain-name": 'SWITCH01.LOCAL',
        "vlanip": '192.168.1.1'
    },
    {
        'connection': {'device_type': 'cisco_ios_telnet', 'host': '', 'username': '', 'password': '', 'secret': '', 'port': 32770, 'timeout': 60}, # change values as needed
        "hostname": 'Switch02',
        "domain-name": 'SWITCH02.LOCAL',
        "vlanip": '192.168.2.1'
    }
]

def connect(switch, config):
	connection = ConnectHandler(**switch)
	connection.enable()
	sendconfig = connection.send_config_set(config)
	connection.disconnect()

def config(switch):
	main_config = [
		'config t',
		f'hostname {switch["hostname"]}'
		f'ip domain-name {switch["domain-name"]}',
		'crypto key generate rsa modulus 2048',
		'ip ssh version 2',
		'lin vty 0 4',
		'transport input ssh',
		'login local',
		'exit',
		'username admin password cisco99',
		'config t',
		'no ip domain-lookup',
		'logging console warnings',
		'enable secret cisco12',
		'service password-encryption',
		'banner motd $ Authorized Access Only $',
		'lin con 0',
		'password cisco12',
		'login',
		'exit',
		'vlan 10',
		'int vlan 10',
		f'ip address {switch["vlanip"]} 255.255.255.0',
		'no shut',
		'int gi0/1',
		'switchport mode access',
		'switchport access vlan 10',
		'no shut',
		'int gi0/0',
		'switchport mode trunk',
		'switchport trunk allowed vlan 10',
		'no shut',
		'exit',
		'do copy running-config startup-config'
	]
	
	connect(switch['connection'], main_config)
	print(f'Completed {switch["hostname"]}')

threads = []

for switch in switches:
	thread = threading.Thread(target=config, args=(switch,))
	threads.append(thread)
	thread.start()

for thread in threads:
	thread.join()
	
	


