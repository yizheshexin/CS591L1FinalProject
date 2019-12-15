#!/anaconda3/bin/python
# -*- coding: UTF-8 -*-
print ('Content-Type: text/html')
print ('')
import cgi,os
from skimage import io
import socket,pickle
from socket import AF_INET, SOCK_DGRAM
import cgitb;cgitb.enable()
###
import cv2
import scipy
import numpy as np
from skimage import io
from fractions import Fraction
import matplotlib.pyplot as plt
from sklearn.decomposition import *
from skimage.transform import resize
from sklearn.preprocessing import scale
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
form=cgi.FieldStorage()
fileitem=form['filename']
def img_to_num(image):
    im_resized = scipy.misc.imresize(image, (8,8))
    im_gray = cv2.cvtColor(im_resized, cv2.COLOR_BGR2GRAY)
    im_hex = Fraction(16,255) * im_gray
    im_reverse = 16 - im_hex
    return im_reverse.astype(np.int)
if fileitem.filename:
    fn=os.path.basename(fileitem.filename)
    open('/Users/chuci/apa/CGI-Executables/files/'+fn,'wb').write(fileitem.file.read())
    #message = mpimg.imread('/Users/chuci/apa/CGI-Executables/files/'+fn)
    img = io.imread('/Users/chuci/apa/CGI-Executables/files/'+fn)
    reshaped = img_to_num(img)
    reshaped = reshaped.reshape(1, 64)[0]

#connection part
###############
    s = socket.socket()
    s.connect(('server.geni5.ch-geni-net.genirack.nyu.edu',1133))
    s.settimeout(3)
    messsage= reshaped
    data_string = pickle.dumps(messsage)
    while(True):
        try:
            s.send(data_string) # send the image all
            data = s.recv(1024)
            message = repr(pickle.loads(data))
            #print('Received result', repr(pickle.loads(data)))
            s.close()
            break
        except :
            print ('Retrying after TimeoutError')
            continue

############## connnection part ends
    print ("""\
    <html>
    <head>
    <meta charset="utf-8">
    <title>CS655 geni project</title>
    </head>
    <body>
    <h1>Recognition complete!</h1>
    <p>The picture that you upload is:</p>
    <img src='/CGI-Executables/files/{}'  alt="upload picture" />
    <h2>The result is:{}</h2>
    <a href="/index1.html">
        <button>try again!</button>
    </a>
    </body>
    </html>
    """.format(fn,message))
else:
    message='fail'
    print ("""\
    <html>
    <head>
    <meta charset="utf-8">
    <title>CS655 geni project</title>
    </head>
    <body>
    <h1>You don't upload the picture</h1>
    <a href="/index1.html">
        <button>try again!</button>
    </a>
    </body>
    </html>
    """)

