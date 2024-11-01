import subprocess
import os
import tkinter as tk
from tkinter import messagebox, ttk
import psutil
from sicherheitscheck import sicherheitscheckfensterle
from dateischredder import shred_file, shred_folder
from verstecktedatein import versteckte_datein_fenster
from swapp_speicher_leeren import reset_swap
from netzwerkcheck import show_network_connections
from tkinter import font as tkFont

class LinuxCleaner:
    def __init__(self, master):
        self.master = master
        self.master.title("Linux Cleaner")
        self.master.configure(bg="#2E2E2E")
        self.master.geometry("600x500")

        # Statusleiste
        self.status = tk.StringVar(value="Bereit")
        self.status_bar = tk.Label(master, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Header Label
        header = tk.Label(master, text="Linux Cleaner", font=("Helvetica", 18, 'bold'), bg="#2E2E2E", fg="#FFFFFF")
        header.pack(pady=20)

        # Notebook für Tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10, expand=True, fill='both')

        # Tabs erstellen
        self.cleaning_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cleaning_tab, text="Systemreinigung")

        self.file_management_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_management_tab, text="Dateiverwaltung")

        self.network_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.network_tab, text="Netzwerk")

        # Funktionen in den Tabs hinzufügen
        self.create_cleaning_frame()
        self.create_file_management_frame()
        self.create_network_frame()

    def create_cleaning_frame(self):
        frame = tk.Frame(self.cleaning_tab, bg="#2E2E2E")
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        cleaning_options = [
            ("🧹 Temporäre Dateien bereinigen", self.clean_temp),
            ("🗄️ Paketcache bereinigen", self.clean_cache),
            ("🚮 Verwaiste Pakete entfernen", self.remove_orphans),
            ("🗑️ Log-Dateien bereinigen", self.clean_logs),
            ("🌐 Browser-Cache bereinigen", self.clean_browser_cache),
            ("🔄 Veraltete Pakete aktualisieren", self.update_packages),
            ("🔍 Doppelte Dateien finden", self.find_duplicates),
            ("📊 Systeminformationen anzeigen", self.show_system_info),
            ("🛡️ Sicherheitsüberprüfung", lambda: sicherheitscheckfensterle(self.master)),
        ]

        for text, command in cleaning_options:
            self.create_button(frame, text, command)

    def create_file_management_frame(self):
        frame = tk.Frame(self.file_management_tab, bg="#2E2E2E")
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        file_management_options = [
            ("🗃️ Datei sicher löschen", lambda: shred_file(self.master)),
            ("🗂️ Ordner sicher löschen", lambda: shred_folder(self.master)),
            ("🔒 Versteckte Dateien verwalten", lambda: versteckte_datein_fenster(self.master)),
            ("♻️ Swap-Speicher zurücksetzen", reset_swap),
        ]

        for text, command in file_management_options:
            self.create_button(frame, text, command)

    def create_network_frame(self):
        frame = tk.Frame(self.network_tab, bg="#2E2E2E")
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        network_options = [
            ("🌐 Netzwerkverbindungen prüfen", show_network_connections),
        ]

        for text, command in network_options:
            self.create_button(frame, text, command)

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command, bg="#4CAF50", fg="white", font=("Helvetica", 12), padx=10, pady=5)
        button.pack(pady=5, fill=tk.X)

    def clean_temp(self):
        self.run_command(['sudo', 'rm', '-rf', '/tmp/*'], "Temporäre Dateien wurden bereinigt.", "Fehler beim Bereinigen der temporären Dateien.")
        
    def clean_cache(self):
        self.run_command(['sudo', 'apt', 'clean'], "Paketcache wurde bereinigt.", "Fehler beim Bereinigen des Paketcaches.")
        
    def remove_orphans(self):
        self.run_command(['sudo', 'apt', 'autoremove'], "Verwaiste Pakete wurden entfernt.", "Fehler beim Entfernen verwaister Pakete.")
        
    def clean_logs(self):
        try:
            subprocess.run(['sudo', 'journalctl', '--vacuum-time=7d'], check=True)
            subprocess.run(['sudo', 'truncate', '-s', '0', '/var/log/syslog'], check=True)
            subprocess.run(['sudo', 'truncate', '-s', '0', '/var/log/messages'], check=True)
            subprocess.run(['sudo', 'truncate', '-s', '0', '/var/log/auth.log'], check=True)
            messagebox.showinfo("Erfolg", "Log-Dateien wurden bereinigt.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Bereinigen der Log-Dateien: {e}")

    def clean_browser_cache(self):
        try:
            subprocess.run(['rm', '-rf', os.path.expanduser('~/.cache/mozilla/firefox/*')], check=True)
            messagebox.showinfo("Erfolg", "Browser-Cache wurde bereinigt.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Bereinigen des Browser-Caches: {e}")

    def update_packages(self):
        self.run_command(['sudo', 'apt', 'update'], "Veraltete Pakete wurden aktualisiert.", "Fehler beim Aktualisieren der Pakete.")
        self.run_command(['sudo', 'apt', 'upgrade', '-y'], "Veraltete Pakete wurden aktualisiert.", "Fehler beim Aktualisieren der Pakete.")
        
    def find_duplicates(self):
        try:
            subprocess.run(['fdupes', '-r', os.path.expanduser('/home/USERNAME')], check=True)
            messagebox.showinfo("Erfolg", "Doppelte Dateien wurden gefunden (Überprüfen Sie die Konsole).")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Finden doppelter Dateien: {e}")

    def show_system_info(self):
        info_window = tk.Toplevel(self.master)
        info_window.title("Systeminformationen")
        info_window.configure(bg="#2E2E2E")

        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Hole die Liste der laufenden Prozesse
        processes = [p.info for p in psutil.process_iter(['pid', 'name'])]

        # Erstelle einen Textbereich zur Anzeige der Informationen
        info_text = f"CPU-Auslastung: {cpu_usage}%\n"
        info_text += f"RAM-Nutzung: {ram_usage}%\n"
        info_text += f"Festplattenspeicher-Nutzung: {disk_usage}%\n\n"
        info_text += "Laufende Prozesse:\n"
        info_text += "\n".join([f"PID: {p['pid']}, Name: {p['name']}" for p in processes])

        # Label zur Anzeige der Informationen
        info_label = tk.Label(info_window, text=info_text, justify=tk.LEFT, bg="#2E2E2E", fg="#FFFFFF")
        info_label.pack(padx=10, pady=10)

    def run_command(self, command, success_message, error_message):
        try:
            subprocess.run(command, check=True)
            self.status.set(success_message)
            messagebox.showinfo("Erfolg", success_message)
        except subprocess.CalledProcessError:
            self.status.set(error_message)
            messagebox.showerror("Fehler", error_message)


    

if __name__ == "__main__":
    root = tk.Tk()
    app = LinuxCleaner(root)
    root.mainloop()
