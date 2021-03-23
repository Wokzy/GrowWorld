import pickle


def set_config(width, height):
	with open('config.bin', 'wb') as f:
		data = {'width': width, 'height': height}
		pickle.dump(data, f)
		f.close()