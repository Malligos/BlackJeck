import random


suits = ('Черви', 'Бубны', 'Пики', 'Трефы' )

ranks = ('Двойка', 'Тройка', 'Четверка', 'Пятерка', 'Шестерка', 'Семёрка', 'Восьмёрка', 'Девятка', 'Десятка', 'Валет',
         'Дама', 'Король', 'Туз')

values = {'Двойка': 2, 'Тройка': 3, 'Четверка': 4, 'Пятерка': 5, 'Шестерка': 6, 'Семёрка': 7, 'Восьмёрка': 8,
          'Девятка': 9, 'Десятка': 10, 'Валет': 10, 'Дама': 10, 'Король': 10, 'Туз': 11}

playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' ' + self.suit


class Deck:
    def __init__(self):
        self.deck = [] #Начинаем с пустого списка
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'В Колоде находяться карты: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def dael(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = [] # Начинаем с пустого списка, так же ка в классе Deck
        self.value = 0 # Начинаем со значения 0
        self.aces = 0 # Добавляем атрибуты что бы учитывать Тузы

    def add_card(self, card):
        # card - это из объекта Deck
        self.cards.append(card)
        self.value += values[card.rank]

        # Тузы
        if card.rank == 'Туз':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces < 0:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:

        try:
            chips.bet = int(input('Сколько вы хотите поставить?:'))

        except:
            print('Извините,пожалуйста введите число: ')

        else:
            if chips.bet > chips.total:
                print('Извините, недостаточно фишек! Доступное количество фишек : {}' .format(chips.total))

            else:
                break


def hit(deck, hand):

    single_card = deck.dael()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  #Для котроля циклr а

    while True:
        x = input('Взять дополнительную карту (hit) или остаться при своих (stand). Введите h или s ')

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print('Игрок остаеться при своих картах. Переход к ходу Диллера!')
            playing = False

        else:
            print('Извините, ответ не понятен, введите hit или stand!')
            continue
        break


def show_some(player, dealer):
    print('\n Карты Диллера:')
    print('<Карта скрыта>')
    print('', dealer.cards[1])
    print('\n Карты игрока:', *player.cards, sep='\n')


def show_all(player, dealer):
    print('\n Карты Диллера:', *dealer.cards, sep='\n')
    print('Карты Диллера:', dealer.value)
    print('\nКарты Игрока', *player.cards, sep='\n')
    print('Карты игрока =', player.value)


def player_busts(player, dealer, chips):
    print('Превышение суммы 21 для Игрока!')
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print('Игрок выиграл!')
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print('Игрок выиграл! Диллер привысил 21')
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print('Диллер выиграл!')
    chips.lose_bet()


def push(player, dealer,):
    print('Ничья')





while True:
    #Напишите приветственное сообщение!

    print('Добро пожаловать в Блэкджек!')
    print('У Вас 100 Фишек!')
    #Создайте и перешайте колоду, выдайте каждому игорку по 2 карты!
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.dael())
    player_hand.add_card(deck.dael())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.dael())
    dealer_hand.add_card(deck.dael())


    #Установите количество фишек Игрока!
    player_chips = Chips()

    #Спросите у игрока его ставку

    take_bet(player_chips)

    # Покажите карты(но оставте одну из карт Диллера скрытой

    show_some(player_hand, dealer_hand)


    while playing:

        #Спросить игрока, хочет ли он взять дополнительную карту или остаться при текущих
        hit_or_stand(deck, player_hand)
        # Покажите карты(но оставте одну из карт Диллера скрытой
        show_some(player_hand, dealer_hand)

        #Если карты игрока привыили 21, Запустите player_busts() и выйдите из Цикла (break)
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

        #Если карты игрока не превысили 21, перейдите к Картам Диллера и Берите доп карты!

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck,dealer_hand)

        #Показываем все карты!

        show_all(player_hand, dealer_hand)

        #Выполняем различные варианты завершения Игры!

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

        #Сообщить игроку количество его Фишек!
    print('\n Количество фишек: {}'.format(player_chips.total))

        #Спросить Игрока хочет ли он снова сыграть?
    new_game = input('Хотите ли Вы сыграть снова?: Yes Или No')

    if new_game[0].lower() == 'Yes':
        playing = True
        continue
    else:
        print('Спасибо за Игру!')
        break




