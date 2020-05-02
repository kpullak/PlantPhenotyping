im_name = 'pic_2020-03-02T20_00_16_313Z_000676.jpg'
predBoxes = [('collar', 84.40327048301697, 2299, 1445, 2562, 2365),
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

# things to measure, the regressor accuracy
# IoU is the metric we will be using to find the area of intersection


def getGroundTruthBoxes(image_name):

	crs = open("./annotate_fixed_window.txt", "r")
	gTruthBoxes = list()

	for columns in (raw.strip().split(',') for raw in crs):

		img_name, x1, y1, x2, y2, annotation = columns
		if img_name.rsplit('/', 1)[-1] == image_name.rsplit('/', 1)[-1]:
			coors = [int(x1), int(y1), int(x2), int(y2), annotation]
			gTruthBoxes.append(coors)
	return gTruthBoxes


def make_uniform(x1, y1, x2, y2):

	# the goal of this function is to convert the box coordinates to uniform alignment of principal diagonal
	if x1 < x2 and y1 < y2:
		# image 1
		return x1, y1, x2, y2
	elif x1 < x2 and y1 > y2:
		# image 2
		return x1, y2, x2, y1
	elif x1 > x2 and y1 > y2:
		# image 3
		return x2, y2, x1, y1
	elif x1 > x2 and y1 < y2:
		# image 4
		return x2, y1, x1, y2
	else:
		return None


gBoxes = getGroundTruthBoxes(im_name)
iou_counter = 0
min_iou_threshold = 0.445
iou_dictionary = {} # key is combination of all pred_boxes and value is the iou
theta_dictionary = {} # key is combination of all pred_boxes and value is the theta of angle of intersection
dice_dictionary = {} # key is combination of all pred_boxes and value is the dice coefficient

for predBox in predBoxes:
	for gBox in gBoxes:
		predAnnotation, predProb, pred_x1, pred_y1, pred_x2, pred_y2 = predBox
		g_x1, g_y1, g_x2, g_y2, gAnnotation = gBox
		pred_x1, pred_y1, pred_x2, pred_y2 = make_uniform(pred_x1, pred_y1, pred_x2, pred_y2)
		g_x1, g_y1, g_x2, g_y2 = make_uniform(g_x1, g_y1, g_x2, g_y2)

		if predAnnotation == gAnnotation:
			x_left = max(pred_x1, g_x1)
			x_right = min(pred_x2, g_x2)
			y_bottom = max(pred_y1, g_y1)
			y_top = min(pred_y2, g_y2)
		else:
			continue

		if x_right < x_left and y_bottom < y_top:
			# print('continue - ', x_left, x_right, y_bottom, y_top)
			continue

		# The intersection of two axis-aligned bounding boxes is always an
		# axis-aligned bounding box
		# print(x_left, x_right, y_bottom, y_top)
		intersection_area = (x_right - x_left) * (y_top - y_bottom)
		# print('Intersection area - ', intersection_area)

		# compute the area of both AABBs
		bb1_area = (pred_x2 - pred_x1) * (pred_y2 - pred_y1)
		bb2_area = (g_x2 - g_x1) * (g_y2 - g_y1)

		# compute the intersection over union by taking the intersection
		# area and dividing it by the sum of prediction + ground-truth
		# areas - the interesection area
		union_area = float(bb1_area + bb2_area - intersection_area)
		# print('Union area - ',union_area)
		iou = intersection_area / union_area

		# dice coefficient
		dice_coeff = 2 * intersection_area / (bb1_area + bb2_area)
		# slope related computations
		pred_slope = (pred_y2 - pred_y1) / (pred_x2 - pred_x1)
		g_slope = (g_y2 - g_y1) / (g_x2 - g_x1)

		tanget_of_intersection = 0.
		numerator = g_slope - pred_slope
		denominator = 1 + g_slope * pred_slope
		tanget_of_intersection = numerator / denominator

		if iou < min_iou_threshold or iou > 1.0:
			pass

		print('IoU is - ', iou)
		key = str(pred_x1) + ", " + str(pred_y1) + ", " + str(pred_x2) + ", " + str(pred_y2)

		if key not in iou_dictionary:
			iou_dictionary[key] = iou
			# theta_dictionary[key] = [tanget_of_intersection, math.degrees(math.atan(tanget_of_intersection))]
			theta_dictionary[key] = tanget_of_intersection
			dice_dictionary[key] = dice_coeff
			iou_counter += 1
		else:
			if iou_dictionary[key] > iou:
				pass
			else:
				iou_dictionary[key] = iou
				# theta_dictionary[key] = [tanget_of_intersection, math.degrees(math.atan(tanget_of_intersection))]
				theta_dictionary[key] = tanget_of_intersection
				dice_dictionary[key] = dice_coeff

print(iou_counter)
print(iou_dictionary)
print(theta_dictionary)
print(dice_dictionary)