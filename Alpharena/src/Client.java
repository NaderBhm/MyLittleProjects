import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) {

        try (Socket soc=new Socket("localhost",9806);
             Scanner input = new Scanner(System.in);
             PrintWriter out = new PrintWriter(soc.getOutputStream(),true);
             BufferedReader in =new BufferedReader(new InputStreamReader(soc.getInputStream()))){
            System.out.println("Client started");
            System.out.println("Give me ur username: ");
            String username=input.nextLine();
            out.println(username);
            System.out.println(in.readLine());
            boolean playAgain;
            do{
                String word=in.readLine();
                GameLogic game=new GameLogic(word);
                game.start(input);
                out.println(game.triesPlayed);
                out.println(game.timePlayed);
                String result=in.readLine();
                System.out.println("The winner is : "+result);
                System.out.println(in.readLine());
                String line;
                char toContinue;
                while (true) {
                    line = input.nextLine().trim();
                    if (line.length() == 1 && (line.charAt(0) == '0' || line.charAt(0) == '1')) {
                        toContinue = line.charAt(0);
                        break;
                    }
                    System.out.println("Please enter 1 or 0:");
                }
                out.println(toContinue);
                System.out.println(in.readLine());
                playAgain=Boolean.parseBoolean(in.readLine());
            }while (playAgain);
        }
        catch (Exception e){
            System.err.println("Error during server operation: " + e.getMessage());
            e.printStackTrace();
        }

    }
}
