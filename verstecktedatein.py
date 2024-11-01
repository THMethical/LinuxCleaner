import os
from tkinter import Toplevel, Listbox, Button, messagebox

def list_hidden_files():
    # Home-Verzeichnis des Benutzers abrufen
    home_dir = os.path.expanduser("~")
    # Liste der versteckten Dateien abrufen
    hidden_files = [f for f in os.listdir(home_dir) if f.startswith('.') and os.path.isfile(os.path.join(home_dir, f))]
    return hidden_files

def delete_selected_files(selected_files, master):
    home_dir = os.path.expanduser("~")
    errors = []
    for file in selected_files:
        file_path = os.path.join(home_dir, file)
        try:
            os.remove(file_path)
        except Exception as e:
            errors.append(f"Fehler beim Löschen von {file}: {e}")
    if errors:
        messagebox.showerror("Fehler", "\n".join(errors))
    else:
        messagebox.showinfo("Erfolg", "Ausgewählte Dateien wurden gelöscht.")
    master.destroy()  # Fenster schließen nach Löschen

def versteckte_datein_fenster(master):
    # Neues Fenster für die Liste der versteckten Dateien erstellen
    window = Toplevel(master)
    window.title("Versteckte Dateien verwalten")

    # Liste der versteckten Dateien abrufen
    hidden_files = list_hidden_files()

    # Listbox für versteckte Dateien
    listbox = Listbox(window, selectmode="multiple", width=50, height=15)
    listbox.pack(padx=10, pady=10)

    # Dateien zur Listbox hinzufügen
    for file in hidden_files:
        listbox.insert("end", file)

    # Löschen-Button
    delete_button = Button(window, text="Ausgewählte Dateien löschen", command=lambda: delete_selected_files([listbox.get(i) for i in listbox.curselection()], window))
    delete_button.pack(pady=10)
