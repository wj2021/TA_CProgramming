import java.io.*;

public class CheckErrorForPerson {
    private static String dir = "C:\\Users\\jun\\Desktop\\problem_4\\"; // 需要验证的程序目录
    private static int inputNum = 10; // 使用20组样例测试代码
    private static boolean showLog = false;

    // 构造输入
    private static String constructInput(final int n) {
        File file = new File("C:\\Users\\jun\\Desktop\\in\\input" + (n + 1) + ".txt");
        FileReader fr;
        BufferedReader br;
        String input = "";
        try {
            fr = new FileReader(file);
            br = new BufferedReader(fr);
            char bn = 10;
            input = br.readLine() + bn + br.readLine() + bn + br.readLine();
            br.close();
            fr.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
        return input;
    }

    public static void main(final String[] args) throws IOException, InterruptedException {
        final long startTime = System.currentTimeMillis();

        // 编译dir目录下所有源代码文件
        final File f = new File(dir);
        File[] files = f.listFiles();
        System.out.println("compiling...");
        if (files == null)
            return;
        for (final File subFile : files) {
            final String fileName = subFile.getName();
            compile(fileName);
            Thread.sleep(50);
        }
        System.out.println("compiling down!");

        Thread.sleep(5000);

        // 运行
        System.out.println("running...");
        String[] cp = { "", "", "", "", "", "", "", "", "", "", "" };
        final String correctProgram = "mf1933100.exe";
        for (int n = 0; n < inputNum; ++n) { // 使用多组输入判断程序和正确程序的输出是否相同
            String input = constructInput(n);
            // 运行正确程序并输出正确结果
            final String cpResult = runApplication(dir + correctProgram, input);
            cp[n] = cpResult;
        }

        // 运行其他程序，将结果与正确程序比较，看看是否正确
        files = new File(dir).listFiles();
        assert files != null;
        for (final File file : files) {
            if (file.getName().equals("191870080.exe")) {
                System.out.println("======================================================================================");
                System.out.println("running " + file.getName());
                for (int i = 0; i < inputNum; ++i) {
                    String input = constructInput(i);
                    final String result = runApplication(file.getPath(), input);
                    if (!cp[i].equals(result)) {
                        System.out.println("input"+(i+1) + ":\n" + input + "\n" + "error result: " + result + "  ||  correctResult: " + cp[i]);
                        System.out.println();
                    }
                }

            }
        }

        final long endTime = System.currentTimeMillis();
        System.out.println("Total Execution Time: " + (endTime - startTime) / 1000.0 + " s");
    }

    private static void compile(final String fileName) throws IOException {
        if (fileName.endsWith(".c") || fileName.endsWith("cpp")) {
            final String name = fileName.substring(0, fileName.indexOf(".c"));
            if (!new File(dir + name + ".exe").exists()) {
                final String cmd = "g++ " + dir + fileName + " -o " + dir + name;
                Runtime.getRuntime().exec(cmd);
            }
        }
    }

    /**
     * 通过 Runtime 调用运行 exe 文件
     *
     * @param filePath    exe 文件绝对路径
     * @param inputString 程序读取数据
     * @throws InterruptedException
     * @throws FileNotFoundException
     */
    static Process p;

    static public String runApplication(final String filePath, final String inputString)
            throws InterruptedException, FileNotFoundException {
        final File file = new File(filePath);
        if (!file.exists())
            throw new FileNotFoundException("找不到exe文件: " + filePath + "!");
        try {
            p = Runtime.getRuntime().exec(filePath);
            if (showLog)
                System.out.println(" -----------------\n " + filePath.substring(filePath.lastIndexOf("\\") + 1));
            // exe程序数据输入流
            final BufferedOutputStream input = new BufferedOutputStream(p.getOutputStream());
            // exe程序数据输出流，相当于进程标准输入+流
            final BufferedInputStream output = new BufferedInputStream(p.getInputStream());

            final StringBuffer outputText = new StringBuffer();

            // 向线程进行输入
            // new Thread(() -> {
            try {
                // 将用户输入数据写入
                input.write(inputString.getBytes());
                input.flush(); // 清空缓存
                if (showLog)
                    System.out.println("input: " + inputString);
            } catch (final IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    input.close();
                } catch (final IOException e) {
                    e.printStackTrace();
                }
            }
            // }).start();

            // 获得输出的线程
            // new Thread(() -> {
            int ch;
            try {
                // 不断获取用户输出
                while ((ch = output.read()) != -1) {
                    outputText.append((char) ch);
                    if (showLog)
                        System.out.print(ch + " ");
                }
            } catch (final IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    output.close();
                } catch (final IOException e) {
                    e.printStackTrace();
                }
            }
            // }).start();

            if (showLog)
                System.out.println("output: " + outputText.toString().replaceAll("\\s+", " ") + "\n----------------\n");
            return outputText.toString().replaceAll("\\s+", " ").trim();
        } catch (final IOException e) {
            e.printStackTrace();
            return null;
        } finally {
            if (p != null) {
                p.destroy();
            }
        }
    }
}