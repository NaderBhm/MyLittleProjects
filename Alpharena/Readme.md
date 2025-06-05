# 🔤 Alpharena V1.0

Welcome to **Alpharena** — a multiplayer word-guessing showdown inspired by Wordle, developed entirely in Java using socket programming.

> 🎓 *This was my first major project in Java. As someone new to the language, I faced numerous challenges — especially with networking and input handling. But I truly enjoyed the process and came out of it having learned so much!*

---

## 🕹️ Game Overview

**Alpharena** is a two-player word-guessing game played in real time over a network. Both players connect to a central server, are given the same randomly selected 5-letter word, and race to guess it correctly. The round ends when either the guesses run out (max 6) or the word is guessed.

The winner is determined based on:
- ✅ Fewer number of tries used
- ✅ Faster time to guess (used as a tiebreaker)

After each round, players can choose to continue or exit the game.

---

## ✨ Key Features

- ✅ **Socket-based multiplayer** using `ServerSocket` and `Socket`
- ✅ **Real-time communication** between two players
- ✅ **Dictionary validation** using a local word list (`5letter.txt`)
- ✅ **Visual feedback** for each guess:
  - 🟩 Correct letter in correct position  
  - 🟨 Correct letter in wrong position  
  - ⬜ Incorrect letter  
- ✅ **Automatic winner selection** based on performance
- ✅ **Replay support** to play multiple rounds
- ✅ **Modular codebase** with clean separation of concerns

---

## 📁 Project Structure

📦 Alpharena/
├── Client.java // Player-side logic, UI, and interaction
├── Server.java // Game coordinator, handles both players
├── GameLogic.java // Core word comparison and feedback mechanics
├── 5letter.txt // Dictionary of valid 5-letter words

---

## 🚧 Future Plans

Here’s what I’m planning to build next to take Alpharena to the next level:

- [ ] 🧵 **Multithreaded Server** — allow multiple pairs of players to play simultaneously
- [ ] 🎨 **Graphical UI** — add a user-friendly interface using JavaFX or Swing
- [ ] 🏆 **Leaderboard System** — persist scores and rankings across sessions
- [ ] ⏱️ **Turn Timer** — implement a countdown to add time pressure
- [ ] 🌍 **LAN/Internet Support** — enable remote connections beyond localhost

---

## 💡 What I Learned

This project gave me a hands-on understanding of:

- Java I/O streams and classes (`BufferedReader`, `PrintWriter`, `Scanner`)
- Client-server communication via sockets
- Parsing and validating user input in multiplayer settings
- Designing clean and modular Java programs
- Debugging real-time synchronization and flow logic

---

**🚀 Built with passion by Nader**
