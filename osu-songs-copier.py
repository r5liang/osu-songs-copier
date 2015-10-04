import os
import re
import time
import shutil
#import eyed3
#from mutagen.easyid3 import EasyID3
#from tagger import *
import subprocess

dir = "C:/Program Files (x86)/osu!/Songs" # osu Songs folder
newpath = "./stuff" # destination folder
filenames = os.listdir(dir) # all the song folders
invalidosus = 0
print len(filenames)

if not os.path.exists(newpath):
    os.mkdir(newpath)

for i in filenames: # for each song folder
    currdir = os.path.join(dir, i)
    currfiles = os.listdir(currdir)
    j = 0
    osufound = False
    songfound = False
    currosu = ""
    currsong = ""
    currnewfilename = ""
    songsnotfound = 0
    osusnotfound = 0

    songscopied = 0

    # for each file in the song folder
    while (j < len(currfiles) and (not osufound or not songfound)):
        if not osufound: # search for .osu file
            if re.search(r".+\.osu$", currfiles[j]):
                currosu = currfiles[j]
                osufound = True

        if re.search(r".+\.mp3$", currfiles[j]): # search for .mp3 file
            # this part will find the largest mp3 file in the folder, in case some mapper decides to use mp3 hitsounds
            if not songfound or os.path.getsize(os.path.join(currdir, currfiles[j])) > os.path.getsize(os.path.join(currdir, currsong)): 
                currsong = currfiles[j]
                songfound = True           
        j = j + 1

    if songfound:
        if osufound: # searching for artist and title in .osu file
            currtitle = ""
            currartist = ""
            f = open(os.path.join(currdir, currosu), "rU")
            fullfile = f.read()
            titlematch = re.search(r"Title:([\S ]+)", fullfile)
            artistmatch = re.search(r"Artist:([\S ]+)", fullfile)   
            if artistmatch:
                currartist = artistmatch.group(1)
            if titlematch:
                currtitle = titlematch.group(1)
            if (not titlematch or not artistmatch):
                invalidosus = invalidosus + 1
                print "wtf"
          
            sanitizedcurrartist = re.sub(r'[\\\/\:\*\?\<\>"\|]', "", currartist) # forbidden characters in filename
            sanitizedcurrtitle = re.sub(r'[\\\/\:\*\?\<\>"\|]', "", currtitle) # forbidden characters in filename
            currnewfilename = sanitizedcurrartist + " - " + sanitizedcurrtitle + ".mp3"

            counter = 2 # incrementing identical file names
            while os.path.exists(os.path.join(newpath, currnewfilename)):
                currnewfilename = sanitizedcurrartist + " - " + sanitizedcurrtitle + " " + str(counter) + ".mp3"
                counter = counter + 1
                
        else:
            osusnotfound = osusnotfound + 1
        
        #print os.path.join(currdir, currsong)
        #print os.path.join(newpath, currnewfilename)
            
        # after dealing with .osu file
        # copying the file to new directory with new name
        shutil.copy(os.path.join(currdir, currsong), os.path.join(newpath, currnewfilename))
        songscopied = songscopied + 1

        
        if osufound: # writing to file's metadata if available
            '''
            metadata = eyed3.load(os.path.join(newpath, currnewfilename))          
            metadata.tag.artist = currartist.decode("utf-8")
            metadata.tag.title = currtitle.decode("utf-8")
            metadata.tag.save()
            
            metadata = EasyID3(os.path.join(newpath, currnewfilename))
            metadata["artist"] = currartist.decode("utf-8")
            metadata["title"] = currtitle.decode("utf-8")
            metadata.save()
            '''
            subprocess.Popen(["java", "-cp", ".;jaudiotagger-2.2.4.jar", "Metadata2", os.path.join(newpath, currnewfilename), currartist, currtitle])
                 
    else:
        songsnotfound = songsnotfound + 1
        
###print songsnotfound
###print osusnotfound
###print invalidosus
