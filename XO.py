from typing import List, Optional
from random import randint


# Глобальная переменная для хранения списка игроков
player_list: Optional[List[str]] = None


def create_play_field() -> List[List[str]]:
    """Создает и возвращает пустое игровое поле."""
    return [['-' for _ in range(4)] for _ in range(4)]


def print_pl_field(play_board: List[List[str]]) -> None:
    """Функция выводит на терминал игровое поле."""
    # Заполняем первую строку и первый столбец индексами
    play_board[0] = [' ', 0, 1, 2]
    for i in range(1, 4):
        play_board[i][0] = i - 1
    # Выводим на терминал игровое поле
    for row in play_board:
        print("  ".join(map(str, row)))


def start() -> Optional[List[str]]:
    """Функция осуществляет приветствие, выбор игрока."""
    global player_list  # Используем глобальную переменную
    print('*' * 10, "Добро пожаловать в игру X VS 0", '*' * 10)
    a = input('Нажмите клавишу Enter для продолжения либо N для выхода из игры:-> ').lower()
    if a == 'n':
        return None
    else:
        if player_list is None:
            p_1 = input('Введите имя первого игрока:  ').lower()
            p_2 = input('Введите имя второго игрока:  ').lower()
            input("Для выбора очередности нажмите клавишу Enter.")
            b, c = randint(0, 10), randint(0, 10)
            if b > c:
                print(f'Игрок {p_1.title()} играет Х и ходит первым')
                player_list = [p_1, p_2]
            else:
                print(f'Игрок {p_2.title()} играет Х и ходит первым')
                player_list = [p_2, p_1]
        return player_list


def input_motion(players: List[str], marker: str, play_field: List[List[str]]) -> None:
    """Функция осуществляет ввод Х и 0 в игровое поле."""
    player = players[0] if marker == "X" else players[1]
    valid = False
    while not valid:
        try:
            print_pl_field(play_field)
            user_input = input(f'Игрок {player.title()} ({marker}) '
                              f'введите номер ячейки через запятую (строка, колонка):---> ').strip()
            # Разделяем ввод на две части
            coords = user_input.split(',')
            if len(coords) != 2:
                print('Некорректный ввод. Введите два числа через запятую.')
                continue

            # Преобразуем в числа
            row, col = int(coords[0]), int(coords[1])

            # Проверяем, что числа в допустимом диапазоне
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print('Некорректный ввод. Числа должны быть в диапазоне от 0 до 2.')
                continue

            # Проверяем, что ячейка свободна
            if play_field[row + 1][col + 1] != '-':
                print('Это поле занято!!! Выберите другую ячейку.')
                continue

            # Если все проверки пройдены, ставим маркер
            play_field[row + 1][col + 1] = marker
            valid = True

        except ValueError:
            print('Некорректный ввод. Введите два числа через запятую.')
            continue

    print_pl_field(play_field)


def check_win(board: List[List[str]], player: str) -> bool:
    """Функция определяет выигрыш."""
    
    for i in range(1, 4):
        if all(cell == player for cell in board[i][1:4]):  # Проверка строк
            return True
        if all(board[j][i] == player for j in range(1, 4)):  # Проверка столбцов
            return True

    # Проверка диагоналей
    if all(board[i][i] == player for i in range(1, 4)):
        return True
    if all(board[i][4 - i] == player for i in range(1, 4)):
        return True

    return False


def check_draw(board: List[List[str]]) -> bool:
    """Функция определяет ничью."""
    return all(cell != '-' for row in board[1:4] for cell in row[1:4])


def game():
    """Основная функция игры."""
    global player_list  # Используем глобальную переменную
    players = start()
    if not players:
        return

    play_field = create_play_field()
    current_player = "X"

    while True:
        input_motion(players, current_player, play_field)

        # Проверка на победу
        if check_win(play_field, current_player):
            print_pl_field(play_field)
            print(f"Игрок {players[0].title() if current_player == 'X' else players[1].title()} победил!")
            break

        # Проверка на ничью
        if check_draw(play_field):
            print_pl_field(play_field)
            print("Ничья!")
            break

        # Смена игрока
        current_player = "O" if current_player == "X" else "X"

    # Предложение сыграть еще раз
    cont = input('Для продолжения игры нажмите Enter, для выхода N:---> ').lower()
    if cont != 'n':
        game()  # Рекурсивный запуск игры


# Запуск игры
game()