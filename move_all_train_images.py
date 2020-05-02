from os import listdir
from shutil import copyfile

srcpath = "./train_image/"
destpath = "./train_image_all/"

# find all images
root_dir = './train_image/'
for filename in listdir(root_dir):
	# this is the folder name with the timestamp
	img_dir = root_dir + filename
	for image_file in listdir(img_dir):
		# this is the image file name
		# generate the source file location + image name
		src_img_file = root_dir + filename + '/' + image_file
		# generate the dest file location + image name
		dst_img_file = destpath + image_file
		# use the copyfile function from shutil to copy the file from
		# source location to destination location
		copyfile(src_img_file, dst_img_file)