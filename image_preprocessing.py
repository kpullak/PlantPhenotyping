import os
import cv2

source_path = './test_images/'

def processImage(filename, mImage):

	if '2019' in filename:
		# ----------------------------------
		# Remove noise - by applying guassian blur on src image
		mImage = cv2.GaussianBlur(mImage, (5, 5), cv2.BORDER_DEFAULT)
		# pink rgb values - 255, 153, 255
		# white rgb values - 255, 255, 255
		# ghost white values - 248, 248, 255
		# mImage = mImage[np.where((mImage == [255, 255, 255]).all(axis=2))] = [255, 153, 255]
		# working (best performing, descending) - gtruth 55 - 200 (58), 220 (86), 180 (33), 150 (0)
		mImage[mImage >= 128] = 200
		mImage[mImage < 128] = 0

		'''
		hsvImg = cv2.cvtColor(mImage,cv2.COLOR_BGR2HSV)
		value = 5 # changeable
	
		vValue = hsvImg[..., 2]
		hsvImg[..., 2] = np.where((255-vValue) < value, 255, vValue + value)
		'''

		# save the processed image with a new file name
		new_name = source_path + os.path.splitext(filename)[0] + '_processed.jpg'
		cv2.imwrite(new_name, mImage)
	else:
		pass


for filename in os.listdir(source_path):
	if filename.lower().endswith(('.bmp', '.jpeg', '.jpg', '.png', '.tif', '.tiff')):
		# read the image
		img = cv2.imread(os.path.join(source_path, filename))
		if img is not None:
			processImage(filename, img)


for filename in os.listdir(source_path):
	if filename.lower().endswith(('.bmp', '.jpeg', '.jpg', '.png', '.tif', '.tiff')):
		if '_processed' in filename:
			to_remove = filename.replace('_processed', '')
			to_remove_file = os.path.join(source_path, to_remove)
			os.remove(to_remove_file)

for filename in os.listdir(source_path):
	if filename.lower().endswith(('.bmp', '.jpeg', '.jpg', '.png', '.tif', '.tiff')):
		if '_processed' in filename:
			new_name = filename.replace('_processed', '')
			os.rename(os.path.join(source_path, filename), os.path.join(source_path, new_name))