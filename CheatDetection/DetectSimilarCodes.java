import java.io.*;
import java.util.Collection;
import java.net.URL;
import org.apache.commons.io.FileUtils;
import it.zielke.moji.SocketClient;

public class DetectSimilarCodes {
    public static void main(String[] args) throws Exception {
        // 代码所在文件夹，该文件夹下的文件均为学号，且没有子文件夹
        String codePath = "C:\\Users\\jun\\Desktop\\problem_1\\";

        // 将文件格式改成Moss需要的格式
        File file = new File(codePath);
        File[] files = file.listFiles();
        if(files == null) {
            System.out.println("文件为空！");
            return;
        }
        for(File f : files) {
            if(f.isFile()) {
                String stuId = f.getName().substring(0, f.getName().indexOf("."));
                File d = new File(codePath + stuId);
                if(!d.exists()){
                    d.mkdir();
                }
                File nf = new File(d.getPath() + "\\" + f.getName());
                FileReader fr = new FileReader(f);
                BufferedReader br = new BufferedReader(fr);
                FileWriter fw = new FileWriter(nf);
                BufferedWriter bw = new BufferedWriter(fw);
                String line;
                StringBuilder sb = new StringBuilder();
                while((line = br.readLine()) != null) {
                    sb.append(line).append("\n");
                }
                bw.write(sb.toString());
                bw.close(); fw.close(); br.close(); fr.close();
            }
            f.delete();
        }

        // a list of students' source code files located in the prepared directory.
        Collection<File> codeFiles = FileUtils.listFiles(new File(codePath),
                new String[] { "c", "cpp" }, true);

        //get a new socket client to communicate with the Moss server and set its parameters.
        SocketClient socketClient = new SocketClient();

        //set your Moss user ID
        socketClient.setUserID("402387689");
        //socketClient.setOpt...

        //set the programming language of all student source codes
        socketClient.setLanguage("c");

        //initialize connection and send parameters
        socketClient.run();

        //upload all source files of students
        for (File f : codeFiles) {
            socketClient.uploadFile(f);
        }

        //finished uploading, tell server to check files
        socketClient.sendQuery();

        //get URL with Moss results and do something with it
        URL results = socketClient.getResultURL();
        System.out.println("Results available at " + results.toString());
    }

}
