#!/opt/homebrew/bin/python3

import subprocess
import time
import threading
import signal
import sys

def start_caffeinate():
    """Lance un processus macOS qui empêche la veille (équivalent d’un signal HDMI actif)."""
    global CAFFEINATE_PROC
    if CAFFEINATE_PROC is None:
        CAFFEINATE_PROC = subprocess.Popen(["caffeinate", "-dimsu"])
        print("🔁 Processus caffeinate lancé pour garder le système éveillé.")

def stop_caffeinate():
    """Arrête le processus caffeinate."""
    global CAFFEINATE_PROC
    if CAFFEINATE_PROC is not None:
        CAFFEINATE_PROC.terminate()
        CAFFEINATE_PROC.wait()
        CAFFEINATE_PROC = None
        print("💤 Processus caffeinate arrêté.")

def periodic_refresh(DEBUG=False):
    """Envoie périodiquement une petite activité pour simuler un signal HDMI vivant."""
    while True:
        time.sleep(30)
        # On exécute une commande anodine pour provoquer une activité système
        subprocess.run(["/usr/bin/true"])
        if DEBUG:
            print("🔁 HDMI keep-alive : signal simulé.")

def signal_handler(sig, frame):
    stop_caffeinate()
    print("\n⛔️ Simulation HDMI arrêtée proprement.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    DEBUG = False
    CAFFEINATE_PROC = None

    print("🚀 Démarrage du simulateur HDMI pour MacOS…")
    start_caffeinate()
    threading.Thread(target=periodic_refresh(DEBUG), daemon=True).start()

    print("💡 Simulation active. Appuie sur Ctrl+C pour quitter.")
    while True:
        time.sleep(60)

