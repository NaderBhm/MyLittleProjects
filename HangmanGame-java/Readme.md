# Hangman Game in Java 🎯

This is a simple **Hangman game** implemented in **Java** as part of my journey learning the language.  
The game randomly selects a word from a text file and challenges the player to guess it letter by letter before the hangman is fully drawn.

## 📂 Files

- `Main.java`: The main game logic.
- `words.txt`: A list of words (one per line) used for the game.

## 🎮 How to Play

1. Run the `Main.java` file.
2. The program will pick a random word from `words.txt`.
3. You guess letters, and the game will reveal correct guesses.
4. You have **7 wrong guesses** before you lose the game.

## ✅ Features

- Input validation (only accepts letters, warns about repeated guesses).
- Hangman drawing ASCII art updates as the game progresses.
- Simple recursive input handling for clean logic.

## 🛠 Requirements

- Java 17 or later
- `words.txt` file with at least 6641 words (or adjust the code if you use a smaller word list)

## 🧠 Notes

- This is a **learning project**—I'm currently exploring Java as a new language!
- Feel free play around or suggest improvements.
