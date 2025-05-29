# 🧠 Smart File Organizer v6

A professional-grade Python desktop utility built with `tkinter`, designed to **organize**, **clean**, **rename**, and **backup** your files with ease. This version features smart renaming, dark mode toggle, live logs, and ZIP export.

---

## 🚀 Features

| Feature              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| 📂 Add Files         | Select multiple files for organization                                      |
| 🧹 Clear Queue       | Remove all selected files from the queue                                    |
| ✅ Organize Files    | Move and rename files into category folders by type and date                |
| 🔍 Preview Changes   | See where files will go before confirming                                   |
| ♻️ Restore Backup    | Undo file changes and revert to original files                              |
| 🧬 Find Duplicates   | Detect duplicate files using MD5 hashing                                    |
| ⏱️ Auto-Schedule     | Automatically organize files every 10 minutes                               |
| 🧳 Export ZIP        | Export the organized folder as a `.zip` archive                             |
| 🌙 Toggle Dark Mode  | Switch between light and dark GUI themes                                    |
| 📜 Live Logs         | See status updates and actions taken in real-time                          |

---

## 🛠️ Tech Stack

- Python 3
- `tkinter` GUI
- `shutil`, `hashlib`, `datetime`, `schedule`
- Cross-platform (macOS, Windows, Linux via Python)

---

## 📸 Screenshots

### ☀️ Light Mode
![Light Mode](screenshots/light_mode.png)

### 🌑 Dark Mode
![Dark Mode](screenshots/dark_mode.png)

---

## 💾 Installation

1. **Clone the repo**
```bash
git clone https://github.com/Emre-aslan2006/sortFiles.git
cd sortFiles

