pred_dictionary = {}
gtruth_dictionary = {}


def makePredictionBoxesDictionary():

	# open the predictions object file and read into a dictionary
	crs = open("./test_dets.txt", "r")

	for columns in (raw.strip().split(',') for raw in crs):
		img_name, x1, y1, x2, y2, annotation, prob = columns
		bbox = (annotation, int(x1), int(y1), int(x2), int(y2))
		if img_name not in pred_dictionary:
			pred_dictionary[img_name] = []
			pred_dictionary[img_name].append(bbox)
		else:
			pred_dictionary[img_name].append(bbox)

	return pred_dictionary


def makeGroundTruthBoxesDictionary():

	# open the ground truth object file and read into a dictionary
	crs = open("./annotate_fixed_window.txt", "r")

	for columns in (raw.strip().split(',') for raw in crs):
		img_name, x1, y1, x2, y2, annotation = columns
		img_name = img_name.rsplit('/', 1)[-1]
		bbox = (annotation, int(x1), int(y1), int(x2), int(y2))
		if img_name not in gtruth_dictionary:
			gtruth_dictionary[img_name] = []
			gtruth_dictionary[img_name].append(bbox)
		else:
			gtruth_dictionary[img_name].append(bbox)

	return gtruth_dictionary

# initializing the dictionaries
groundBoxes = makeGroundTruthBoxesDictionary()
predBoxes = makePredictionBoxesDictionary()

pred_leaf_counter = 0
pred_collar_counter = 0
gtruth_leaf_counter = 0
gtruth_collar_counter = 0

for image, predBoxes in pred_dictionary.items():
	for predBox in predBoxes:
		if predBox[0] == 'leaf':
			pred_leaf_counter += 1
		elif predBox[0] == 'collar':
			pred_collar_counter += 1

	for key, gBoxes in gtruth_dictionary.items():
		if image not in key:
			pass
		else:
			for gBox in gBoxes:
				if gBox[0] == 'leaf':
					gtruth_leaf_counter += 1
				elif gBox[0] == 'collar':
					gtruth_collar_counter += 1


if gtruth_leaf_counter != 0 and gtruth_collar_counter != 0:
	print(pred_leaf_counter/gtruth_leaf_counter)
	print(gtruth_leaf_counter/gtruth_collar_counter)