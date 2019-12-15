#!/anaconda3/bin/python
# -*- coding: UTF-8 -*-
print ('Content-Type: text/html')
print ('')
import cgi,os
import matplotlib.image as mpimg
from PIL import Image
import cgitb;cgitb.enable()
form=cgi.FieldStorage()
fileitem=form['filename']
if fileitem.filename:
	fn=os.path.basename(fileitem.filename)
	open('/Users/chuci/apa/CGI-Executables/files/'+fn,'wb').write(fileitem.file.read())
	#message = mpimg.imread('/Users/chuci/apa/CGI-Executables/files/'+fn)
	im = Image.open('/Users/chuci/apa/CGI-Executables/files/'+fn)
	im1 = im.convert('L')
	im1.save('/Users/chuci/apa/CGI-Executables/files/test123.png')
	message = mpimg.imread('/Users/chuci/apa/CGI-Executables/files/test123.png')
    
else:
    message='fail'
print ("""\
<html>
<head>
<meta charset="utf-8">
<title>test</title>
</head>
<body>
   <p>%s</p>
</body>
</html>
""" % (message,))
