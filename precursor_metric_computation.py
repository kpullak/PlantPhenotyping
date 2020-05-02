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


# takes input in any of the four forms - inclining downward, sloping upward, right to left, left to right
# and returns the values in the standard format - incliding upward and left to right (principal diagonal)
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
		return x1, y1, x2, y2


groundBoxes = makeGroundTruthBoxesDictionary()
predBoxes = makePredictionBoxesDictionary()

iou_counter = 0
min_iou_threshold = 0.445 # trial and error approach

leaf_iou_dictionary = {} # key is combination of all pred_boxes and value is the leaf_iou
collar_iou_dictionary = {} # key is combination of all pred_boxes and value is the collar_iou

leaf_theta_dictionary = {} # key is combination of all pred_boxes and value is theta of angle of intersection of leaves
collar_theta_dictionary = {} # key is combination of all pred_boxes and value is theta of angle of inter of collars

leaf_dice_dictionary = {} # key is combination of all pred_boxes and value is the leaf dice coefficient
collar_dice_dictionary = {} # key is combination of all pred_boxes and value is the collar dice coefficient

for img_name, predBox in predBoxes.items():
	groundBox = groundBoxes[img_name]
	for pBox in predBox:
		for gBox in groundBox:
			predAnnotation, pred_x1, pred_y1, pred_x2, pred_y2 = pBox
			gAnnotation, g_x1, g_y1, g_x2, g_y2 = gBox
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
			if (pred_x2 == pred_x1) or (g_x2 == g_x1):
				continue
			pred_slope = (pred_y2 - pred_y1) / (pred_x2 - pred_x1)
			g_slope = (g_y2 - g_y1) / (g_x2 - g_x1)

			tanget_of_intersection = 0.
			numerator = g_slope - pred_slope
			denominator = 1 + g_slope * pred_slope
			tanget_of_intersection = numerator / denominator

			if iou < min_iou_threshold or iou > 1.0:
				continue

			# print('IoU is - ', iou)
			key = str(pred_x1) + ", " + str(pred_y1) + ", " + str(pred_x2) + ", " + str(pred_y2)

			if predAnnotation == 'leaf':
				if key not in leaf_iou_dictionary:
					leaf_iou_dictionary[key] = iou
					# theta_dictionary[key] = [tanget_of_intersection, math.degrees(math.atan(tanget_of_intersection))]
					leaf_theta_dictionary[key] = tanget_of_intersection
					leaf_dice_dictionary[key] = dice_coeff
					iou_counter += 1
				else:
					if leaf_iou_dictionary[key] > iou:
						pass
					else:
						leaf_iou_dictionary[key] = iou
						# theta_dictionary[key] = [tanget_of_intersection, math.degrees(math.atan(tanget_of_intersection))]
						leaf_theta_dictionary[key] = tanget_of_intersection
						leaf_dice_dictionary[key] = dice_coeff
			elif predAnnotation == 'collar':
				if key not in collar_iou_dictionary:
					collar_iou_dictionary[key] = iou
					# theta_dictionary[key] = [tanget_of_intersection, math.degrees(math.atan(tanget_of_intersection))]
					collar_theta_dictionary[key] = tanget_of_intersection
					collar_dice_dictionary[key] = dice_coeff
					iou_counter += 1
				else:
					if collar_iou_dictionary[key] > iou:
						pass
					else:
						collar_iou_dictionary[key] = iou
						# theta_dictionary[key] = [tanget_of_intersection, math.degrees(math.atan(tanget_of_intersection))]
						collar_theta_dictionary[key] = tanget_of_intersection
						collar_dice_dictionary[key] = dice_coeff


leaf_iou_summer = 0
for key, val in leaf_iou_dictionary.items():
	leaf_iou_summer += val
if len(leaf_iou_dictionary) != 0:
	avg_leaf_iou = leaf_iou_summer/len(leaf_iou_dictionary)
else:
	avg_leaf_iou = 0


collar_iou_summer = 0
for key, val in collar_iou_dictionary.items():
	collar_iou_summer += val
if len(collar_iou_dictionary) != 0:
	avg_collar_iou = collar_iou_summer/len(collar_iou_dictionary)
else:
	avg_collar_iou = 0


leaf_theta_summer = 0
for key, val in leaf_theta_dictionary.items():
	leaf_theta_summer += val
if len(leaf_theta_dictionary) != 0:
	avg_leaf_theta = leaf_theta_summer / len(leaf_theta_dictionary)
else:
	avg_leaf_theta = 0


collar_theta_summer = 0
for key, val in collar_theta_dictionary.items():
	collar_theta_summer += val
if len(collar_theta_dictionary) != 0:
	avg_collar_theta = collar_theta_summer/len(collar_theta_dictionary)
else:
	avg_collar_theta = 0


leaf_dice_summer = 0
for key, val in leaf_dice_dictionary.items():
	leaf_dice_summer += val
if len(leaf_dice_dictionary) != 0:
	avg_leaf_dice = leaf_dice_summer/len(leaf_dice_dictionary)
else:
	avg_leaf_dice = 0


collar_dice_summer = 0
for key, val in collar_dice_dictionary.items():
	collar_dice_summer += val
if len(collar_dice_dictionary) != 0:
	avg_collar_dice = collar_dice_summer/len(collar_dice_dictionary)
else:
	avg_collar_dice = 0

print('Leaf, Collar')
print(avg_leaf_iou, avg_collar_iou)
print(avg_leaf_theta, avg_collar_theta)
print(avg_leaf_dice, avg_collar_dice)

from tabulate import tabulate
print(tabulate([['IoU', avg_leaf_iou, avg_collar_iou], ['Theta', avg_leaf_theta, avg_collar_theta],
								['Dice', avg_leaf_dice, avg_collar_dice]], headers=['Metric', 'Leaf', 'Collar']))