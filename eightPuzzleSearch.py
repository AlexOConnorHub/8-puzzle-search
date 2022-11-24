#!/usr/bin/env python3

# 0 1 2
# 3 4 5
# 6 7 8
import random
import queue

SOLUTION = "12345678-"

correct_position = {
    '1': (0, 0),
    '2': (1, 0),
    '3': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '7': (0, 2),
    '8': (1, 2)
}

valid_moves = {
    0: [1, 3],         # 0
    1: [0, 2, 4],      # 1
    2: [1, 5],         # 2
    3: [0, 4, 6],      # 3
    4: [1, 3, 5, 7],   # 4
    5: [2, 4, 8],      # 5
    6: [3, 7],         # 6
    7: [4, 6, 8],      # 7
    8: [5, 7]          # 8
}

def scramble(depth: int) -> str:
    final = SOLUTION
    for _ in range(depth):
        final = puzzle_move(final, random.choice(valid_moves[final.find('-')]))
    return final

def puzzle_move(state_of_puzzle: str, pos: int) -> str:
    char_to_move = state_of_puzzle[pos]
    final = ""
    for char in state_of_puzzle:
        if (char == "-"):
            final += char_to_move
        elif char == char_to_move:
            final += "-"
        else:
            final += char
    return final

def number_of_tiles_out_of_place(state_of_puzzle: str) -> int:
    return sum(
        char != str(solution_state) and (solution_state != 9 or char != '-')
        for solution_state, char in enumerate(state_of_puzzle, start=1)
    )

def manhattan_distance(state_of_puzzle: str) -> int:
    final = 0
    for i in range(9):
        char_in_question = state_of_puzzle_gui[i]
        if (char_in_question == '-'):
            continue
        final = final + abs(i % 3 - correct_position[char_in_question][0]) + abs(
            int(i/3) - correct_position[char_in_question][1])
        # final = final + abs(i % 3 - ((int(i) - 1) % 3)) + abs(
        #     int(i/3) - int((int(i) - 1) / 3))
    return final

def breadth_first_search(state_of_puzzle: str) -> list[str]:
    q = queue.SimpleQueue()
    q.put(str(state_of_puzzle.find('-')) + state_of_puzzle)
    states = {state_of_puzzle: None}
    while(SOLUTION not in states):
        state = q.get()
        possible_moves = valid_moves[int(state[0])]
        for move in possible_moves:
            to_push = puzzle_move(state[1:], move)
            if(to_push not in states):
                states[to_push] = state[1:]
                q.put(str(move) + to_push)
    final = [SOLUTION]
    while (states[final[-1]] != None):
        final.append(states[final[-1]])
    final.reverse()
    return final

def best_first_search(state_of_puzzle: str, heuristic: str) -> list[str]:
    q = queue.PriorityQueue()
    q.put((heuristic(state_of_puzzle), str(state_of_puzzle.find('-')) + state_of_puzzle))
    states = {state_of_puzzle: None}
    while(SOLUTION not in states):
        state = q.get()[1]
        possible_moves = valid_moves[int(state[0])]
        for move in possible_moves:
            to_push = puzzle_move(state[1:], move)
            if(to_push not in states):
                states[to_push] = state[1:]
                q.put((heuristic(to_push), str(move) + to_push))
    final = [SOLUTION]
    while (states[final[-1]] != None):
        final.append(states[final[-1]])
    final.reverse()
    return final

def a_star_search(state_of_puzzle: str, heuristic: str) -> list[str]:
    q = queue.PriorityQueue()
    q.put((heuristic(state_of_puzzle), str(state_of_puzzle.find('-')) + state_of_puzzle + '0'))
    states = {state_of_puzzle: None}
    while(SOLUTION not in states):
        state = q.get()[1]
        depth = int(state[10:]) + 1
        possible_moves = valid_moves[int(state[0])]
        for move in possible_moves:
            to_push = puzzle_move(state[1:10], move)
            if(to_push not in states):
                states[to_push] = state[1:10]
                q.put((heuristic(to_push) + depth,
                      str(move) + to_push + str(depth)))
    final = [SOLUTION]
    while (states[final[-1]] != None):
        final.append(states[final[-1]])
    final.reverse()
    return final

########## GUI SECTION ##########
if (__name__ == "__main__"):
    import tkinter
    import time
    # global variables
    window = tkinter.Tk()
    toTime = tkinter.IntVar()
    heuristic_func = tkinter.IntVar()
    state_of_puzzle_gui = SOLUTION
    previous_scramble = state_of_puzzle_gui
    heuristic_func_to_use = [
        number_of_tiles_out_of_place,
        manhattan_distance
    ]
    
    # functions for gui

    def move_gui(index: str):
        global state_of_puzzle_gui
        if (buttons[index]['text'] == "-"):
            return
        grid_of_puzzle = [[[], [], []], [[], [], []], [[], [], []]]
        index_of_blank = None
        index_of_selected = None
        can_move_x = False
        can_move_y = False
        i = 0
        for x in range(3):
            for y in range(3):
                grid_of_puzzle[x][y] = state_of_puzzle_gui[i]
                if (buttons[i]['text'] == "-"):
                    index_of_blank = [x, y]
                elif (buttons[i]['text'] == buttons[index]['text']):
                    index_of_selected = [x, y]
                i += 1
        same_x = index_of_selected[0] == index_of_blank[0]
        same_y = index_of_selected[1] == index_of_blank[1]
        can_move_x = False
        can_move_y = False
        if (index_of_selected[0] > index_of_blank[0]):
            if ((index_of_selected[0] - 1) == index_of_blank[0]):
                can_move_x = True
        elif ((index_of_selected[0] + 1) == index_of_blank[0]):
            can_move_x = True

        if (index_of_selected[1] > index_of_blank[1]):
            if ((index_of_selected[1] - 1) == index_of_blank[1]):
                can_move_y = True
        elif ((index_of_selected[1] + 1) == index_of_blank[1]):
            can_move_y = True

        if ((can_move_x and same_y) or (same_x and can_move_y)):
            state_of_puzzle_gui = puzzle_move(state_of_puzzle_gui, index)
            set_gui_state_gui(state_of_puzzle_gui)

    def scramble_gui():
        global state_of_puzzle_gui
        global previous_scramble
        previous_scramble = state_of_puzzle_gui
        new_state_of_puzzle_gui = scramble(100)
        set_gui_state_gui(new_state_of_puzzle_gui)
        state_of_puzzle_gui = new_state_of_puzzle_gui

    def previous_scramble_gui():
        global state_of_puzzle_gui
        global previous_scramble
        set_gui_state_gui(previous_scramble)
        state_of_puzzle_gui = previous_scramble

    def set_gui_state_gui(new_state: str):
        global state_of_puzzle_gui
        for i in range(9):
            buttons[i]['text'] = new_state[i]
        state_of_puzzle_gui = new_state
        window.update()

    def show_heuristic_gui():
        global state_of_puzzle_gui
        global heuristic_func
        global heuristic_func_to_use
        top = tkinter.Toplevel(window)
        top.geometry("100x50")
        top.title("Time of Solve")
        tkinter.Label(top, text=str(heuristic_func_to_use[heuristic_func.get()](state_of_puzzle_gui)), font=('Calibri 18 bold')).place(x=15, y=8)

    def solve_gui(func_name):  # sourcery skip: hoist-statement-from-if
        global state_of_puzzle_gui
        global previous_scramble
        global heuristic_func
        global heuristic_func_to_use
        if (state_of_puzzle_gui == SOLUTION):
            return
        previous_scramble = state_of_puzzle_gui
        start_time = None
        end_time = None
        solution_path = None
        if (func_name.__code__.co_argcount == 2):
            to_use = heuristic_func_to_use[heuristic_func.get()]
            start_time = time.perf_counter()
            solution_path = func_name(state_of_puzzle_gui, to_use)
            end_time = time.perf_counter()
        else:
            start_time = time.perf_counter()
            solution_path = func_name(state_of_puzzle_gui)
            end_time = time.perf_counter()
        if (toTime.get()):
            top = tkinter.Toplevel(window)
            top.geometry("250x80")
            top.title("Time of Solve")
            tkinter.Label(top, text=str(end_time - start_time)[:6] + " seconds\nusing " + str(len(solution_path) - 1) + " moves", font=('Calibri 18 bold')).place(x=15, y=8)
        sleep_time = 10/len(solution_path)
        for step in solution_path:
            set_gui_state_gui(step)
            time.sleep(sleep_time)

    def run_everything_gui():
        average_breadth = [0, 0]
        average_best_man = [0, 0]
        average_best_num = [0, 0]
        average_a_man = [0, 0]
        average_a_num = [0, 0]
        NUM_OF_RUNS = 6
        for _ in range(NUM_OF_RUNS):
            scrambled = scramble(100)
            set_gui_state_gui(scrambled)

            start_time = time.perf_counter()
            breadth = breadth_first_search(scrambled)
            average_breadth[0] = average_breadth[0] + time.perf_counter() - start_time
            average_breadth[1] = average_breadth[1] + len(breadth)

            start_time = time.perf_counter()
            best_man = best_first_search(scrambled, manhattan_distance)
            average_best_man[0] = average_best_man[0] + time.perf_counter() - start_time
            average_best_man[1] = average_best_man[1] + len(best_man)

            start_time = time.perf_counter()
            best_num = best_first_search(scrambled, number_of_tiles_out_of_place)
            average_best_num[0] = average_best_num[0] + time.perf_counter() - start_time
            average_best_num[1] = average_best_num[1] + len(best_num)

            start_time = time.perf_counter()
            a_star_man = a_star_search(scrambled, manhattan_distance)
            average_a_man[0] = average_a_man[0] + time.perf_counter() - start_time
            average_a_man[1] = average_a_man[1] + len(a_star_man)

            start_time = time.perf_counter()
            a_star_num = a_star_search(scrambled, number_of_tiles_out_of_place)
            average_a_num[0] = average_a_num[0] + time.perf_counter() - start_time
            average_a_num[1] = average_a_num[1] + len(a_star_num)
        average_breadth = [i / NUM_OF_RUNS for i in average_breadth]
        average_best_man = [i / NUM_OF_RUNS for i in average_best_man]
        average_best_num = [i / NUM_OF_RUNS for i in average_best_num]
        average_a_man = [i / NUM_OF_RUNS for i in average_a_man]
        average_a_num = [i / NUM_OF_RUNS for i in average_a_num]
        output_text = "Averages of " + str(NUM_OF_RUNS) + " runs: \n"
        output_text = output_text + "Breadth first: " + str(average_breadth[0])[:6] + " seconds, " + str(average_breadth[1])[:6] + " moves\n"
        output_text = output_text + "Best first (tile): " + str(average_best_num[0])[:6] + " seconds, " + str(average_best_num[1])[:6]+ " moves\n"
        output_text = output_text + "Best first (dist): " + str(average_best_man[0])[:6] + " seconds, " + str(average_best_man[1])[:6] + " moves\n"
        output_text = output_text + "A* (tile): " + str(average_a_num[0])[:6] + " seconds, " + str(average_a_num[1])[:6] + " moves\n"
        output_text = output_text + "A* (dist): " + str(average_a_man[0])[:6] + " seconds, " + str(average_a_man[1])[:6] + " moves\n"
        top = tkinter.Toplevel(window)
        top.geometry("600x200")
        top.title("Averages of Solves")
        tkinter.Label(top, text=output_text, font=('Calibri 18')).place(x=15, y=8)
        reset_gui()

    def reset_gui():
        set_gui_state_gui(SOLUTION)

    # GUI Window
    window.geometry("810x765")
    window.config(bg="#333333")
    window.resizable(width=False, height=False)
    window.title('3x3 Slide Puzzle')

    # GUI Menu
    menubar = tkinter.Menu(window)

    solve_menu = tkinter.Menu(menubar, tearoff=0)
    solve_menu.add_command(label="A*", command=lambda method_to_use=a_star_search: solve_gui(method_to_use))
    solve_menu.add_command(label="Best First", command=lambda method_to_use=best_first_search: solve_gui(method_to_use))
    solve_menu.add_command(label="Breadth First",
                        command=lambda method_to_use=breadth_first_search: solve_gui(method_to_use))
    solve_menu.add_separator()
    solve_menu.add_command(label="See Heuristic", command=show_heuristic_gui)
    solve_menu.add_command(label="Test Methods", command=run_everything_gui)
    menubar.add_cascade(label="Solve", menu=solve_menu)

    scramble_menu = tkinter.Menu(menubar, tearoff=0)
    scramble_menu.add_command(label="Scramble", command=scramble_gui)
    scramble_menu.add_command(label="Previous Scramble", command=previous_scramble_gui)
    scramble_menu.add_command(label="Reset", command=reset_gui)
    menubar.add_cascade(label="Scramble", menu=scramble_menu)

    heuristic_menu = tkinter.Menu(menubar, tearoff=0)
    heuristic_menu.add_checkbutton(label="Timer", variable=toTime)
    heuristic_menu.add_separator()
    heuristic_menu.add_radiobutton(label="Number of Tiles Out of Place", variable=heuristic_func, value=0)
    heuristic_menu.add_radiobutton(label="Manhattan Distance", variable=heuristic_func, value=1)
    heuristic_menu.add_separator()
    heuristic_menu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="Settings", menu=heuristic_menu)

    window.config(menu=menubar)

    # GUI Buttons
    pixel = tkinter.PhotoImage(width=1, height=1)
    buttons = []
    x = 0
    y = 0
    for i in range(0, 9):
        if (i == 8):
            buttons.append(tkinter.Button(window, text="-", font=("Calibri 50"), image=pixel, height=250, width=250, bg="#AAAAAA", compound="center",  command=lambda t=i: move_gui(t)))
        else:
            buttons.append(tkinter.Button(window, text=str(i + 1), font=("Calibri 50"), image=pixel, height=250, width=250, bg="#AAAAAA", compound="center", command=lambda t=i: move_gui(t)))
        buttons[-1].place(x=(x % 3) * 265, y=y * 250)
        x = x + 1
        if ((x % 3) == 0):
            y = y + 1

    window.mainloop()

############ RESULT DISCUSSION ############
# Results from 6 runs with 100 scramble   Time (sec)    Moves
# Breadth first                            0.5469       19.666
# Best first (Tiles out of Place)          0.0705       104.0
# Best  first (Manhattan)                  0.7138       86.0
# A* (Tiles out of Place)                  0.6122       19.666
# A* (Manhattan)                           1.9176       19.666
# ---
# Based on my results I have currently, Breadth first search is the best 
# method for searching for optimal solutions. On some tests where the 
# average moves per solution was less than 18, A* using tiles out of place 
# did a bit better when measured by time. This is an interesting result, 
# and most likly points to a non-optimal program, rather than a non-optimal
# method. While I do not check this at all, due to the method, the A* 
# should use less memory.
#
# Also, before starting this project, I knew A.I. loves numbers, but did 
# not realize how much simply adding the depth to the queue sorting could
# change the effiency of the output of the function.