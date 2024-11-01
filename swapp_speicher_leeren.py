# swap_reset.py

import subprocess
from tkinter import messagebox

def reset_swap():
    try:
        # Swap-Speicher deaktivieren und wieder aktivieren
        subprocess.run(['sudo', 'swapoff', '-a'], check=True)
        subprocess.run(['sudo', 'swapon', '-a'], check=True)
        messagebox.showinfo("Erfolg", "Swap-Speicher wurde zurückgesetzt.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Zurücksetzen des Swap-Speichers: {e}")
