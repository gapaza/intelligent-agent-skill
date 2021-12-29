from api import NXTClient




















def main():
	print('--> RUNNING TESTS')
	client = NXTClient()
	client.turn_motor(degrees=180)
	# client.rotate_radar(duration=2)
	# client.move_clockwise(counter_clockwise=True)
	
	
	
	
	# print(client.get_distance())
	
	
	
	# print('--> CHARGE:', client.get_charge())
	# client.run_motor()
	
	
	
	




if __name__ == "__main__":
	main()


