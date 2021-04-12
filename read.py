import sys
import os
from typing import List, TextIO
from Node import Node

def is_valid_state(state: List[List[str]]) -> bool:
    """Verifica daca o stare este valida sau nu.

    Args:
        state: starea de verificat, o matrice

    Returns:
        True daca este valida si False altfel.
    """

    # Verificam sa nu fie matricea goala.
    if len(state) == 0:
        return False
    if len(state[0]) == 0:
        return False

    for line in state:
        # Verificam daca toate liniile au aceeasi lungime.
        if len(line) != len(state[0]):
            return False

        for char in line:
            # Verificam ca toate caracterele sa fie litere intre 'a' si 'z'.
            if char != '#' and (char > 'z' or char < 'a'):
                return False

    # Toate conditiile au fost indeplinite, returnam True.
    return True

def read_state():
    """Citeste si returneaza: 
        urmatoarea stare de procesat din fisierele de input, fisierul de output, numarul de solutii cerute si timpul de timeout.

    Returns:
        Daca mai avem stari de procesat si argumentele din terminal sunt bune, 
            returneaza starea, fisierul unde va trebui sa se gaseasca output-ul si numarul de solutii cerute si timpul de timeout.
        Altfel, returneaza None

    Raises:
        ValueError: Daca vreo stare din fisier nu e valida.
    """

    # Citim argumentele.
    try:
        in_folder_name: str = sys.argv[1]
        out_folder_name: str = sys.argv[2]
        n_sol: int = int(sys.argv[3])
        timeout_time: float = float(sys.argv[4])
    except:
        # Daca argumentele nu sunt bune, afisam o eroare si cum ar trebui apelat.
        print("Argumentele nu sunt bune.")
        print("Exemplu: python3 UCS.py [nume_folder_input] [nume_folder_output] [n_sol] [timeout_time]")
        raise ValueError("Argumentele nu sunt bune. Exemplu: python3 main.py [nume_folder_input] [nume_folder_output] [n_sol] [timeout_time]")

    # Verificam ca folderele de intrare si de iesire sa existe.
    if not os.path.isdir(in_folder_name):
        raise ValueError("Folderul <%s> nu exista" % in_folder_name)
    if not os.path.isdir(out_folder_name):
        raise ValueError("Folderul <%s> nu exista" % out_folder_name)

    # Luam fiecare fisier din folderul de intrare.
    for in_file_name in os.listdir(in_folder_name):
        out_file_name = os.path.join(out_folder_name, in_file_name)
        in_file_name = os.path.join(in_folder_name, in_file_name)

        in_file: TextIO = open(in_file_name, "r")

        # Citim fisierul de intrare.
        initial_state = in_file.read().splitlines()

        # Convert string to list of characters.
        initial_state = [[c for c in line] for line in initial_state]

        # Verificam ca starea citita sa fie valida.
        if not is_valid_state(initial_state):
            in_file.close()
            print("Starea citita din fisierul <%s> nu este valida." % in_file_name)
            yield None
        else:
            yield (Node(initial_state, 0, None), out_file_name, n_sol, timeout_time)

        in_file.close()
