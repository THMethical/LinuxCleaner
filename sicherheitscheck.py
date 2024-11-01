import subprocess
import tkinter as tk

def sicherheitscheckfensterle(master):
    security_window = tk.Toplevel(master)
    security_window.title("Sicherheitsüberprüfung")

    label = tk.Label(security_window, text="System wird auf Sicherheitsprobleme überprüft...", justify=tk.LEFT)
    label.pack(pady=5)

    check_button = tk.Button(security_window, text="Sicherheitsüberprüfung starten", command=lambda: run_security_checks(security_window))
    check_button.pack(pady=10)

def run_security_checks(window):
    output_text = tk.Text(window, height=15, width=50)
    output_text.pack(pady=5)

    # Überprüfung auf veraltete Pakete
    output_text.insert(tk.END, "Überprüfung auf veraltete Pakete...\n")
    outdated_packages = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True)
    output_text.insert(tk.END, outdated_packages.stdout if outdated_packages.stdout else "Keine veralteten Pakete gefunden.\n")

    # Überprüfung auf schwache Passwörter
    output_text.insert(tk.END, "\nÜberprüfung auf leere oder Standardpasswörter...\n")
    try:
        weak_passwords = subprocess.run(['sudo', 'grep', '::', '/etc/shadow'], capture_output=True, text=True)
        output_text.insert(tk.END, weak_passwords.stdout if weak_passwords.stdout else "Keine schwachen Passwörter gefunden.\n")
    except Exception as e:
        output_text.insert(tk.END, f"Fehler bei der Passwortüberprüfung: {e}\n")
    
    output_text.insert(tk.END, "\nSicherheitsüberprüfung abgeschlossen.\n")
