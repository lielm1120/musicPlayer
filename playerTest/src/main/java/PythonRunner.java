import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class PythonRunner {
    public void runPythonScript(String pythonScriptPath, String songsFilePath) {
        // Variables definition
        String pythonExecutable = "python3";

        // List definition
        List<String> command = new ArrayList<>();

        command.add(pythonExecutable);
        command.add(pythonScriptPath);
        command.add(songsFilePath);

        ProcessBuilder processBuilder = new ProcessBuilder(command);

        try {
            Process process = processBuilder.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public  void runAI() {
        String scriptPath = "/Users/lielmachluf/PycharmProjects/playerTest-AI/main.py";
        String filePath = "/Users/lielmachluf/IdeaProjects/playerTest/src/main/java//songs.txt";
        this.runPythonScript(scriptPath, filePath);
    }
}
