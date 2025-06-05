import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Random;

public class Server {
    public static void main(String[] args) {
        try (ServerSocket ss= new ServerSocket(9806)){
            System.out.println("Waiting for player....");
            Socket socP1 =ss.accept();
            System.out.println("Player1 connected");
            BufferedReader inP1 = new BufferedReader(new InputStreamReader(socP1.getInputStream()));
            String usernameP1 = inP1.readLine();
            System.out.println("Username: "+ usernameP1);
            PrintWriter outP1 = new PrintWriter(socP1. getOutputStream(),true);
            outP1.println("You're connected successfully "+ usernameP1);
            Socket socP2 =ss.accept();
            System.out.println("Player2 connected");
            BufferedReader inP2 = new BufferedReader(new InputStreamReader(socP2.getInputStream()));
            String usernameP2 = inP2.readLine();
            System.out.println("Username: "+usernameP2);
            PrintWriter outP2 = new PrintWriter(socP2.getOutputStream(),true);
            outP2.println("You're connected successfully "+ usernameP2);
            ArrayList<String> wordlist = new ArrayList<>();
            BufferedReader reader = new BufferedReader(new FileReader("5letter.txt"));
            String line;
            while ((line = reader.readLine()) != null) {
                wordlist.add(line.trim());
            }
            Random random=new Random();
            boolean toContinue;
            do{
                String word=wordlist.get(random.nextInt(0,wordlist.size()));
                outP1.println(word);
                outP2.println(word);
                int triesPlayedP1;
                try {
                    triesPlayedP1 = Integer.parseInt(inP1.readLine());
                } catch (Exception e) {
                    triesPlayedP1 = 7;
                }
                double timePlayedP1;
                try {
                    timePlayedP1 = Double.parseDouble(inP1.readLine());
                } catch (Exception e) {
                    timePlayedP1 = 999999;
                }
                int triesPlayedP2;
                try {
                    triesPlayedP2 = Integer.parseInt(inP2.readLine());
                } catch (Exception e) {
                    triesPlayedP2 = 7;
                }
                double timePlayedP2;
                try {
                    timePlayedP2 = Double.parseDouble(inP2.readLine());
                } catch (Exception e) {
                    timePlayedP2 = 999999;
                }
                if (triesPlayedP1<triesPlayedP2 || (triesPlayedP1==triesPlayedP2 && timePlayedP1<timePlayedP2)){
                    outP1.println(usernameP1);
                    outP2.println(usernameP1);
                } else if (triesPlayedP1>triesPlayedP2 ||  timePlayedP1>timePlayedP2) {
                    outP1.println(usernameP2);
                    outP2.println(usernameP2);
                }
                else{
                    outP1.println("draw");
                    outP2.println("draw");
                }
                outP1.println("Do you want to play again? (1/0)");
                outP2.println("Do you want to play again? (1/0)");
                char playAgainP1=inP1.readLine().charAt(0);
                char playAgainP2=inP2.readLine().charAt(0);
                if(playAgainP1=='0'){
                    outP1.println("YOU quit the match");
                    outP2.println(usernameP1+" quit the match");
                    toContinue=false;
                } else if (playAgainP2=='0') {
                    outP1.println(usernameP2+" quit the match");
                    outP2.println("YOU quit the match");
                    toContinue=false;
                }
                else {
                    outP1.println("The game Continue!");
                    outP2.println("The game Continue!");
                    toContinue=true;
                }
                outP1.println(toContinue);
                outP2.println(toContinue);
            }while (toContinue);


        }
        catch (Exception e){
            System.err.println("Error during server operation: " + e.getMessage());
            e.printStackTrace();

        }

    }
}
