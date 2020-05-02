# fit a mask rcnn on the kangaroo dataset
from os import listdir
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from mrcnn.config import Config
from mrcnn.model import MaskRCNN


# class that defines and loads the kangaroo dataset
class KangarooDataset(Dataset):

	# load the dataset definitions
	def load_dataset(self, folder_location, is_train=True):

		# define two class
		self.add_class("dataset", 0, "leaf")  # Change required
		self.add_class("dataset", 1, "collar")  # Change required

		# find all images
		for image_name in listdir(folder_location):
			img_file = folder_location + image_name
			self.add_image('dataset', image_id=image_name, path=img_file)

	def extract_boxes(self, image_name):

		crs = open("./annotate_fixed_window.txt", "r")
		boxes = list()

		for columns in (raw.strip().split(',') for raw in crs):

			img_name, x1, y1, x2, y2, annotation = columns
			if img_name.rsplit('/', 1)[-1] == image_name.rsplit('/', 1)[-1]:
				coors = [int(x1), int(y1), int(x2), int(y2), annotation]
				boxes.append(coors)

		return boxes


	'''
	# extract bounding boxes from an annotation file
	def extract_boxes(self, image_name):

			# load and parse the file
			tree = ElementTree.parse(filename)
			# get the root of the document
			root = tree.getroot()
			# extract each bounding box
			boxes = list()
			for box in root.findall('.//bndbox'):
				xmin = int(box.find('xmin').text)
				ymin = int(box.find('ymin').text)
				xmax = int(box.find('xmax').text)
				ymax = int(box.find('ymax').text)
				coors = [xmin, ymin, xmax, ymax]
				boxes.append(coors)
			# extract image dimensions
			width = int(root.find('.//size/width').text)
			height = int(root.find('.//size/height').text)
			return boxes, width, height
	'''

	# load the masks for an image
	def load_mask(self, image_id):
		# get details of image
		info = self.image_info[image_id]
		# define box file location
		path = info['path']
		boxes = self.extract_boxes(path)
		w = 290
		h = 770
		# create one array for all masks, each on a different channel
		masks = zeros([h, w, len(boxes)], dtype='uint8')
		# create masks
		class_ids = list()
		for i in range(len(boxes)):
			box = boxes[i]
			row_s, row_e = box[1], box[3]
			col_s, col_e = box[0], box[2]
			annotation = box[4]

			if annotation == 'leaf':
				masks[row_s:row_e, col_s:col_e, i] = 0
				class_ids.append(self.class_names.index('leaf'))  # Change required
			elif annotation == 'collar':
				masks[row_s:row_e, col_s:col_e, i] = 1
				class_ids.append(self.class_names.index('collar'))  # Change required
			else: # background
				masks[row_s:row_e, col_s:col_e, i] = 2
				class_ids.append(self.class_names.index('bg'))  # Change required

		return masks, asarray(class_ids, dtype='int32')

	# load an image reference
	def image_reference(self, image_id):
		info = self.image_info[image_id]
		return info['path']

# define a configuration for the model
class KangarooConfig(Config):
	# define the name of the configuration
	NAME = "kangaroo_cfg"
	# number of classes (background + leaf + collar)
	NUM_CLASSES = 1 + 1 + 1
	# number of training steps per epoch
	STEPS_PER_EPOCH = 32

# prepare train set
train_set = KangarooDataset()
train_set.load_dataset('./train_image_all/', is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))
# prepare test/val set
test_set = KangarooDataset()
test_set.load_dataset('./test_images/', is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))

# prepare config
config = KangarooConfig()
config.display()

# define the model
model = MaskRCNN(mode='training', model_dir='./', config=config)

# load weights (mscoco) and exclude the output layers
model.load_weights('./mask_rcnn_coco.h5', by_name=True,
									 exclude=["mrcnn_class_logits", "mrcnn_bbox_fc",  "mrcnn_bbox", "mrcnn_mask"])

# train weights (output layers or 'heads')
model.train(train_set, test_set, learning_rate=0.001, epochs=5, layers='heads') # config.LEARNING_RATE

model.save('./mask_rcnn_model.h5')