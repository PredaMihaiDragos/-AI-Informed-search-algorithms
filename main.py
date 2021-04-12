import multiprocessing
import typing

from AStar import astar
from AStarOpt import astaropt
from IDAStar import idastar
from UCS import ucs
from read import read_state


def main():
    # Citim de la tastatura numarul algoritmului pe care il vrem.
    print("Introdu numarul algoritmului:")
    print("1. UCS\n2. A Star\n3. A Star optimizat\n4. IDA Star")
    alg = input()
    if alg != "1" and alg != "2" and alg != "3" and alg != "4":
        print("Numar algoritm <%s> invalid" % alg)
        return

    if alg == "2" or alg == "3" or alg == "4":
        euristics = ["banal", "adm1", "adm2", "neadm"]
        print("Introdu numarul euristicii " + str(euristics) + ": ")
        euristic = input()
        if euristic not in euristics:
            print("Euristica invalida: " + euristic)
            return

    # Citim starile din fisierele de intrare.
    for r in read_state():
        if r is None:
            continue
        start_state, out_file_name, n_sol, timeout_time = r

        # Daca starea initiala nu poate duce la solutie, ne oprim.
        if not start_state.can_be_sol():
            file: typing.TextIO = open(out_file_name, "w")
            file.write("Nu avem solutie.")
            file.close()
            continue

        # Pornim algoritmul ca proces separat pentru a putea avea un timeout.
        if alg == "1":
            p = multiprocessing.Process(target=ucs, args=(start_state, out_file_name, n_sol,))
        elif alg == "2":
            p = multiprocessing.Process(target=astar, args=(start_state, out_file_name, n_sol, euristic,))
        elif alg == "3":
            p = multiprocessing.Process(target=astaropt, args=(start_state, out_file_name, n_sol, euristic,))
        elif alg == "4":
            p = multiprocessing.Process(target=idastar, args=(start_state, out_file_name, n_sol, euristic,))
        p.start()

        # Asteptam timeout_time sau pana termina procesul.
        p.join(timeout_time)

        # Daca procesul nu s-a terminat
        if p.is_alive():
            p.kill()
            p.join()

            file: typing.TextIO = open(out_file_name, "w")
            file.write("TIMEOUT")
            file.close()
    

if __name__ == '__main__':
    main()
