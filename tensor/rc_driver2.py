__author__ = 'zhengwang'

import threading
import SocketServer
#import serial
import cv2
import numpy as np
import math

# distance data measured by ultrasonic sensor
#sensor_data = " "


'''class NeuralNetwork(object):

    def __init__(self):
        self.model = cv2.ANN_MLP()

    def create(self):
        layer_size = np.int32([38400, 32, 4])
        self.model.create(layer_size)
        self.model.load('mlp_xml/mlp.xml')

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)


class RCControl(object):

    def __init__(self):
        haha=0#self.serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

    def steer(self, prediction):
        if prediction == 2:
            #self.serial_port.write(chr(1))
            print("Forward")
        elif prediction == 0:
           # self.serial_port.write(chr(7))
            print("Left")
        elif prediction == 1:
           # self.serial_port.write(chr(6))
            print("Right")
        else:
            self.stop()

    def stop(self):
       yo=80# self.serial_port.write(chr(0))


class DistanceToCamera(object):

    def __init__(self):
        # camera params
        self.alpha = 8.0 * math.pi / 180
        self.v0 = 119.865631204
        self.ay = 332.262498472

    def calculate(self, v, h, x_shift, image):
        # compute and return the distance from the target point to the camera
        d = h / math.tan(self.alpha + math.atan((v - self.v0) / self.ay))
        if d > 0:
            cv2.putText(image, "%.1fcm" % d,
                (image.shape[1] - x_shift, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return d


class ObjectDetection(object):

    def __init__(self):
        self.red_light = False
        self.green_light = False
        self.yellow_light = False

    def detect(self, cascade_classifier, gray_image, image):

        # y camera coordinate of the target point 'P'
        v = 0

        # minimum value to proceed traffic light state validation
        threshold = 150     
        
        # detection
        cascade_obj = cascade_classifier.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # draw a rectangle around the objects
        for (x_pos, y_pos, width, height) in cascade_obj:
            cv2.rectangle(image, (x_pos+5, y_pos+5), (x_pos+width-5, y_pos+height-5), (255, 255, 255), 2)
            v = y_pos + height - 5
            #print(x_pos+5, y_pos+5, x_pos+width-5, y_pos+height-5, width, height)

            # stop sign

            roi = gray_image[y_pos+10:y_pos + height-10, x_pos+10:x_pos + width-10]
            mask = cv2.GaussianBlur(roi, (25, 25), 0)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
                
            # check if light is on
            if maxVal - minVal > threshold:
                    cv2.circle(roi, maxLoc, 5, (255, 0, 0), 2)
                    
                    # Red light
                    if 1.0/8*(height-30) < maxLoc[1] < 4.0/8*(height-30):
                        cv2.putText(image, 'Red', (x_pos+5, y_pos-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        print "red light detected"
                        self.red_light = True
                    
                    # Green light
                    elif 5.5/8*(height-30) < maxLoc[1] < height-30:
                        cv2.putText(image, 'Green', (x_pos+5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        print "green light detected"
                        self.green_light = True
    
                    # yellow light
                    #elif 4.0/8*(height-30) < maxLoc[1] < 5.5/8*(height-30):
                    #    cv2.putText(image, 'Yellow', (x_pos+5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    #    self.yellow_light = True
        return v


'''

class VideoStreamHandler(SocketServer.StreamRequestHandler):
    print("hi1")
    # h1: stop sign
    h1 = 15.5 - 10  # cm
    # h2: traffic light
    h2 = 15.5 - 10

    # create neural network
    #model = NeuralNetwork()
    #model.create()

    #obj_detection = ObjectDetection()
    #rc_car = RCControl()

    # cascade classifiers
    #stop_cascade = cv2.CascadeClassifier('cascade_xml/stop_sign.xml')
    #light_cascade = cv2.CascadeClassifier('cascade_xml/traffic_light.xml')
    #limit_cascade =  cv2.CascadeClassifier('cascade_xml/speed_limit.xml')

    #d_to_camera = DistanceToCamera()
    d_stop_sign = 25
    d_light = 25
    d_limit = 25

    stop_start = 0              # start time when stop at the stop sign
    stop_finish = 0
    stop_time = 0
    drive_time_after_stop = 0

    def handle(self):
	print("hi2")
        #global sensor_data
        stream_bytes = ' '
        stop_flag = False
        stop_sign_active = False
	l=1

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
		    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),1)
		    gray= cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),0)
		    cv2.imwrite(temp,img)
		    
		    #ims = cv2.resize(img, (640, 480)) 
		    #cv2.imshow('image', ims)
		    
		    cv2.imwrite(temp,img)
		    #cv2.imshow('img', img)
                    #your code goes here
		#cv2.destroyAllWindows()
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
