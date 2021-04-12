from NodeH import NodeH
from time import time
from typing import List, TextIO
import math

# Nr maxim de noduri din memorie.
max_nodes = 0

# Numarul total de noduri calculate.
total_nodes = 0

# Numarul de noduri din memorie.
nodes_in_memory = 0

# Timpul de inceput al programului.
start_time = 0

def idastar_util(current_state: NodeH, lim: float, euristic: str, file: TextIO):
    """Aici se intampla tot algoritmul.

    Args:
        current_state: starea in care suntem acum
        lim: limita estimarii pana la care putem merge
        euristic: euristica pe care o folosim
        file: fisierul in care afisam raspunsul

    Returns: 
        Un tuplu de 2 elemente. Primul element ne spune daca drumul a ajuns intr-o stare finala, iar al doilea limita.
    """
    global max_nodes, total_nodes, nodes_in_memory, start_time

    # Marim nr de noduri procesate.
    total_nodes += 1

    # Crestem numarul de noduri din memorie si il scadem cand se termina functia.
    nodes_in_memory += 1

    # Actualizam max_nodes.
    max_nodes = max(max_nodes, nodes_in_memory)

    # Daca estimarea nodului curent a depasit limita, oprim algoritmul.
    if current_state.f() > lim:
        nodes_in_memory -= 1
        return False, current_state.f()

    # Daca nodul curent este final, afisam drumul.
    if current_state.final():
        # Cat a durat pana am gasit aceasta solutie
        time_taken = time() - start_time
        file.write("-----------------------------------------\n")
        current_state.print_path(file)
        file.write("Numarul maxim de noduri in memorie a fost: " + str(max_nodes) + "\n")
        file.write("Numarul total de noduri din memorie a fost: " + str(total_nodes) + "\n")
        file.write("A durat: " + str(time_taken) + " secunde.")
        file.write("\n-----------------------------------------\n")
        nodes_in_memory -= 1
        return True, 0

    mn = math.inf
    # Generam urmatoarele stari.
    states = current_state.generate_next(euristic)
    for s in states:
        final, l = idastar_util(s, lim, euristic, file)
        if final:
            nodes_in_memory -= 1
            return True, 0
        mn = min(mn, l)

    # Daca nu mai exista nicio stare urmatoare, iar starea curenta nu e nici finala
    nodes_in_memory -= 1
    return False, mn


def idastar(start_state, out_file_name, n_sol, euristic):
    """Functia care face IDAStar si afiseaza raspunsul in out_file.
    """
    # Fisierul unde vom afisa raspunsul.
    file: typing.TextIO = open(out_file_name, "w")
    start_node = NodeH(start_state, euristic)
    limit = start_node.f()
    drumuri = 0

    # Resetam.
    global max_nodes, total_nodes, start_time
    max_nodes = 0
    total_nodes = 0
    start_time = time()

    while True:
        # Facem un DFS, oprindu-ne cand lungimea drumului ajunge la limit.
        final, lim = idastar_util(start_node, limit, euristic, file)
        if final:
            drumuri += 1
            if drumuri == n_sol:
                break

        # Actualizam limita.
        limit = lim

        # Daca limita e infinit, inseamna ca nu avem solutie.
        if limit == math.inf:
            if drumuri == 0:
                file.write("Nu avem solutie.")
            break

    file.close()
