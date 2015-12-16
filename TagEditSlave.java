/*
 * Helper class that changes title and artist tags of one MP3 file.
*/

import org.jaudiotagger.audio.AudioFile;
import org.jaudiotagger.audio.AudioFileIO;
import java.io.File;
import java.io.IOException;
import org.jaudiotagger.tag.FieldKey;
import org.jaudiotagger.tag.*;
import org.jaudiotagger.audio.mp3.MP3File;
import java.util.ArrayList;
import java.util.Scanner;

public class TagEditSlave {
    
    public static void main(String[] args) {
        ArrayList<String[]> dataAL = new ArrayList<String[]>();
        String[] curr = new String[3];
        File f = new File(args[0]);
        int counter = 0;
        try {
            Scanner sc = new Scanner(f);
            int i = 0;
            while (sc.hasNextLine()) {
            	if (i % 3 == 0) {
            		i = 0;
            		counter++;
            		curr = new String[3];
            		dataAL.add(curr);
            	} 
            	curr[i] = sc.nextLine();
            	i++;
            }
        } catch (IOException e) {
        	
        }
        String[][] data = (dataAL.toArray(new String[counter][3]));
        for (int i = 0; i < data.length; i++) {
        	System.out.print("Song " + (i + 1) + ": ");
        	for (int j = 0; j < data[i].length; j++) {
        		System.out.print(data[i][j] + " ");
        	}
        	System.out.println("");
        	rename(data[i]);
        }
        f.delete();
    }
        

    /*
     * Input: filename, artist, title
     * Precondition: filename must be an MP3 file with supported ID3 version (unsure).
     * Postcondition: If the ID3 version is supported, tags will be set properly.
     */
    public static void rename(String[] args) {
        //System.out.println(args[0] + " - " + args[1]);
        try {
            MP3File metadata = (MP3File)AudioFileIO.read(new File(args[0]));
            Tag tag;
            /*if (metadata.hasID3v2Tag()) {
                tag = metadata.getID3v2TagAsv24();
            } else { */
                tag = metadata.getTag();
            //}
            tag.setField(FieldKey.ARTIST, args[1]);
            tag.setField(FieldKey.TITLE, args[2]);
            metadata.commit();

        } catch (IOException e) {
            System.err.println("wtf");
        } catch (Exception e) {
            System.err.println("wtf " + e);
        }
        
    }
}