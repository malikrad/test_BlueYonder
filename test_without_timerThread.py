#!/usr/bin/env python
import requests
import threading
from io import open as iopen
from urlparse import urlsplit
from PIL import Image
import time
import sys
#list contains the images names extracted from the URL
images_names=[]


def parseUrlsFile(file):
    """
        this method used to parse the plaintext file and return
        a list containing the non.blank lines
        Parameters:
          file - a plaintext file containing Urls of images
    """
    try:
        file=open(file,"r")
        lines=file.readlines()
        file.close()
        urls=[]
        for line in lines:
            if line.strip():
                urls.append(line)
        return urls
    except IOError:
        print "there is a problem in openning the palintext file:"


def download_image(image_url,url_number):
    """
            this method used to download a image from its Url
            Parameters:
              image_url - url of the image to be downloaded
              url_number - line number of Url within the plaintext file

            1-it checks if the Url points to an image of type jpg, gif or
            png. Moreover, it extracts its name and save it into images_names list
            to be used in future for retrieval purposes

            2- it downloads the image and store it in the system

            3- if there is any error (no image within Url, download interruption
            and store interruption), line printed indicating the url line number
            within the file
    """
    images_suffix_list = ['jpg', 'gif', 'png']
    image_name =  urlsplit(image_url)[2].split('/')[-1]
    images_names.append(image_name)
    image_suffix = image_name.split('.')[1]

    if image_suffix in images_suffix_list:
        download = requests.get(image_url)
        if download.status_code == requests.codes.ok:
            try:
                with iopen(image_name, 'wb') as file:
                    file.write(download.content)
                    print image_name+" successfully downloaded..."

            except IOError:
                print "Could not store file:", image_name
                pass
        else:
            print image_name+" cannnot be downloaded"
    else:
        print image_name+" is not an image----> check UrlFile in line number "+ str(url_number)


def main(file):
    urls = parseUrlsFile(file)
    print "number of images to be downloaded is: "+ str(len(urls))
    for i in range(0,len(urls)):
        print "start downloading images ---->"
        download_image(str(urls[i].strip()),i+1)
    print "downloading images finished ---->"


# checks if the command kine has a file name parameter
if len(sys.argv)==2:
    main(str(sys.argv[1]))
else:
    print "please pass thr name of file"

