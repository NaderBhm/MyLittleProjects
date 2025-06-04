import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class Main {
    static Scanner input = new Scanner(System.in);

    static String getWord(){
        Random random = new Random();
        String filepath="words.txt";
        String word="";
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))){
            for(int i=0,N=random.nextInt(0,6641);i<N;i++){
                word=reader.readLine();
            }
            return word;
        }
        catch(FileNotFoundException e){
            System.out.println("File not found");
        }
        catch(IOException e){
            System.out.println("something went wrong");
        }
        return "";
    }

    static char getC(ArrayList<Character> usedC){
        char c=input.next().charAt(0);
        if(!Character.isLetter(c)){
            System.out.println("enter a proper letter please");
        }
        else if (usedC.contains(c)){
            System.out.println("you already tried this letter stupid 🤨");
        }
        else{
            usedC.add(c);
            return c;
        }
        return getC(usedC);
    }

    public static void main(String[] args)  {
        String word = getWord();
        char c;
        int wrongGuess=0;
        ArrayList<Character> usedC= new ArrayList<>();
        ArrayList<Character> status= new ArrayList<>();
        for(int i=0,l=word.length();i<l;i++){
            status.add('-');
        }
        System.out.println("****************************");
        System.out.println(" Welcome to the hangman game");
        System.out.println("****************************");
        while(wrongGuess<7){
            System.out.print("your guess: ");
            c=getC(usedC);
            if(word.contains(Character.toString(c))){
                System.out.println("Correct guess");
                for(int i=0,l=word.length();i<l;i++){
                    if(word.charAt(i)==c) {
                        status.set(i, c);
                    }
                }
                if(!status.contains('-')){
                    System.out.println("Congratulations! You won");
                    System.out.print("The word was : ");
                    wrongGuess=100;
                }
            }
            else{
                System.out.println("wrong guess");
                wrongGuess++;

            }
            for(char p:status){
                System.out.print(p+" ");
            }
            System.out.println();
            System.out.println(getHangmanArt(wrongGuess));

        }
        if(wrongGuess!=100){
            System.out.println("Sorry you lost 😔");
            System.out.println("The word was : "+word);
        }
    }
    static String getHangmanArt(int N){
        switch (N) {
            case 1 -> {
                return """
                          |
                        """;
            }
            case 2 -> {
                return """
                          |
                          0
                        """;
            }
            case 3 -> {
                return """
                          |
                          0
                         /
                        """;
            }
            case 4 -> {
                return """
                          |
                          0
                        / |
                        """;
            }
            case 5 -> {
                return """
                          |
                          0
                        / | \\
                        """;
            }
            case 6 -> {
                return """
                          |
                          0
                        / | \\
                         /
                        """;
            }
            case 7 -> {
                return """
                          |
                          0
                        / | \\
                         / \\
                        """;
            }
            default -> {return "";}
        }
    }
}