import pickle

with open('config.bin', 'wb') as f:
	data = {'width': 640, 'height': 360}
	pickle.dump(data, f)