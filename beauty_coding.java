import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * Created by Gary Ma on 2017/6/5.
 */
public class beauty_coding {
    static String trainSourceFile=".\\BoP2017_DBAQ_dev_train_data\\BoP2017-DBQA.train.txt";
    static String questionDevSourceFile=".\\BoP2017_DBAQ_dev_train_data\\questionDevOnly.txt";
    static String questionTrainSourceFile=".\\BoP2017_DBAQ_dev_train_data\\questionTrainOnly.txt";
    static String questionAnswerTrainout=".\\BoP2017_DBAQ_dev_train_data\\questionAnswerTrainOut.txt";
    static String intentInformation=".\\BoP2017_DBAQ_dev_train_data\\intentInformation.txt";

    ArrayList<Intent> intentList=new ArrayList<>();
    ArrayList<String> entities;
    String intentName;
    ArrayList<String> intentNameList=new ArrayList<>();

    public static void main(String[] args) throws IOException {	

        new beauty_coding().updateTheWholeProcess();
    }
	
    //update the process
    private void updateTheWholeProcess() throws IOException {
        beauty_coding microsoft=new beauty_coding();
        microsoft.populateIntentMatching();
        ArrayList<String> feature=microsoft.getCurrentFeatures();
        microsoft.processSpareFile(feature);
        microsoft.putQuestionIntoIntentFile();
        microsoft.getCurrentIntentInformation();
        microsoft.getTheQuestion();
    }

    //create a file with the current intent and its feature
    private void getCurrentIntentInformation() throws IOException {
        File intentFile=new File(intentInformation);
        FileWriter writer=new FileWriter(intentFile);
        for(Intent intent:intentList){
            String current=intent.getIntentName();
            current+=current.length()==6?"\t":"\t\t";
            current+=intent.getEntities().toString()+"\n";
            writer.write(current);
        }
		writer.write("// the following is all of the entents used for all of the intents"+"\n");
        writer.write("\n"+getCurrentFeatures().toString());
        writer.close();
    }

    //get the current feature;
    private ArrayList<String> getCurrentFeatures() {
        ArrayList<String> feature=new ArrayList<>();
        for(Intent intent:intentList){
            feature.addAll(intent.getEntities());
        }
        return feature;
    }

    //put different questions into different file
    private void putQuestionIntoIntentFile() throws IOException {
        //create the relevant file writers in a map
        String intentAndQuestionsOutPut=".\\BoP2017_DBAQ_dev_train_data\\intentFile";
        for(Intent intent:intentList){
            intentNameList.add(intent.getIntentName());
        }
        HashMap<String,FileWriter> writerMap=new HashMap<>();
        for(String s:intentNameList){
            File intentFile=new File(intentAndQuestionsOutPut+"\\"+s+".txt");
            writerMap.put(s,new FileWriter(intentFile));
        }

        //put the current distinguishable questions into their place
        File input=new File(questionTrainSourceFile);
        Scanner scanner=new Scanner(input);
        while(scanner.hasNext()){
            String current=scanner.next();
            for(Intent intent:intentList){
                for(String s:intent.getEntities()){
                    if(current.contains(s)){
                        if(!(intent.getIntentName()=="询问别名"&&(current.contains("哪年")||current.contains("什么时候"))&&current.contains("名称"))
                                &&!(intent.getIntentName()=="询问原因"&&(current.contains("为什么"))&&(current.contains("成为什么")||current.contains("称为什么")||current.contains("评为什么"))))
                        writerMap.get(intent.getIntentName()).write(current+"\n");
                    }
                }
            }
        }
        scanner.close();

        //put the other cases left into it
        String remainingFilePath=".\\BoP2017_DBAQ_dev_train_data\\questionTrainRemaining.txt";
        File remainingFile=new File(remainingFilePath);
        Scanner remainingScanner=new Scanner(remainingFile);

        String secondRoundRemainingPath=".\\BoP2017_DBAQ_dev_train_data\\questionTrainSecondRemaining.txt";
        File secondRoundRemainingFile=new File(secondRoundRemainingPath);
        FileWriter secondWriter=new FileWriter(secondRoundRemainingFile);

        HashMap<String,FileWriter> remainingMap=new HashMap<>();
        remainingMap.put("几",writerMap.get("询问数量"));
        remainingMap.put("什么",writerMap.get("询问名称定义"));
        remainingMap.put("怎么",writerMap.get("询问方法"));
        remainingMap.put("如何",writerMap.get("询问方法"));
        remainingMap.put("哪",writerMap.get("询问名称定义"));

        for(Intent intent:intentList){
            switch(intent.getIntentName()){
                case "询问名称定义":
                    intent.addEntity("什么");
                    intent.addEntity("哪");
                    break;
                case "询问方法":
                    intent.addEntity("怎么");
                    intent.addEntity("如何");
                    break;
                    case "询问数量":
                    intent.addEntity("几");
                    break;
                default:
                    break;
            }
        }

        while(remainingScanner.hasNext()){
            String current=remainingScanner.next();
            if(current.contains("几")){
                remainingMap.get("几").write(current+"\n");
            }else if(current.contains("什么")){
                remainingMap.get("什么").write(current+"\n");
            }else if(current.contains("怎么")){
                remainingMap.get("怎么").write(current+"\n");
            }else if(current.contains("哪")){
                remainingMap.get("哪").write(current+"\n");
            }else if(current.contains("如何")){
                remainingMap.get("如何").write(current+"\n");
            }else{
                secondWriter.write(current+"\n");
            }
        }
        secondWriter.close();
        remainingScanner.close();

        //save and close the file
        for(Map.Entry<String,FileWriter> entry:writerMap.entrySet()){
            entry.getValue().close();
        }
    }

    //to see how many of the questions are left and put them into the remainFile
    private void processSpareFile(ArrayList<String> currentFeature) throws IOException {

        String outFile=".\\BoP2017_DBAQ_dev_train_data\\questionTrainRemaining.txt";
        File input=new File(questionTrainSourceFile);
        Scanner scanner=new Scanner(input);
        File output=new File(outFile);
        FileWriter writer=new FileWriter(output);
        while(scanner.hasNext()){
            String current=scanner.next();
            Boolean writable=true;
            for(String s:currentFeature){
                if(current.contains(s)){
                    writable=false;
                    break;
                }
            }
            if(writable){
                writer.write(current+"\n");
            }
        }
        scanner.close();
        writer.close();
    }

    // a helper with the regex helper
    private static void test(){
        String test="0\t台北市立建国高级中学附设高级进修补习学校什么时候停止开夜间部的？\t夜间部及补校同学是在卡其制服上綉黑色的学号，外套（夹克）上綉白色的学号。";
        Pattern pat=Pattern.compile("\t(.*?)\t(.*)");
        Matcher mat=pat.matcher(test);
        while(mat.find()){
            System.out.println(mat.group());
            System.out.println(mat.group(1));
            System.out.println(mat.group(2));
        }
    }

    //a helper method to generate the intent and put the intent into the intentList
    private void generateAIntent(String Name,ArrayList<String> feature){
        ArrayList<String> entities=new ArrayList<String>();
        for(String s:feature){
            entities.add(s);
        }
        Intent intent=new Intent(Name,entities);
        intentList.add(intent);
    }

    //use the matching rule to populate the intent list
    public void populateIntentMatching(){
        entities=new ArrayList<>(
                Arrays.asList("时候","什么时间","哪年","那年","哪一年","几号","日期","时期",
                        "几月","哪一天","哪天","何时","几年","时间","几岁","何年","在什么建立"));
        intentName="询问时间";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("谁","哪个人","那个人","叫什么","名字","是哪一个","校长","哪位","那位"));
        intentName="询问人名";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("多少个","是多少","多少","多少年","数量","几次","多少天","几个","有几",
                        "多久","第几","几条","几类","几家","几天"));
        intentName="询问数量";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("多大","大小","多深","速度",
                        "多快","多高","多重","多长","多宽"));
        intentName="询问量度";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("哪些","有什么","吃什么","哪几","那两个","那些","有些什么","哪两","哪四","哪七","哪三","哪4",
                        "哪八"));
        intentName="询问枚举";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("哪个","是什么","哪部","什么活动","网址是",
                        "什么语言","什么是","指什么","什么人","什么叫"));
        intentName="询问名称定义";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("多大"));
        intentName="询问面积";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("做什么","怎么用","怎样","怎么了","怎么判断","怎么区分","方法"));
        intentName="询问方法";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("哪里","什么地方","在哪？","位于哪","哪人","是哪？","那里","哪个城市",
                        "地方","位置","出生地","所在地","那地","地址","地区"));
        intentName="询问地点";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("什么不同","什么变化","演变"));
        intentName="询问不同变化";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("为什么","如何","怎么来","为何","由于","为了什么"));
        intentName="询问原因";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("由什么","组成","构成"));
        intentName="询问组成";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("属于","出自","起源"));
        intentName="询问属于关系";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("原来","简称","别称","原名","名为","叫什么","全称","还称为","名称","前身","又被称作"));
        intentName="询问别名";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("多远"));
        intentName="询问距离";
        generateAIntent(intentName,entities);

        entities=new ArrayList<>(
                Arrays.asList("做什么的","什么职务","什么职位","用于","职责","职务","功效"));
        intentName="询问职务";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("什么样子","什么样的","什么样"));
        intentName="询问模样";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("怎么样？","如何？"));
        intentName="询问评价";
        generateAIntent(intentName,entities);

        entities=new ArrayList<>(
                Arrays.asList("怎么说","译名","日语","西班牙语","英语","英文"));
        intentName="询问译名";
        generateAIntent(intentName,entities);


        entities=new ArrayList<>(
                Arrays.asList("是否有","有没有","吗","能不能","是否"));
        intentName="询问正误";
        generateAIntent(intentName,entities);
    }

    //this file get the questions and the answers of the 1 type.
    public void handleSourceFile(String sourceFile,String outPutFile) throws FileNotFoundException {
        File inputFile=new File(sourceFile);
        Scanner scanner=new Scanner(inputFile);

        File ouFile=new File(outPutFile);
        PrintWriter writer=new PrintWriter(ouFile);

        Pattern pattern=Pattern.compile("\t(.*?)\t(.*)");

        String lastInside="";
        while(scanner.hasNext()){
            String currentLine=scanner.nextLine();
            Character trueFalse=currentLine.charAt(0);
            if(trueFalse.equals('1')){
                Matcher m=pattern.matcher(currentLine);
                while(m.find()){
                    String material=m.group(1);
                    String second=m.group(2);
                    if(!material.equals(lastInside)){
                        writer.print(material+"\t"+second+"\n");
                        lastInside=material;
                    }

                }
            }
        }
        scanner.close();
        writer.close();
    }
}
