image_name = 'pic_2020-03-02T20_00_16_313Z_000676.jpg'
all_dets = [('collar', 84.40327048301697, 2299, 1445, 2562, 2365),
						('collar', 82.07628130912781, 2365, 1379, 2628, 2168),
						('collar', 79.67304587364197, 657, 657, 919, 1445),
						('collar', 78.75728607177734, 722, 1314, 985, 2102),
						('collar', 78.14204692840576, 788, 1445, 1051, 2234),
						('collar', 76.63304805755615, 591, 65, 854, 854),
						('collar', 76.60690546035767, 2431, 1642, 2628, 2365),
						('collar', 76.36932730674744, 657, 1445, 919, 2234),
						('collar', 75.38456916809082, 2431, 985, 2693, 1774),
						('collar', 73.89962673187256, 2496, 459, 2759, 1248),
						('collar', 71.7272937297821, 591, 525, 854, 1314),
						('leaf', 71.7272937297821, 591, 525, 854, 1314)]


# things to measure, the classifier accuracy and regressor accuracy
# for classifier accuracy, we can measure the number of leafs/collars in the prediction divided by
# the number of leaf/collars in the ground truth object

def getGroundTruthCounter(image_name):

	gtruth_leaf_counter = 0
	gtruth_collar_counter = 0

	crs = open("./annotate_fixed_window.txt", "r")

	for columns in (raw.strip().split(',') for raw in crs):

		img_name, x1, y1, x2, y2, annotation = columns
		if img_name.rsplit('/', 1)[-1] == image_name.rsplit('/', 1)[-1]:
			if annotation == 'leaf':
				gtruth_leaf_counter += 1
			elif annotation == 'collar':
				gtruth_collar_counter += 1

	return gtruth_leaf_counter, gtruth_collar_counter


def getGroundTruthBoxer(image_name):

	crs = open("./annotate_fixed_window.txt", "r")
	gTruthBoxes = list()

	for columns in (raw.strip().split(',') for raw in crs):

		img_name, x1, y1, x2, y2, annotation = columns
		if img_name.rsplit('/', 1)[-1] == image_name.rsplit('/', 1)[-1]:
			coors = [int(x1), int(y1), int(x2), int(y2), annotation]
			gTruthBoxes.append(coors)
	return gTruthBoxes

# this is for one image
leaf_counter = 0
collar_counter = 0
for det in all_dets:
	annotation, prob, x1, y1, x2, y2 = det
	if annotation == 'leaf':
		leaf_counter += 1
	elif annotation == 'collar':
		collar_counter += 1
gtruth_leaf_counter, gtruth_collar_counter = getGroundTruthCounter(image_name)

leaf_accuracy = leaf_counter / gtruth_leaf_counter
collar_accuracy = collar_counter / gtruth_collar_counter

print(image_name)
print('predictions')
print(leaf_counter, collar_counter)
print('ground truth')
print(gtruth_leaf_counter, gtruth_collar_counter)
print('accuracies')
print(leaf_accuracy, collar_accuracy)