# Smart File Organizer v6 - Live Log, Dark Mode, AI Rename, ZIP Export

import os
import shutil
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import time
import threading
import schedule
import zipfile

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".html", ".css", ".js"]
}

file_queue = []
backup_folder = None
is_dark_mode = False

# Toggle dark/light mode
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    bg = "#2c2f33" if is_dark_mode else "#dcdcdc"
    fg = "white" if is_dark_mode else "black"
    root.config(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.config(bg=bg, fg=fg)
        except:
            pass
    log_text.config(bg="black" if is_dark_mode else "white", fg=fg)

# Pattern-based smart renamer
def smart_name_guess(file_path):
    name = os.path.basename(file_path).lower()
    if "invoice" in name:
        return "Invoice"
    elif "resume" in name or "cv" in name:
        return "Resume"
    elif "report" in name:
        return "Report"
    else:
        return "File"

def get_date_folder(file_path):
    mod_time = os.path.getmtime(file_path)
    dt = datetime.fromtimestamp(mod_time)
    return os.path.join(str(dt.year), dt.strftime("%m_%B"))

def auto_rename(file_path, category_folder):
    ext = os.path.splitext(file_path)[1]
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    prefix = smart_name_guess(file_path)
    new_name = f"{prefix}_{timestamp}_{str(int(time.time() * 1000)[-4:])}{ext}"
    return os.path.join(category_folder, new_name)

def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)

def organize_folder(preview=False):
    if not file_queue:
        messagebox.showerror("Error", "No files selected.")
        return

    actions = []
    global backup_folder
    folder_path = os.path.dirname(file_queue[0])

    if not preview:
        backup_folder = os.path.join(folder_path, "_backup")
        os.makedirs(backup_folder, exist_ok=True)
        for f in file_queue:
            shutil.copy2(f, os.path.join(backup_folder, os.path.basename(f)))

    for file_path in file_queue:
        if not os.path.isfile(file_path):
            continue

        filename = os.path.basename(file_path)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        moved = False

        for category, extensions in categories.items():
            if ext in extensions:
                date_folder = get_date_folder(file_path)
                dest_folder = os.path.join(folder_path, category, date_folder)
                os.makedirs(dest_folder, exist_ok=True)
                renamed_path = auto_rename(file_path, dest_folder)
                if preview:
                    actions.append(f"[PREVIEW] {filename} → {renamed_path}")
                else:
                    shutil.move(file_path, renamed_path)
                    actions.append(f"Moved + Renamed {filename} → {renamed_path}")
                moved = True
                break

        if not moved:
            other_folder = os.path.join(folder_path, "Others")
            os.makedirs(other_folder, exist_ok=True)
            renamed_path = auto_rename(file_path, other_folder)
            if preview:
                actions.append(f"[PREVIEW] {filename} → {renamed_path}")
            else:
                shutil.move(file_path, renamed_path)
                actions.append(f"Moved + Renamed {filename} → {renamed_path}")

    if not actions:
        msg = "⚠️ No actionable files found for preview."
    else:
        msg = "\n".join(actions[:20]) + ("\n...and more" if len(actions) > 20 else "")

    log(msg)
    messagebox.showinfo("Preview" if preview else "Organized", msg)
    update_status()

def restore_backup():
    global backup_folder
    if not backup_folder or not os.path.exists(backup_folder):
        messagebox.showerror("Error", "No backup found.")
        return

    folder_path = os.path.dirname(backup_folder)
    for file in os.listdir(backup_folder):
        shutil.move(os.path.join(backup_folder, file), os.path.join(folder_path, file))
    shutil.rmtree(backup_folder)
    for category in list(categories.keys()) + ["Others"]:
        cat_path = os.path.join(folder_path, category)
        if os.path.exists(cat_path):
            shutil.rmtree(cat_path)
    log("✅ Restored original state.")
    messagebox.showinfo("Restored", "🔁 Files restored to original state.")
    update_status()

def find_duplicates():
    if not file_queue:
        messagebox.showerror("Error", "No files in queue.")
        return
    hashes = {}
    duplicates = []
    for file_path in file_queue:
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash in hashes:
                duplicates.append(os.path.basename(file_path))
            else:
                hashes[file_hash] = file_path
        except:
            continue
    if duplicates:
        msg = "\n".join(duplicates)
        log(f"⚠️ Duplicates Found:\n{msg}")
        messagebox.showinfo("🔁 Duplicates Found", msg)
    else:
        log("✅ No duplicates found.")
        messagebox.showinfo("✅ No Duplicates", "No duplicate files in selection.")

def add_files():
    files = filedialog.askopenfilenames()
    for file in files:
        if file not in file_queue:
            file_queue.append(file)
            file_listbox.insert(tk.END, file)
    update_status()

def clear_queue():
    file_queue.clear()
    file_listbox.delete(0, tk.END)
    update_status()

def update_status():
    status_label.config(text=f"🧾 {len(file_queue)} file{'s' if len(file_queue) != 1 else ''} in queue")

def export_zip():
    if not file_queue:
        messagebox.showerror("Error", "No files to zip.")
        return
    zip_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
    if not zip_path:
        return
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in file_queue:
            zipf.write(file, os.path.basename(file))
    log(f"📦 Exported zip: {zip_path}")
    messagebox.showinfo("Exported", f"📦 Exported zip: {zip_path}")

def auto_organize_job():
    if file_queue:
        organize_folder(preview=False)
    else:
        log("⏳ Scheduler: No files in queue.")

def run_scheduler():
    schedule.every(10).minutes.do(auto_organize_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_auto_scheduler():
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    messagebox.showinfo("Scheduler Started", "⏱️ Auto-organizer will run every 10 minutes.")

root = TkinterDnD.Tk() if DND_AVAILABLE else tk.Tk()
root.title("🧠 Smart File Organizer v6")
root.geometry("700x700")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="🎯 Select Files to Organize:", font=("Arial", 13)).pack()
tk.Button(frame, text="➕ Add Files", command=add_files, bg="#ffc107", font=("Arial", 11)).pack(pady=2)
tk.Button(frame, text="🗑️ Clear Queue", command=clear_queue, bg="#343a40", fg="white", font=("Arial", 11)).pack(pady=2)
file_listbox = tk.Listbox(root, height=8, width=80)
file_listbox.pack(pady=10)

if DND_AVAILABLE:
    def on_drop(event):
        files = root.tk.splitlist(event.data)
        for file in files:
            if os.path.isfile(file) and file not in file_queue:
                file_queue.append(file)
                file_listbox.insert(tk.END, file)
        update_status()
    file_listbox.drop_target_register(DND_FILES)
    file_listbox.dnd_bind('<<Drop>>', on_drop)
    tk.Label(root, text="📂 You can also drag & drop files here", font=("Arial", 10), fg="gray").pack()
else:
    tk.Label(root, text="⚠️ Drag-and-drop not available (tkinterDnD2 not installed)", font=("Arial", 10), fg="red").pack()

tk.Button(root, text="✅ Organize Files", command=lambda: organize_folder(preview=False),
          bg="#007bff", fg="white", font=("Arial", 13)).pack(pady=4)
tk.Button(root, text="🔍 Preview Changes", command=lambda: organize_folder(preview=True),
          bg="#6c757d", fg="white", font=("Arial", 13)).pack(pady=2)
tk.Button(root, text="♻️ Restore Backup", command=restore_backup,
          bg="#dc3545", fg="white", font=("Arial", 11)).pack(pady=4)
tk.Button(root, text="🧬 Find Duplicates", command=find_duplicates,
          bg="#28a745", fg="white", font=("Arial", 11)).pack(pady=2)
tk.Button(root, text="⏱️ Enable Auto-Schedule", command=start_auto_scheduler,
          bg="#17a2b8", fg="white", font=("Arial", 11)).pack(pady=4)
tk.Button(root, text="📦 Export ZIP", command=export_zip,
          bg="#6610f2", fg="white", font=("Arial", 11)).pack(pady=4)
tk.Button(root, text="🌓 Toggle Dark Mode", command=toggle_theme,
          bg="#adb5bd", font=("Arial", 11)).pack(pady=3)

status_label = tk.Label(root, text="🧾 0 files in queue", font=("Arial", 10), fg="black")
status_label.pack(pady=5)

log_text = tk.Text(root, height=8, width=80)
log_text.pack(pady=10)

root.mainloop()
