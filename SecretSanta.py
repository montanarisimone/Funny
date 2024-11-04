import random
import time
import os
import sys
from colorama import init, Fore, Back, Style
import pygame

# Inizializza colorama
init()

# Inizializza pygame per la musica
pygame.init()
pygame.mixer.init()

def play_background_music():
    """Avvia la riproduzione della musica di sottofondo"""
    try:
        pygame.mixer.music.load("christmas_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print_centered("\nFile musicale non trovato. Il programma continuerà senza musica.", Fore.YELLOW)
        time.sleep(2)

def stop_background_music():
    """Ferma la riproduzione della musica"""
    pygame.mixer.music.stop()

def clear_screen():
    """Pulisce lo schermo in modo compatibile con diversi sistemi operativi"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_snow_border():
    """Stampa una cornice di neve"""
    width = os.get_terminal_size().columns
    snowflakes = ['❄', '❅', '❆']
    border = ''
    for _ in range(width):
        border += random.choice(snowflakes)
    print(Fore.CYAN + border + Style.RESET_ALL)

def print_centered(text, color=Fore.WHITE):
    """Stampa il testo centrato con il colore specificato"""
    terminal_width = os.get_terminal_size().columns
    print(color + text.center(terminal_width) + Style.RESET_ALL)

def print_participants_list(partecipanti):
    """Stampa la lista dei partecipanti"""
    print_centered("\nPartecipanti:", Fore.YELLOW)
    for p in partecipanti:
        print_centered(f"🎄 {p}", Fore.CYAN)
    print()

def print_decorative_box(text, color=Fore.WHITE):
    """Stampa il testo in un box decorativo"""
    terminal_width = os.get_terminal_size().columns
    box_width = len(text) + 8
    padding = (terminal_width - box_width) // 2
    
    print('\n' + ' ' * padding + color + '╔' + '═' * (box_width-2) + '╗' + Style.RESET_ALL)
    print(' ' * padding + color + '║' + ' ' * ((box_width-2-len(text))//2) + text + 
          ' ' * ((box_width-2-len(text)+1)//2) + '║' + Style.RESET_ALL)
    print(' ' * padding + color + '╚' + '═' * (box_width-2) + '╝' + Style.RESET_ALL)

def initialize_secret_santa():
    """Inizializza la lista dei partecipanti"""
    partecipanti = []
    while True:
        clear_screen()
        print_snow_border()
        print_centered("\n🎄 Secret Santa - Configurazione 🎄", Fore.GREEN)
        print_snow_border()
        
        if partecipanti:
            print_participants_list(partecipanti)
        
        nome = input(Fore.GREEN + "Inserisci il nome di un partecipante (o premi invio per terminare): " + 
                    Style.RESET_ALL).strip()
        
        if nome == "":
            if len(partecipanti) < 2:
                print_centered("\nServono almeno 2 partecipanti!", Fore.RED)
                input("\nPremi invio per continuare...")
                continue
            break
        if nome not in partecipanti:
            partecipanti.append(nome)
            print_centered(f"\n✨ {nome} aggiunto alla lista! ✨", Fore.YELLOW)
        else:
            print_centered("\nQuesto nome è già stato inserito!", Fore.RED)
        time.sleep(1)
    return partecipanti

def check_valid_assignments(assegnazioni, partecipanti):
    """Verifica se le assegnazioni sono valide"""
    for estrattore in partecipanti:
        # Se l'estrattore non ha ancora estratto, continua
        if estrattore not in assegnazioni:
            continue
        # Se l'estrattore ha estratto se stesso, non valido
        if assegnazioni[estrattore] == estrattore:
            return False
    return True

def reset_assignments_if_needed(partecipanti, assegnazioni, nome_estrattore):
    """
    Controlla se le assegnazioni attuali porterebbero a una situazione impossibile
    e resetta le assegnazioni se necessario
    """
    # Crea una copia delle assegnazioni per la simulazione
    assegnazioni_simulate = assegnazioni.copy()
    partecipanti_rimasti = [p for p in partecipanti if p not in assegnazioni.values()]
    
    # Se siamo all'ultima estrazione e l'unica persona rimasta è l'estrattore
    if len(partecipanti_rimasti) == 1 and partecipanti_rimasti[0] == nome_estrattore:
        print_centered("\n⚠️ Rilevata situazione di stallo, rimescolo le assegnazioni...", Fore.YELLOW)
        time.sleep(2)
        return {}  # Resetta le assegnazioni
    
    return assegnazioni

def estrai_nome(partecipanti, assegnazioni, nome_estrattore):
    """Estrae un nome dalla lista dei partecipanti"""
    clear_screen()
    print_snow_border()
    print_centered("\n🎁 Estrazione Secret Santa 🎁", Fore.GREEN)
    print_snow_border()
    
    print_participants_list(partecipanti)
    
    if not nome_estrattore:
        nome_estrattore = input(Fore.GREEN + "Chi sta estraendo? " + Style.RESET_ALL).strip()
    
    if nome_estrattore not in partecipanti:
        print_centered("\nNome non trovato nella lista dei partecipanti!", Fore.RED)
        input("\nPremi invio per continuare...")
        return None, None
    
    if nome_estrattore in assegnazioni:
        print_centered("\nHai già estratto un nome!", Fore.RED)
        input("\nPremi invio per continuare...")
        return None, None
    
    # Reset delle assegnazioni se necessario
    assegnazioni = reset_assignments_if_needed(partecipanti, assegnazioni, nome_estrattore)
    
    nomi_disponibili = [nome for nome in partecipanti 
                       if nome != nome_estrattore and nome not in assegnazioni.values()]
    
    if not nomi_disponibili:
        return None, None
    
    print_centered("\nEstrazione in corso...", Fore.YELLOW)
    for _ in range(3):
        print_centered("🎲", Fore.CYAN)
        time.sleep(0.5)
    
    nome_estratto = random.choice(nomi_disponibili)
    clear_screen()
    print_snow_border()
    print_decorative_box(f"✨ {nome_estrattore}, hai estratto: {nome_estratto} ✨", Fore.YELLOW)
    print_snow_border()
    
    time.sleep(8)
    clear_screen()
    
    return nome_estrattore, nome_estratto

def main():
    clear_screen()
    print_snow_border()
    print_centered("🎄 Benvenuto al Secret Santa Digitale! 🎄", Fore.GREEN)
    print_snow_border()
    
    play_background_music()
    
    time.sleep(2)
    
    try:
        partecipanti = initialize_secret_santa()
        assegnazioni = {}
        
        while len(assegnazioni) < len(partecipanti):
            clear_screen()
            print_snow_border()
            print_centered(f"\n🎄 Secret Santa - Estrazioni 🎄", Fore.GREEN)
            print_snow_border()
            print_participants_list(partecipanti)
            
            # Se siamo all'ultima estrazione, determiniamo automaticamente chi deve estrarre
            if len(assegnazioni) == len(partecipanti) - 1:
                ultimo_estrattore = [p for p in partecipanti if p not in assegnazioni.keys()][0]
                estrattore, estratto = estrai_nome(partecipanti, assegnazioni, ultimo_estrattore)
            else:
                estrattore, estratto = estrai_nome(partecipanti, assegnazioni, None)
            
            if estrattore and estratto:
                assegnazioni[estrattore] = estratto
            
            input(Fore.CYAN + "\nPremi invio per continuare..." + Style.RESET_ALL)
            
            # Se tutte le assegnazioni sono state fatte ma non sono valide, ricomincia
            if len(assegnazioni) == len(partecipanti) and not check_valid_assignments(assegnazioni, partecipanti):
                print_centered("\n⚠️ Rilevato problema nelle assegnazioni, ricominciamo...", Fore.YELLOW)
                time.sleep(2)
                assegnazioni = {}
        
        clear_screen()
        print_snow_border()
        print_centered("\n🎉 Tutte le estrazioni sono state completate! 🎉", Fore.GREEN)
        print_centered("🎄 Buon Secret Santa! 🎁", Fore.RED)
        print_snow_border()
        time.sleep(3)
    
    finally:
        stop_background_music()
        pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop_background_music()
        pygame.quit()
        print("\nProgramma terminato.")
        sys.exit(0)
