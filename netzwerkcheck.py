# network_check.py

import subprocess
from tkinter import Toplevel, Listbox, Button, messagebox, END

def list_connections():
    try:
        # Verwende ss, um aktive Verbindungen aufzulisten (netstat kann alternativ genutzt werden)
        result = subprocess.run(['ss', '-tulpn'], capture_output=True, text=True)
        connections = result.stdout.splitlines()
        return connections
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Abrufen der Verbindungen: {e}")
        return []

def show_network_connections():
    # Fenster für Netzwerkverbindungen
    window = Toplevel()
    window.title("Aktive Netzwerkverbindungen")

    # Listbox zur Anzeige der Verbindungen
    listbox = Listbox(window, width=100, height=20)
    listbox.pack(pady=10)

    # Verbindungen in die Listbox laden
    connections = list_connections()
    for connection in connections:
        listbox.insert(END, connection)

    def close_connection():
        try:
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warnung", "Bitte eine Verbindung auswählen.")
                return

            # Beispiel: PID aus der ausgewählten Zeile extrahieren und Prozess beenden
            selected_line = listbox.get(selection[0])
            pid = extract_pid_from_line(selected_line)
            if pid:
                subprocess.run(['sudo', 'kill', '-9', pid], check=True)
                messagebox.showinfo("Erfolg", f"Verbindung mit PID {pid} beendet.")
                listbox.delete(selection[0])  # Entfernte Verbindung aus der Listbox löschen
            else:
                messagebox.showerror("Fehler", "PID konnte nicht gefunden werden.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Beenden der Verbindung: {e}")

    # Button zum Beenden der ausgewählten Verbindung
    close_button = Button(window, text="Verbindung trennen", command=close_connection)
    close_button.pack(pady=10)

def extract_pid_from_line(line):
    try:
        # Extrahiert die PID aus einer typischen Verbindungsliste (ss -tulpn)
        parts = line.split()
        for part in parts:
            if 'pid=' in part:
                return part.split('=')[1]
        return None
    except IndexError:
        return None
