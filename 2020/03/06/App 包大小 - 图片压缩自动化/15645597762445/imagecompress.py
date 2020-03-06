# -*- coding: utf-8 -*-
import urllib2
import json
import sys
import os
from base64 import b64encode

class ImageHelper:
    def __init__(self, imagePath, branch):
        self.imagePath = imagePath
        self.branch = branch
    def compress(self):
        file_name = '%s.txt' % self.branch
        file_name = file_name.replace('/', ',');
        path = '%s/%s' % (sys.path[0],file_name)
        print 'path %s' % path
        fp = open(path, 'a')
        print 'compressing %s ...' % self.imagePath
        data = open(self.imagePath, 'rb').read()
        print 'size before compress: %d' % len(data)
        apikey = 'g5RWy9Q01uRNXZqj-wQ7oj0EtFWnpsat'
        req = urllib2.Request('https://api.tinify.com/shrink', data=data)
        req.add_header('Authorization', 'Basic %s' % b64encode(bytes("api:" + apikey).decode('ascii')))
        try:
            res = urllib2.urlopen(req)
        except urllib2.HTTPError:
            print 'request failed'
            context = 'imagePath: %s ; request failed\n' % (self.imagePath)
            fp.write(context)
            return
        if res.getcode() == 201:
            url = res.headers.get('Location')
            result = json.loads(res.read())
            newlength = result['output']['size']
            print 'compress completed! url: %s length %d' % (url, newlength)
            newdata = urllib2.urlopen(url).read()
            open(self.imagePath, 'wb').write(newdata)
            context = 'imagePath: %s ; oldlength: %d ; newlength: %d\n' % (self.imagePath, len(data), newlength)
            fp.write(context)
        else:
            print 'compress failed, try again'
            context = 'imagePath: %s ; compress failed\n' % (self.imagePath)
            fp.write(context)
            compress()

        fp.close()


def main():
    image_helper = ImageHelper(sys.argv[1],sys.argv[2])
    image_helper.compress()
    print "~~~~~~~~~~~~~~~~~~~~~~"

if __name__=='__main__':
    main()