import time 
import random
import curses
from PC import PC
from levels import easy_levels, normal_levels, challenger_levels, expert_levels, mastermind_levels

def print_ascii_art(stdscr, pillar_num, pillar_blocks_nums, put_text):
    clear_screen_cache(stdscr)
    game_rendering = load_text_file('pages/game_play_page.txt')
    for index, line in enumerate(game_rendering):
        stdscr.addstr(index, 0, line.strip())

    cols = 123
    fill_symbol = "."
    roof = "███████"
    top_block = "╚╬╬╬╝"
    bottom_block = "╔╬╬╬╗"

    pillar_width = len(roof)
    total_pillar_width = pillar_num * pillar_width
    spacing_between_pillars = 2
    total_spacing_width = (pillar_num - 1) * spacing_between_pillars
    roof_width = total_pillar_width + total_spacing_width
    start = (cols - roof_width) // 2 + 1  
    max_height = max(pillar_blocks_nums) + 2

    # Print the roof row
    roof_row = [fill_symbol] * cols
    roof_start = start - 1
    for j in range(roof_width):
        roof_row[roof_start + j] = "▄"
    put_text(stdscr, 12 - max_height, 1, "".join(roof_row))

    # Print pillar rows (This For-Loop was written with the help of ChatGPT):
    for i in range(max_height):
        row_content = [fill_symbol] * cols
        for p in range(pillar_num):
            pillar_start = start + p * (pillar_width + spacing_between_pillars)
            num_blocks = pillar_blocks_nums[p]
            if i == 0:
                block = top_block
            elif i == max_height - 1:
                block = bottom_block
            else:
                if i <= num_blocks:
                    block = f".╠{i}╣."
                else:
                    block = ".║▒║."
            for j in range(len(block)):
                if pillar_start + j < cols:
                    row_content[pillar_start + j] = block[j]
        put_text(stdscr, 13 - max_height + i, 1, "".join(row_content))

    # Print the ground row
    ground_row = [fill_symbol] * cols
    for j in range(roof_width):
        ground_row[roof_start + j] = "█"
    put_text(stdscr, 13, 1, "".join(ground_row))


def load_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return ["Error: File not found."]


def put_text(stdscr, pos_row, pos_col, text):
    try:
        stdscr.addstr(pos_row, pos_col, text)
    except curses.error:
        pass 

def clear_screen_cache(stdscr):
    stdscr.clear()
    stdscr.clearok(True)
    stdscr.refresh()

def show_welcome(stdscr):
    stdscr.clear()
    
    welcome_text = load_text_file('pages/welcome_page.txt')
    for index, line in enumerate(welcome_text):
        stdscr.addstr(index, 0, line.strip())
    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key in [ord('i'), ord('I')]:  
            show_instructions(stdscr)
            break
        elif key in [ord('q'), ord('Q')]:
            break
        elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            level = int(chr(key))
            choose_level_after_difficulty(stdscr, level)
            break


def choose_level_after_difficulty(stdscr, difficulty_level):
    stdscr.clear()
    
    render_text = load_text_file('pages/selecting_levels_page.txt')
    for index, line in enumerate(render_text):
        stdscr.addstr(index, 0, line.strip())
    stdscr.refresh()

    difficulty_map = {
        1: (500, easy_levels, "Easy"),
        2: (1000, normal_levels, "Normal"),
        3: (2500, challenger_levels, "Challenger"),
        4: (5000, expert_levels, "Expert"),
        5: (10000, mastermind_levels, "Mastermind"),
    }
    traning_n_times, level_dict, difficulty_level_text = difficulty_map.get(difficulty_level, (500, easy_levels, "Easy"))

    selected_level = 1
    max_level = 9

    # Show arrow ^^ here
    def display_level_selection():
        for index, line in enumerate(render_text):
            stdscr.addstr(index, 0, line.strip())
        put_text(stdscr, 13, 5 + 13 * (selected_level - 1), "^^^^^^^^^^^")
        put_text(stdscr, 15, 17, difficulty_level_text)
        put_text(stdscr, 16, 22, str(selected_level))
        stdscr.refresh()

    display_level_selection()  

    while True:
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:  # click -> arrow butt
            if selected_level < max_level :
                selected_level += 1
            else :
                selected_level = 1

        elif key == curses.KEY_LEFT:  # click -> arrow butt 
            if selected_level > 1 :
                selected_level -= 1
            else :
                selected_level = 9

        elif key == ord('\n'):  # click enter to enter
            if selected_level in level_dict:
                game_config = level_dict[selected_level]
                break
            else:
                put_text(stdscr, 15, 0, "Invalid level selection. Try again.")
                stdscr.refresh()
                continue

        elif key in [ord('b'), ord('B')]:  
            show_welcome(stdscr)
            return

        display_level_selection()

    # init game
    game = PC(initial_pillars=game_config['pillars'], max_blocks_per_turn=game_config['max_blocks'])

    loading_text = load_text_file('pages/loading_page.txt')

    for index, line in enumerate(loading_text):
        stdscr.addstr(index, 0, line.strip())
    stdscr.refresh()

    game.train(traning_n_times)
    start_game(stdscr, game=game)


def show_instructions(stdscr):
    stdscr.clear()

    blank_text = load_text_file('pages/blank_page.txt')
    for index, line in enumerate(blank_text):
        stdscr.addstr(index, 0, line.strip())
    
    instructions_text = [
        "Instructions:",
        "- Choose difficulty by pressing a number (1-5) in the welcome screen.",
        "- Choose a level after selecting difficulty by pressing a number (1-9).",
        "- Don't be the last player who make it collapse",
        "- Enjoy!!!"
    ]
    
    start_row = 5
    start_col = 5

    for index, line in enumerate(instructions_text):
        put_text(stdscr, start_row + index, start_col, line)
    put_text(stdscr, start_row + len(instructions_text) + 2, start_col, "Press 'B' to go back.")
    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key in [ord('b'), ord('B')]:
            show_welcome(stdscr)
            break

def start_game(stdscr, game):
    stdscr.clear()

    game.pillars = game.initial_pillars.copy()
    print_ascii_art(stdscr, len(game.pillars), game.pillars, put_text)
    stdscr.refresh()
    game.player = random.randint(0, 1)
    game.winner = None

    selected_pile = 0  # init pile
    selected_count = 1  # init block

    ai_play_atleast_onced = False
    ai_last_move_pile = 0
    ai_last_move_block_take = 1

    

    def display_selection_marker():
        stdscr.addstr(14, 0, "║...........................................................................................................................║")

        # show ^^^ under pillars
        pillar_start = 64 - int(9 * len(game.pillars) / 2) + selected_pile * 9  
        put_text(stdscr, 14, pillar_start, "^^^^^")

        put_text(stdscr, 16, 2, "Your Turn! Use arrows to select pile and blocks, press Enter to confirm.")
        put_text(stdscr, 17, 2, f"[« »] Selected Pile: {selected_pile + 1}")
        if game.pillars[selected_pile] >= game.max_blocks_per_turn :
            if selected_count > game.max_blocks_per_turn :
                # selected_count = game.max_blocks_per_turn
                pass
            put_text(stdscr, 18, 2, f"[^ v] Number of Blocks to Remove: {selected_count} ({game.max_blocks_per_turn} Blocks Maximum)")
        elif game.pillars[selected_pile] < game.max_blocks_per_turn :
            if selected_count > game.pillars[selected_pile] :
                # selected_count = game.pillars[selected_pile]
                pass
            put_text(stdscr, 18, 2, f"[^ v] Number of Blocks to Remove: {selected_count} ({game.pillars[selected_pile]} Blocks Maximum)")
        put_text(stdscr, 16, 75, ".AI's Last Move:.....")
        if ai_play_atleast_onced :
            put_text(stdscr, 17, 75, f".Selected Pile: {ai_last_move_pile + 1}")
            put_text(stdscr, 18, 75, f".Blocks Removed: {ai_last_move_block_take}")
        else :
            put_text(stdscr, 17, 75, f".Selected Pile: -")
            put_text(stdscr, 18, 75, f".Blocks Removed: -")

        stdscr.refresh()

    while True:
        display_selection_marker()
        available = game.available_actions(game.pillars)

        if game.winner is not None:
            print_ascii_art(stdscr, len(game.pillars), game.pillars, put_text)
            # Overlay result text without clearing the final state
            result_text = None
            if game.winner == 0:
                result_text = load_text_file('pages/victory_overwrite.txt')
            else:
                result_text = load_text_file('pages/defeat_overwrite.txt')
            
            if result_text:
                for index, line in enumerate(result_text):
                    put_text(stdscr, index, 0, line.strip())
            else:
                put_text(stdscr, 3, 5, "Error: Result page file not found or is empty.")
            
            # Display AI's last move as an overlay
            put_text(stdscr, 16, 75, ".AI's Last Move:")
            put_text(stdscr, 17, 75, f".Selected Pile: {ai_last_move_pile + 1}")
            put_text(stdscr, 18, 75, f".Blocks Removed: {ai_last_move_block_take}")

            stdscr.refresh()
            time.sleep(1)

            while True:
                key = stdscr.getch()
                if key in [ord('b'), ord('B')]:
                    show_welcome(stdscr)
                    return

        if game.player == 0:
            valid_input = False

            while not valid_input:
                key = stdscr.getch()
                
                if key == curses.KEY_RIGHT:
                    if selected_pile+1 < len(game.pillars) :
                        selected_pile = selected_pile + 1 
                    else :
                        selected_pile = 0

                elif key == curses.KEY_LEFT:
                    if selected_pile+1 > 1 :
                        selected_pile = selected_pile - 1 
                    else :
                        selected_pile = len(game.pillars)-1
                
                elif key == curses.KEY_UP:
                    if game.pillars[selected_pile] >= game.max_blocks_per_turn :
                        if selected_count+1 < game.max_blocks_per_turn :
                            selected_count += 1
                        else :
                            selected_count = game.max_blocks_per_turn
                    else :
                        if selected_count+1 < game.pillars[selected_pile] :
                            selected_count += 1
                        else :
                            selected_count = game.pillars[selected_pile]

                elif key == curses.KEY_DOWN:
                    if selected_count-1 > 1 :
                        selected_count -= 1
                    else :
                        selected_count = 1
                    
                elif key == ord('\n'):  #Enter to enter
                    if (selected_pile, selected_count) in available:
                        valid_input = True  
                    else:
                        put_text(stdscr, 16, 2, "Invalid move or exceeds max blocks! Try again.") # just in case 
                        stdscr.refresh()
                elif key in [ord('b'), ord('B')]:
                    show_welcome(stdscr)
                    return
                display_selection_marker()
                stdscr.refresh()

            game.move((selected_pile, selected_count))

        # AI's turn
        else:
            print_ascii_art(stdscr, len(game.pillars), game.pillars, put_text)
            # Clear player message area with dots and display AI's message
            put_text(stdscr, 16, 1, ".[You need to wait]......................................................")
            put_text(stdscr, 17, 1, ".........................................................................")
            put_text(stdscr, 18, 1, ".........................................................................")
            put_text(stdscr, 16, 75, ".AI's Turn! Thinking.............................")
            stdscr.refresh()
            time.sleep(1.5)  # Pause for 1 second to simulate AI thinking
            action = game.choose_best_action(game.pillars, epsilon=0)
            if action:
                game.move(action)
                # Display the AI's move details
                ai_pile, ai_count = action
                ai_last_move_pile = ai_pile
                ai_last_move_block_take = ai_count
                ai_play_atleast_onced = True
                print_ascii_art(stdscr, len(game.pillars), game.pillars, put_text)
                stdscr.refresh()
            else:
                put_text(stdscr, 16, 75, "AI could not make a move.")
                stdscr.refresh()

# init
def main(stdscr):
    curses.curs_set(0)  # hide cursor
    show_welcome(stdscr)  # start at welcome screen

curses.wrapper(main)

