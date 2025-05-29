# 🧠 Smart File Organizer v6

A modern Python desktop app that organizes, renames, backs up, and auto-schedules your messy files — now with dark mode, live logs, AI-style renaming patterns, and ZIP export.

![Smart File Organizer](https://user-images.githubusercontent.com/00000000/organizer-screenshot.png) <!-- Replace with your actual screenshot path -->

---

## ⚡ Features

✅ **Smart File Sorting**  
Sorts files into folders like `Images`, `Documents`, `Videos`, `Audio`, `Code`, and more.

✅ **Automatic Renaming**  
Renames files using timestamps and category-aware patterns.

✅ **Live Logs**  
View detailed file actions (moved, renamed, skipped) in real time.

✅ **Preview Mode**  
See what changes will be made before committing.

✅ **Backup + Restore**  
Safely back up and restore files before/after organizing.

✅ **Duplicate Detector**  
Finds exact duplicate files using MD5 hashing.

✅ **Auto-Scheduler**  
Runs every 10 minutes in the background using `schedule`.

✅ **Export as ZIP**  
Exports all organized files into a single ZIP archive.

✅ **Dark Mode**  
Toggle between light/dark modes for the GUI.

---

## 🚀 Tech Stack

- 🐍 Python 3.x
- 🖼️ Tkinter GUI (desktop-native)
- 🧠 `hashlib`, `schedule`, `shutil`, `zipfile`, `threading`, `datetime`
- 📦 `poetry` or `requirements.txt` for dependency management

---

## 🧪 How to Run

### 🔧 Clone & Run Locally

```bash
git clone https://github.com/Emre-aslan2006/sortFiles.git
cd sortFiles
python3 main.py
