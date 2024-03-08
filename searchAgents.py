from problems import PacmanProblem
import copy
import time
from queue import Queue, PriorityQueue

class searchAgents:
    def UCS(self, g: PacmanProblem) -> list:
        frontier = Queue()
        initial_state = g.pacman_pos
        frontier.put((initial_state, []))

        explored = set()
        
        while not frontier.empty():
            current_state, path = frontier.get()
            explored.add(current_state)
            #print(current_state, path)
            if g.goal_test(current_state):
                g.target_pos.discard(current_state)
                
                if not g.target_pos:
                    return path + ['Stop']
                #print("reset")
                explored.clear()
                frontier = Queue()
                frontier.put((current_state, path))
                
            for action, successor in g.get_successors(current_state):
                if successor not in explored:
                    explored.add(successor)
                    frontier.put((successor, path + [action]))
            
        return []

    def manhattan(self, current_pos, target_positions):
        return min([abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1]) for goal_pos in target_positions])

    def euclidean(self, current_pos, target_positions):
        return min([((current_pos[0] - goal_pos[0]) ** 2 + (current_pos[1] - goal_pos[1]) ** 2) ** 0.5 for goal_pos in target_positions])

    def A_star(self, g: PacmanProblem, heuristic_func) -> list:
        frontier = PriorityQueue()
        initial_state = g.pacman_pos
        f_value = 0 + heuristic_func(initial_state, g.target_pos)
        frontier.put((f_value, (initial_state, [])))

        explored = set()

        while not frontier.empty():
            current_f_value, (current_state, path) = frontier.get()
            explored.add(current_state)
            #print('\n', current_state, path)
            if g.goal_test(current_state):
                g.target_pos.discard(current_state)

                if not g.target_pos:
                    return path + ['Stop']
                #print("reset")
                explored.clear()
                frontier = PriorityQueue()
                f_value = 0 + heuristic_func(current_state, g.target_pos)
                frontier.put((f_value, (current_state, path)))

            for action, successor in g.get_successors(current_state):
                if successor not in explored:
                    explored.add(successor)
                    g_value = len(path) + 1
                    h_value = heuristic_func(successor, g.target_pos)
                    f_value = g_value + h_value

                    #print("current:", current_state, action, ' -> ', successor, ' f:', f_value)
                    
                    frontier.put((f_value, (successor, path + [action])))

        return []

def algorithm(problem: PacmanProblem):
    searcher = searchAgents()

    searcher_chosen = input("Choose Searcher:\n 1.UCS \t2.A* \n")
    searcher_chosen = int(searcher_chosen)

    if searcher_chosen==1:
        path = searcher.UCS(problem)

    elif searcher_chosen==2:
        heuristic_chosen = input("Choose Heuristic Func:\n 1.Manhattan \t 2.Euclidean\n")
        heuristic_chosen = int(heuristic_chosen)

        if heuristic_chosen==1:
            path = searcher.A_star(problem, searcher.manhattan)

        elif heuristic_chosen==2:
            path = searcher.A_star(problem, searcher.euclidean)

        else:
            print("Manhattan is chosen as default!")
            path = searcher.A_star(problem, searcher.manhattan)

    else:
        print("UCS is chosen as default!")
        path = searcher.UCS(problem)

    print("Path:", path)
    print("Total Cost:", len(path))

    for countdown in range(3, 0, -1):
        print("Pacman will go in: ", countdown)
        time.sleep(1.5)
    
    problem.let_go_pacman(path)


while True:
    pacman = PacmanProblem()

    map_chosen = input("Choose Map:\n 1.Small \t 2.Medium \t 3.Big \t 4.SmallCustom\n")
    map_chosen = int(map_chosen)

    if map_chosen==1:
        pacman.load_map("smallMaze.lay")
        algorithm(pacman)

    elif map_chosen==2:
        pacman.load_map("mediumMaze.lay")
        algorithm(pacman)

    elif map_chosen==3:
        pacman.load_map("bigMaze.lay")
        algorithm(pacman)

    elif map_chosen==4:
        pacman.load_map("customMaze.lay")
        algorithm(pacman)

    else:
        print("smallMaze is chosen as default!")
        pacman.load_map("smallMaze.lay")
        algorithm(pacman)