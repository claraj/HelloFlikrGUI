from tkinter import *
#import urllib.request
import requests
import json
import shutil
from PIL import Image
import key

#In Pycharm, Preferences > Project interpreter, add pillow. Or add via pip or however you manage packages

# A very simple application which searches Flickr for cat pictures and displays the first picture in a GUI
# Uses tkinter for the GUI
# Uses pillow ( a PIL fork ) to convert the jgp returned from Flickr to a GIF for tkinter
# Uses HTTP requests to fetch data, no wrappers.


class Flickr(Frame):


    def __init__(self):

        Frame.__init__(self)
        self.grid()

        #Add a label to GUI
        self._label = Label(self, text="Here are some pictures of cats")
        self._label.grid()

        #Sample Flickr search URL build from
        #https://www.flickr.com/services/api/explore/flickr.photos.search
        #Search for cat pictures, modify to search for whatever tag you want


        flickerSearchURL = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&tags=cat&format=json&nojsoncallback=1' % key.flikrkey

        #Search flickr for cat pictures
        flickrResponse = urllib.request.urlopen(flickerSearchURL)
        #get json back
        flickrResponseJSONString = flickrResponse.read().decode('UTF-8')
        flickrResponseJson = json.loads(flickrResponseJSONString)
        #Get first json object ('photos') which contains another json object ('photo') which is an json array; each
        # element represents one photo. Take element 0
        #firstResponsePhoto = flickrResponseJson['photos']['photo'][0]

        #Or, maybe you want lots of cat pictures? This fetches the first 5

        for cat in range(0, 5):
            jsonforphoto = flickrResponseJson['photos']['photo'][cat]
            #deal with this in the following way. vvvvvvv

            #Extract the secret, server, id and farm; which you need to construct another URL to request a specific photo
            #https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg

            secret = jsonforphoto['secret']
            id = jsonforphoto['id']
            server = jsonforphoto['server']
            farm = jsonforphoto['farm']

            print(jsonforphoto)  #Just checking we get the JSON we expect
            #TODO add error handing

            fetchPhotoURL = 'https://farm%s.staticflickr.com/%s/%s_%s_m.jpg' % (farm, server, id, secret)
            print(fetchPhotoURL)   #Again, just checking

            #Reference: http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests

            catPicFileNameJPEG = 'cat' + str(cat) + '.jpg'
            catPicFileGif = 'cat' + str(cat) + '.gif'

            #Read the response and save it as a .jpg. Use shutil to copy the stream of bytes into a file
            #What does 'with' mean? http://preshing.com/20110920/the-python-with-statement-by-example/
            resp = requests.get(fetchPhotoURL, stream=True)
            with open(catPicFileNameJPEG, 'wb') as out_file:
                shutil.copyfileobj(resp.raw, out_file)
            del resp


            #Flickr returns a jpg. Tkinter displays gif. Use pillow to convert the JPG to GIF
            #Reference https://pillow.readthedocs.org/handbook/tutorial.html

            Image.open(catPicFileNameJPEG).save(catPicFileGif)

            #Add PictureImage to GUI. Remember within loop so adds all 5 pictures.
            #TODO arrange nicely
            _catPic = PhotoImage(file=catPicFileGif)
            _catPicLabel = Label(self, image=_catPic)
            _catPicLabel.image = _catPic  #Keep a reference to the image or it doesn't show up
            _catPicLabel.grid()



def main():

    Flickr().mainloop()

main()
