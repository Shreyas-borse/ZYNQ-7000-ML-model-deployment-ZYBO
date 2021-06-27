from flower_preprocessing import *

def eval_input(iter, eval_image_dir, eval_image_list, class_num, eval_batch_size):
  images = []
  labels = []
  line = open(eval_image_list).readlines()
  for index in range(0, eval_batch_size):
    curline = line[iter * eval_batch_size + index]
    [image_name, label_id] = curline.split(' ')
    image = cv2.imread(eval_image_dir + image_name)
    image = central_crop(image, 64, 64)
    image = mean_image_subtraction(image, MEANS)
    images.append(image)
    labels.append(int(label_id))
  lb = preprocessing.LabelBinarizer()
  lb.fit(range(0, class_num))
  labels = lb.transform(labels)
  return {"input": images, "labels": labels}

calib_image_dir = "./calibration_data/calibration/"
calib_image_list = "./calibration_data/calibration.txt"
calib_batch_size = 50

def calib_input(iter):
  images = []
  line = open(calib_image_list).readlines()
  for index in range(0, calib_batch_size):
    curline = line[iter * calib_batch_size + index]
    [image_name, label_id] = curline.split(' ')
    image = cv2.imread(calib_image_dir + image_name)
    image = central_crop(image, 64, 64)
    image = mean_image_subtraction(image, MEANS)
    images.append(image)
  return {"conv2d_input": images}

