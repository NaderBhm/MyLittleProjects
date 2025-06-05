import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Scanner;

public class GameLogic {
    String word;
    double timePlayed;
    int triesPlayed = 1;

    public GameLogic(String word) {
        this.word = word;
    }

    void start(Scanner input) {
        ArrayList<String> wordlist = new ArrayList<>();
        loadDict(wordlist);
        System.out.println("the game starts!");
        long start = System.currentTimeMillis();
        while (triesPlayed<=6) {
            System.out.println("Enter your try: ");
            String tryWord = "";
            boolean test = true;
            while (test) {
                test = false;
                tryWord = input.nextLine().toLowerCase();
                if (tryWord.length() != word.length()) {
                    System.out.println("give me a word of the same length at least!");
                    test = true;
                } else if (!wordlist.contains(tryWord)) {
                    System.out.println("word is not in my dictionary");
                    test = true;
                }
            }
            String matchup=tryCalculator(tryWord);
            System.out.println(matchup);
            System.out.println(visualMatchup(matchup));
            if (matchup.equals("2".repeat(word.length()))) {
                System.out.println("You guessed the word!");
                long end = System.currentTimeMillis();
                timePlayed = (end - start) / 1000.0;
                break;
            } else {
                triesPlayed++;
            }
        }
        if (triesPlayed >= 6) {
            System.out.println("Game over! Word was: " + word);
        }
    }

    String tryCalculator(String tryWord) {
        StringBuilder result = new StringBuilder("00000");
        boolean[] matchedInWord = new boolean[word.length()];
        boolean[] matchedInTry = new boolean[tryWord.length()];

        for (int i = 0,N=word.length(); i < N; i++) {
            if (tryWord.charAt(i) == word.charAt(i)) {
                result.setCharAt(i, '2');
                matchedInWord[i] = true;
                matchedInTry[i] = true;
            }
        }
        for (int i = 0,N=tryWord.length(); i < N; i++) {
            if (matchedInTry[i]) continue;
            for (int j = 0; j < N; j++) {
                if (!matchedInWord[j] && tryWord.charAt(i) == word.charAt(j)) {
                    result.setCharAt(i, '1');
                    matchedInWord[j] = true;
                    break;
                }
            }
        }

        return result.toString();
    }
    String visualMatchup(String matchup){
        StringBuilder result = new StringBuilder();
        for (int i = 0,N=matchup.length(); i < N; i++) {
            switch (matchup.charAt(i)){
                case '2' ->
                    result.append("\uD83D\uDFE9");

                case '1' ->
                    result.append("\uD83D\uDFE8");

                case '0' ->
                    result.append("\uD83C\uDF2B");

            }
        }
        return result.toString();
    }
    void loadDict(ArrayList<String> wordlist) {
        try (BufferedReader reader = new BufferedReader(new FileReader("5letter.txt"));){
            String line;
            while ((line = reader.readLine()) != null) {
                wordlist.add(line.trim());
            }
        } catch (Exception e) {
            System.err.println("Error during server operation: " + e.getMessage());
            e.printStackTrace();

        }
    }
}