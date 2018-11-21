__author__ = 'zhengwang'

import threading
import SocketServer
#import serial
import cv2
import numpy as np
import math
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import time
import mysql.connector

from utils import label_map_util
from utils import visualization_utils as vis_util

mydb = mysql.connector.connect(
  host="localhost",
  user="phpmyadmin",
  passwd="jithesh@55",
  database="mp"
)


# What model to download.

MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90
# ## Download Model

"""
#initial use only
 
opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
  file_name = os.path.basename(file.name)
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())



"""

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine




label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

### DATABASE MANAGEMENT

def insertdb(count,id1):
	mycursor = mydb.cursor()
	ts="55"
	sql = "INSERT INTO counter (id, cnt) VALUES (%s, %s)"
	val = (id1, count)
	mycursor.execute(sql, val)
	mydb.commit()
	

def deletedb(id1):
	mycursor = mydb.cursor()
	sql = "DELETE FROM counter WHERE id = %s"
	val = (id1, )
	mycursor.execute(sql, val)
	mydb.commit()
	




c1=0

# Create a connection object

mydb = mysql.connector.connect(
  host="localhost",
  user="phpmyadmin",
  passwd="jithesh@55",
  database="mp"
)



#socket +tensor flow code



class VideoStreamHandler(SocketServer.StreamRequestHandler):
    print("hi1")

    def handle(self):
	print("hi2")
	l=1
	c1=0
	stream_bytes = ' '
        # stream video frames one by one
        try:
            while True:
            	
            	#print("hi3")
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    l=l+1
            	    temp=str(l)+'.jpg'
                    print("hi4")
                    jpg = stream_bytes[first:last+2]#this is the image
		    stream_bytes = stream_bytes[last+2:]
		    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),1) #color image
		    gray= cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),0) #grayscale
		    #cv2.imwrite(temp,img)
		    #cv2.imshow('image', ims)
		    #your code goes here tensorflow
		    with detection_graph.as_default():
  			with tf.Session(graph=detection_graph) as sess:
  				image_np=img
				# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      				image_np_expanded = np.expand_dims(image_np, axis=0)
     				image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      				# Each box represents a part of the image where a particular object was detected.
      				boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      				# Each score represent how level of confidence for each of the objects.
      				# Score is shown on the result image, together with the class label.
      				scores = detection_graph.get_tensor_by_name('detection_scores:0')
      				classes = detection_graph.get_tensor_by_name('detection_classes:0')
      				num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      				# Actual detection.
      				(boxes, scores, classes, num_detections) = sess.run(
          				[boxes, scores, classes, num_detections],
          				feed_dict={image_tensor: image_np_expanded})
      				# Visualization of the results of a detection.
      				#count
      				final_score=np.squeeze(scores)
      				finalclass= np.squeeze(classes).astype(np.int32)
      				#print finalclass
      				countp=0
      				counts=0
      
     				# print finalclass[0]
      				for i in range (100):
              				if ((scores is None or final_score[i]>0.4) and finalclass[i]==1):
                 				 #print 'person'
                  				countp=countp+1
                 				# print countp
                  
    						#end count

      				vis_util.visualize_boxes_and_labels_on_image_array(
          				image_np,
          				np.squeeze(boxes),
          				np.squeeze(classes).astype(np.int32),
          				np.squeeze(scores),
          				category_index,
          				use_normalized_coordinates=True,
          				line_thickness=8)

      			j=str(countp)
      			j="People:"+j
      			font = cv2.FONT_HERSHEY_SIMPLEX 
      			cv2.putText(image_np,j,(10,450), font, 1,(255,255,255),2,cv2.LINE_AA)
      
			#end print count
			
			#database
			id1="0"
     			c1=c1+1
      			if(c1>5):
				deletedb(id1)
      			insertdb(countp,id1);
      			#end db functioncall
      			
      			cv2.imshow('image',image_np)
      			
      
      			if cv2.waitKey(25) & 0xFF == ord('q'):
          
          			cv2.destroyAllWindows()
          			#cap.release()
          			break
          #End tensorflow				
		
 	finally:
            print "Connection closed on thread 1"


class ThreadServer(object):

    def server_thread(host, port):
        server = SocketServer.TCPServer((host, port), VideoStreamHandler)
        server.serve_forever()

    video_thread = threading.Thread(target=server_thread('192.168.43.149', 8063))
    video_thread.start()

if __name__ == '__main__':
    ThreadServer()
