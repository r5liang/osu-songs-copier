# osu-songs-copier

* Extracts song mp3 files from their beatmap folders and copies them to a single directory.  
* Renames every file in the form "Artist - Title", which are found with regex searches in any .osu file in the same folder. Duplicate song names are incremented. 
* Attempts to write this metadata to the MP3's tags. 

MP3 files can have different ID3 tag versions that store metadata differently. The majority of time was spent trying different Python ID3 libraries to edit these tags, but no library was able to handle multiple ID3 versions and they were too outdated/convoluted or failed outright. Eventually I outsourced the tag editing part to a Java helper class I wrote to use a Java library, of which there were far more options. Jaudiotagger (found here http://www.jthink.net/jaudiotagger/) was the most successful, and manages to set tags for most of the files, so thanks to them.

###Instructions for usage: 
* Double-click stuff.py to start. The entire process should take several minutes depending on the size of your Songs folder and speed of your hard disk. DO NOT RUN THIS IN THE COMMAND LINE (python stuff.py) OR YOU WILL BE OVERWHELMED BY HUNDREDS OF CMD WINDOWS!! (because a Java program is called on to edit the tags)
* The current Songs directory is hardcoded in the dir variable as C:/Program Files (x86)/osu!/Songs. I haven't added command line argument functionality to specify a Songs folder location yet (and the default should work for most people), but if you need you can change the dir variable in stuff.py.
* All new files will be copied to a folder stuff in the current directory. Again, there are no command line arguments to specify a destination folder yet, but feel free to change the newpath variable in stuff.py.
* Duplicate songs will exist in case two songs have the same name but happen to be different cuts or remixes of each other. They can be dealt with relatively easily on a case-by-case basis (sort alphabetically and look for similar filenames).

###Known Issues:
Can't set tags in some files with different ID3 versions

###Later features:
Support command line input for certain arguments
Prevent java cmd window spam when running from command line
