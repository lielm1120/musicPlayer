import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class SongFileReader {
    public List<String> readSongsFromFile(String filename) {
        List<String> songs = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                songs.add(line.trim());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return songs;
    }
}
