import time
import psutil
import os

os.system('mode con: cols=100 lines=7')

class global_vars:
	last_received = psutil.net_io_counters().bytes_recv
	last_sent = psutil.net_io_counters().bytes_sent

def update():
	bytes_received = psutil.net_io_counters().bytes_recv
	bytes_sent = psutil.net_io_counters().bytes_sent

	bytes_recv_r, bytes_sent_r = bytes_received - global_vars.last_received, bytes_sent - global_vars.last_sent
	global_vars.last_received, global_vars.last_sent = bytes_received, bytes_sent
	return bytes_recv_r / 1024 / 1024, bytes_sent_r / 1024/ 1024

print("Download		Upload")

def run():
	while True:
		recv, sent = update()

		if recv < 1:
			recv_unit = 'KB/s'
			recv *= 1024
		else:
			recv_unit = 'MB/s'
		if sent < 1:
			sent_unit = 'KB/s'
			sent *= 1024
		else:
			sent_unit = 'MB/s'

		print(f"\r{recv:.2f} {recv_unit}		{sent:.2f} {sent_unit} 	", end="")
		time.sleep(2)

try:
	run()
except KeyboardInterrupt:
	print("\n* Received Keyboard Interrupt, Exiting...")
