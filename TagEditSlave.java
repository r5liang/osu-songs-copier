import org.jaudiotagger.audio.AudioFile;
import org.jaudiotagger.audio.AudioFileIO;
import java.io.File;
import java.io.IOException;
import org.jaudiotagger.tag.FieldKey;
import org.jaudiotagger.tag.*;
import org.jaudiotagger.audio.mp3.MP3File;

public class TagEditSlave {
    public static void main(String[] args) {
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
            System.err.println(e);
        }
        
    }
}