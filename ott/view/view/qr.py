import qrcode

def qr_to_file(content, path='', name='qr', ext='png'): 
    img  = qrcode.make(content)
    file_name = "{0}{1}.{2}".format(path, name, ext)
    f = open(file_name, 'w+')
    img.save(f, ext.upper()) 
    f.close()


def qr_to_stream(content, ext='png'): 
    img  = qrcode.make(content)
    img_io = StringIO.StringIO()
    img.save(img_io, ext.upper()) 
    img_io.seek(0)
    return img_io


if __name__ == "__main__":
    qr_to_file('http://maps.trimet.org?from=PDX&to=ZOO')

