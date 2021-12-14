import random


def generate_domino_set():
    return [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 1], [1, 2],
            [1, 3], [1, 4], [1, 5], [1, 6], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
            [3, 3], [3, 4], [3, 5], [3, 6], [4, 4], [4, 5], [4, 6], [5, 5], [5, 6], [6, 6]]


def del_from_stock(_pieces):
    global stock
    for piece in _pieces:
        stock.remove(piece)


# max piece between all doubled pieces
def get_start_piece():
    return max([p for p in (computer_pieces + player_pieces) if p[0] == p[1]])


def get_user_input():
    while True:
        try:
            n_ = int(input())
            assert(n_ in range(-len(player_pieces), len(player_pieces) + 1))
        except (ValueError, AssertionError):
            print("Invalid input. Please try again.")
        else:
            return n_


def sort_comp_pieces_by_scores():
    # Count the number of 0's, 1's, 2's, etc., in computers pieces, and in the snake
    digits_amount = {}
    for digit in range(7):
        amount = 0
        for piece in (computer_pieces + snake):
            amount = amount + piece.count(digit)
        digits_amount[digit] = amount

    # Each domino receives a score equal to the sum of appearances of each of its numbers.
    # sort computer pieces - first pieces with the highest score
    def piece_score(p):
        return digits_amount[p[0]] + digits_amount[p[1]]

    computer_pieces.sort(reverse=True, key=piece_score)


def legal_move(n_, piece):
    if n_ > 0 and right_edge in piece:
        return True
    elif n_ < 0 and left_edge in piece:
        return True
    elif n_ == 0:
        return True
    else:
        return False


def draw():
    def count_ends(n_):
        return [domino[i] for domino in snake for i in range(2)].count(n_)
    if (left_edge == right_edge) and count_ends(left_edge) == 8:
        return True


def end_game():
    if not player_pieces:
        print("Status: The game is over. You won!")
    elif not computer_pieces:
        print("Status: The game is over. The computer won!")
    elif draw() is True:
        print("Status: The game is over. It's a draw!")
    else:
        return False

    return True


# if computer has start piece - player has next move. And vice versa
def determine_status():
    if start_piece in computer_pieces:
        computer_pieces.remove(start_piece)
        return 'player'
    elif start_piece in player_pieces:
        player_pieces.remove(start_piece)
        return 'computer'


def display():
    print('======================================================================')
    print(f'Stock size: {len(stock)}')
    print(f'Computer pieces: {len(computer_pieces)}')

    if len(snake) <= 6:
        print('\n', *snake, '\n', sep='')
    else:
        print(f"{snake[0]} {snake[1]} {snake[2]}...{snake[-3]} {snake[-2]} {snake[-1]} ")

    print('Your pieces:')
    for i in range(len(player_pieces)):
        print(f'{i + 1}: {player_pieces[i]}')


def make_move(n, active_set):
    global status
    new_status = 'computer' if status == 'player' else 'player'
    if n == 0:
        try:
            stock_piece = random.choice(stock)
        except IndexError:
            status = new_status
        else:
            active_set.append(stock_piece)
            stock.remove(stock_piece)
    elif n > 0:
        active_set.remove(active_piece)
        if active_piece[0] != right_edge:
            active_piece.reverse()
        snake.insert(len(snake), active_piece)
    elif n < 0:
        active_set.remove(active_piece)
        if active_piece[1] != left_edge:
            active_piece.reverse()
        snake.insert(0, active_piece)

    status = new_status


# handing out dominoes, 7 for computer, 7 for player, others in stock
# select start piece. If there is not any double piece - hand out dominoes again
while True:
    stock = generate_domino_set()

    computer_pieces = random.sample(stock, k=7)
    del_from_stock(computer_pieces)

    player_pieces = random.sample(stock, k=7)
    del_from_stock(player_pieces)

    start_piece = get_start_piece()
    if start_piece is not None:
        status = determine_status()
        snake = [start_piece]
        break

display()
while True:
    right_edge = snake[len(snake) - 1][1]
    left_edge = snake[0][0]
    if status == 'player':
        print("\nStatus: It's your turn to make a move. Enter your command.")
        # getting player's input until it's valid and legal
        while True:
            n = get_user_input()
            active_piece = player_pieces[abs(n) - 1]
            if not legal_move(n, active_piece):
                print('Illegal move. Please try again')
            else:
                break
        make_move(n, player_pieces)
    else:
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        input()
        sort_comp_pieces_by_scores()

        move_status = False
        for active_piece in computer_pieces:
            if legal_move(1, active_piece):
                move_status = True
                make_move(1, computer_pieces)
                break
            elif legal_move(-1, active_piece):
                move_status = True
                make_move(-1, computer_pieces)
                break

        if move_status is False:  # if was not any legal move - skip turn
            make_move(0, computer_pieces)

    display()
    if end_game():
        break
