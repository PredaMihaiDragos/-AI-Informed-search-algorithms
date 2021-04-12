import typing
from time import time

import Node
from NodeH import NodeH


def astar(start_state, out_file_name, n_sol, euristic):
    """Functia care face AStar si afiseaza raspunsul in out_file.
    """
    # Timpul la care incepe executia AStar-ului.
    start_time = time()

    c: [NodeH] = [NodeH(start_state, euristic)]

    # Numarul de drumuri gasit pana acum.
    drumuri = 0

    # Fisierul unde vom afisa raspunsul.
    file: typing.TextIO = open(out_file_name, "w")

    # Nr maxim de noduri din memorie.
    max_nodes = 0

    # Numarul total de noduri calculate.
    total_nodes = 0

    x = 0

    while len(c) > 0:
        current: Node = c.pop(0)

        # Daca am ajuns in nodul destinatie, afisam drumul.
        if current.final():
            # Cat a durat pana am gasit aceasta solutie
            time_taken = time() - start_time
            file.write("-----------------------------------------\n")
            current.print_path(file)
            file.write("Numarul maxim de noduri in memorie a fost: " + str(max_nodes) + "\n")
            file.write("Numarul total de noduri din memorie a fost: " + str(total_nodes) + "\n")
            file.write("A durat: " + str(time_taken) + " secunde.")
            file.write("\n-----------------------------------------\n")
            drumuri += 1
            if drumuri == n_sol:
                break

        # Generam urmatoarele stari.
        states = current.generate_next(euristic)

        # Actualizam total_nodes.
        total_nodes += len(states)

        # Mentinem vectorul ordonat dupa cost, inserand noile stari in locurile corespunzatoare.
        for s in states:
            ind = None
            for i in range(len(c)):
                if c[i].f() > s.f() or (c[i].f() == s.f() and c[i].cost > s.cost):
                    ind = i
                    break
            if ind is not None:
                c.insert(ind, s)
            else:
                c.append(s)

        # Actualizam max_nodes.
        max_nodes = max(max_nodes, len(c))

    if drumuri == 0:
        file.write("Nu avem solutie.")

    file.close()
