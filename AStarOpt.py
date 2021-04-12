from NodeH import NodeH
from time import time
from typing import List

def astaropt(start_state, out_file_name, n_sol, euristic):
    """Functia care face AStar Optimizat si afiseaza raspunsul in out_file.
    """
    # Timpul la care incepe executia AStar-ului.
    start_time = time()

    closed_list: [NodeH] = []
    open_list: [NodeH] = [NodeH(start_state, euristic)]

    # Numarul de drumuri gasit pana acum.
    drumuri = 0

    # Fisierul unde vom afisa raspunsul.
    file: typing.TextIO = open(out_file_name, "w")

    # Nr maxim de noduri din memorie.
    max_nodes = 0

    # Numarul total de noduri calculate.
    total_nodes = 0

    while (len(open_list) > 0):
        current: Node = open_list.pop(0)
        closed_list.append(current)

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

            # Daca am gasit o solutie, ne oprim in cazul AStarOpt.
            drumuri += 1
            break

        # Generam urmatoarele stari.
        states = current.generate_next(euristic)

        # Actualizam total_nodes.
        total_nodes += len(states)

        def contains(lst: List[NodeH], state) -> bool:
            """Returneaza true daca list contine starea state, false altfel
            """
            for s in lst:
                if s.info == state.info:
                    return False
            return True

        # Mentinem vectorul ordonat dupa cost, inserand noile stari in locurile corespunzatoare.
        for s in states:
            contained = False
            # Cautam starea s in open_list.
            for i in range(len(open_list)):
                if open_list[i].info == s.info:
                    contained = True
                    ind = None
                    if open_list[i].f() > s.f():
                        open_list.pop(i)
                        ind = i
                    for i in range(len(open_list)):
                        if open_list[i].f() > s.f() or (open_list[i].f() == s.f() and open_list[i].cost > s.cost):
                            ind = i
                            break
                    if ind is not None:
                        open_list.insert(ind, s)
                    else:
                        open_list.append(s)
                    break
                    
            # Cautam starea s in closed_list.
            for i in range(len(closed_list)):
                if closed_list[i].info == s.info:
                    contained = True
                    if closed_list[i].f() > s.f():
                        closed_list.pop(i)
                        closed_list.append(s)
                        break

            # Daca starea este deja in open_list sau closed_list, trecem peste.
            if contained:
                continue
    
            # Daca nu este in niciuna din cele 2 stari, o inseram in open_list.
            ind = None 
            for i in range(len(open_list)):
                if open_list[i].f() > s.f() or (open_list[i].f() == s.f() and open_list[i].cost > s.cost):
                    ind = i
                    break
            if ind is not None:
                open_list.insert(ind, s)
            else:
                open_list.append(s)

        # Actualizam max_nodes.
        max_nodes = max(max_nodes, len(open_list) + len(closed_list))

    if drumuri == 0:
        file.write("Nu avem solutie.")

    file.close()
