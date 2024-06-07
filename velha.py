import math

# Função para desenhar o tabuleiro
def draw_board(board):
    print('   |   |')
    print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
    print('   |   |')

# Função para verificar se alguém ganhou
def check_win(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Função para verificar se o tabuleiro está cheio
def check_full(board):
    return ' ' not in board

# Função para obter o movimento do jogador
def player_move(board):
    move = -1
    while move not in range(1, 10) or board[move-1] != ' ':
        try:
            move = int(input("Escolha sua jogada (1-9): "))
        except ValueError:
            print("Entrada inválida! Por favor, insira um número de 1 a 9.")
    return move - 1

# Função para obter o movimento do computador usando Minimax
def computer_move(board):
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# Função Minimax para encontrar o melhor movimento
def minimax(board, depth, is_maximizing):
    if check_win(board, 'O'):
        return 1
    elif check_win(board, 'X'):
        return -1
    elif check_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Função principal para jogar o jogo
def play_game():
    board = [' ' for _ in range(9)]
    current_player = 'X'  # O jogador começa como 'X'

    while True:
        draw_board(board)

        if current_player == 'X':
            print("Sua vez!")
            move = player_move(board)
        else:
            print("Vez do computador!")
            move = computer_move(board)

        board[move] = current_player

        if check_win(board, current_player):
            draw_board(board)
            print(f"Jogador {current_player} ganhou!")
            break
        elif check_full(board):
            draw_board(board)
            print("Empate!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    play_game()
