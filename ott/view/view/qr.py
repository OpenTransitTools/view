import qrcode
img  = qrcode.make('http://maps.trimet.org?from=PDX&to=ZOO')
path = ''
name = 'qr'
ext  = 'png'
file_name = "{0}{1}.{2}".format(path, name, ext)
f = open(file_name, 'w+')
img.save(f, ext.upper()) 
f.close()
