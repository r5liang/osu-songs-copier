import os
import re
import time
import shutil
#import eyed3
import subprocess

# reading input arguments from config.txt file
f = open("config.txt", "rU")
params = f.read()
match = re.search(r"dir=(.*)", params)
if not match:
    print "Config dir variable missing"
    quit()
dir = match.group(1) # osu Songs folder
match = re.search(r"dest=(.*)", params)
if not match:
    print "Config dest variable missing"
    quit()
newpath = match.group(1) # destination folder
match = re.search(r"antidupe=(.*)", params)
if not match:
    print "Config antidupe variable missing"
    quit()
antidupestr = match.group(1).lower()
antidupe = False
if antidupestr == "true":
    antidupe = True
elif antidupestr == "false":
    antidupe = False
else:
    print "Config antidupe invalid"
    quit()
    
filenames = os.listdir(dir) # all the song folders
tobecopied = "" # list of data to transfer to java

# some counters just for checking stuff
songsnotfound = 0
osusnotfound = 0
songscopied = 0
invalidosus = 0

if not os.path.exists(newpath):
    os.mkdir(newpath)

for i in filenames: # for each song folder
    currdir = os.path.join(dir, i) # full path of the current song folder
    if not os.path.isdir(currdir):
        continue
    currfiles = os.listdir(currdir) # all files in the folder
    j = 0
    osufound = False
    songfound = False
    currosu = ""
    currsong = ""
    currnewfilename = ""


    # for each file in the song folder
    while (j < len(currfiles) and (not osufound or not songfound)):
        if not osufound: # search for .osu file
            if re.search(r".+\.osu$", currfiles[j]):
                currosu = currfiles[j]
                osufound = True

        if re.search(r".+\.mp3$", currfiles[j]): # search for .mp3 file
            # this part will find the largest mp3 file in the folder,
            # in case some mapper decides to use mp3 hitsounds
            if not songfound or os.path.getsize(os.path.join(
                currdir, currfiles[j])) > os.path.getsize(
                    os.path.join(currdir, currsong)): 
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

            # forbidden characters in filename
            sanitizedcurrartist = re.sub(r'[\\\/\:\*\?\<\>"\|]', "", currartist)
            sanitizedcurrtitle = re.sub(r'[\\\/\:\*\?\<\>"\|]', "", currtitle) 
            currnewfilename = (sanitizedcurrartist + " - " +
                               sanitizedcurrtitle + ".mp3")

            counter = 2 # incrementing identical file names
            while os.path.exists(os.path.join(newpath, currnewfilename)):
                currnewfilename = (sanitizedcurrartist + " - " +
                sanitizedcurrtitle + " " + str(counter) + ".mp3")
                counter = counter + 1
                
        else:
            osusnotfound = osusnotfound + 1
        
        #print os.path.join(currdir, currsong)
        #print os.path.join(newpath, currnewfilename)
            
        # after dealing with .osu file
        # copying the file to new directory with new name
        shutil.copy(os.path.join(currdir, currsong),
                    os.path.join(newpath, currnewfilename))
        songscopied = songscopied + 1

        
        if osufound: # writing to file's metadata if available
            ''' Old (not working) eyed3 code
            metadata = eyed3.load(os.path.join(newpath, currnewfilename))          
            metadata.tag.artist = currartist.decode("utf-8")
            metadata.tag.title = currtitle.decode("utf-8")
            metadata.tag.save()
            '''
            print currartist + " - " + currtitle
            '''
            # outsourcing tag editing to java class
            subprocess.Popen(["java", "-cp", ".;jaudiotagger-2.2.4.jar",
                              "TagEditSlave",
                              os.path.join(newpath, currnewfilename),
                              currartist, currtitle])
            '''
            tobecopied = tobecopied + os.path.join(newpath, currnewfilename) + \
                         "\n" + currartist + "\n" + currtitle + "\n"
    else:
        songsnotfound = songsnotfound + 1

f = open("osctemp.txt", "w")
f.write(tobecopied[:len(tobecopied)-1])
f.close()
# outsourcing tag editing to java class
subprocess.Popen(["java", "-cp", ".;jaudiotagger-2.2.4.jar", "TagEditSlave",
                  "osctemp.txt"])

print str(songscopied) + " songs copied!"
###print songsnotfound
###print osusnotfound
###print invalidosus
