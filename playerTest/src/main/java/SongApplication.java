import java.util.List;

public class SongApplication {
    public static void main(String[] args) {
        // Constants definition
        final String FILE_NAME = "/Users/lielmachluf/IdeaProjects/playerTest/src/main/java//songs.txt";

        // Variable definition
        SongFileReader reader = new SongFileReader();
        YouTubePlayer player = new YouTubePlayer();
        PythonRunner aiRunner = new PythonRunner();

        // Code section

        aiRunner.runAI();
        for (String song : reader.readSongsFromFile(FILE_NAME)) {
            if(!song.isEmpty()) {
                System.out.println("Playing: " + song);
                player.playSong(song);
            }
        }

        player.close();
    }
}
