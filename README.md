# osu-songs-copier

* Extracts song mp3 files from their beatmap folders and copies them to a single directory.  
* Renames every file in the form "Artist - Title", which are found with regex searches in any .osu file in the same folder. Duplicate song names are incremented. 
* Attempts to write this metadata to the MP3's tags. 

MP3 files can have different ID3 tag versions that store metadata differently. The majority of time was spent trying different Python ID3 libraries to edit these tags, but no library was able to handle multiple ID3 versions and they were too outdated/convoluted or failed outright. Eventually I outsourced the tag editing part to a Java helper class I wrote to use a Java library, of which there were far more options. Jaudiotagger (found here http://www.jthink.net/jaudiotagger/) was the most successful, and manages to set tags for most of the files, so thanks to them.

###Instructions for usage: 
* **You must have Python 2.7 and Java Runtime Environment installed.** 
* Open config.txt and replace the path after "dir=" with your current Songs directory. The default (which should work for most people running Windows 7 or 8) is C:/Program Files (x86)/osu!/Songs
* Replace the path after "dest=" with the location of your destination folder. All new files will be copied to here. The default is a folder called stuff inside the current directory.
* Double-click osu-songs-copier.py to start. The entire process should take several minutes depending on the size of your Songs folder and speed of your hard disk. DO NOT RUN THIS IN THE COMMAND LINE (python osu-songs-copier.py) OR YOU WILL BE OVERWHELMED BY HUNDREDS OF CMD WINDOWS!! (because a Java program is called on to edit the tags)
* Duplicate songs will exist in case two songs have the same name but happen to be different cuts or remixes of each other. They can be dealt with relatively easily on a case-by-case basis (sort alphabetically and look for similar filenames).

If you want to compile TagEditSlave.java (requires JDK): javac -cp jaudiotagger-2.2.4.jar TagEditSlave.java

###Known Issues:
* Can't set tags in some files with different ID3 versions
* Somehow fewer songs are copied than than beatmap folders in the Songs directory
* First world problem: MY SSD CALLS THE JAVA TAG EDITOR SO QUICKLY THAT WINDOWS RUNS OUT OF MEMORY

###Later features:
* Prevent java cmd window spam when running from command line
* Use source for album tag
* Use judgement for duplicates by comparing song lengths
* Probably make all or some of the above optional and with a config text file or GUI interface instead of command line