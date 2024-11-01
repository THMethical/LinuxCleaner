import subprocess
import os
from tkinter import filedialog, messagebox

def shred_file(master):
    # Öffnet ein Dialogfenster zur Dateiauswahl
    file_path = filedialog.askopenfilename(title="Wähle eine Datei zum sicheren Löschen aus")
    if not file_path:
        return  # Abbrechen, wenn keine Datei ausgewählt wurde
    
    # Bestätigungsnachricht
    confirm = messagebox.askyesno("Bestätigung", f"Bist du sicher, dass du die Datei '{os.path.basename(file_path)}' sicher löschen möchtest? Diese Aktion kann nicht rückgängig gemacht werden.")
    if not confirm:
        return

    try:
        # Sichere Datei löschen mit shred
        subprocess.run(['sudo', 'shred', '-u', '-v', file_path], check=True)
        messagebox.showinfo("Erfolg", "Die Datei wurde sicher gelöscht.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim sicheren Löschen der Datei: {e}")

def shred_folder(master):
    # Öffnet ein Dialogfenster zur Ordnerauswahl
    folder_path = filedialog.askdirectory(title="Wähle einen Ordner zum sicheren Löschen aus")
    if not folder_path:
        return  # Abbrechen, wenn kein Ordner ausgewählt wurde

    # Bestätigungsnachricht
    confirm = messagebox.askyesno("Bestätigung", f"Bist du sicher, dass du den Ordner '{os.path.basename(folder_path)}' sicher löschen möchtest? Diese Aktion kann nicht rückgängig gemacht werden.")
    if not confirm:
        return

    try:
        # Alle Dateien im Ordner sicher löschen
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                subprocess.run(['sudo', 'shred', '-u', '-v', file_path], check=True)
            # Löschen der leeren Ordner
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(folder_path)  # Löschen des Hauptordners
        messagebox.showinfo("Erfolg", "Der Ordner und alle enthaltenen Dateien wurden sicher gelöscht.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim sicheren Löschen des Ordners: {e}")
