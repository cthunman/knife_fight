import itertools
from enum import Enum
from typing import Callable, Iterator, Sequence, TypedDict

from card_functions import CardFunctions


class Player(Enum):
    P1 = 1
    P2 = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class PlayerState(TypedDict):
    damage_dealt: int
    damage_received: int
    damage_blocked: int
    current_block: int
    played_cards: Sequence["PlayerCard"]

    @staticmethod
    def create_player_state():
        player_state = PlayerState()
        player_state["damage_dealt"] = 0
        player_state["damage_received"] = 0
        player_state["damage_blocked"] = 0
        player_state["played_cards"] = []
        return player_state


class GameState:
    def __init__(self) -> None:
        self.p1 = PlayerState.create_player_state()
        self.p2 = PlayerState.create_player_state()

    def get_opponent(self, player: Player) -> Player:
        if player == Player.P1:
            return self.p2
        return self.p1

    def get_hero(self, player: Player) -> PlayerState:
        if player == Player.P1:
            return self.p1
        return self.p2

    def copy(self):
        new_game_state = GameState()
        new_game_state.p1 = self.p1.copy()
        new_game_state.p2 = self.p2.copy()
        return new_game_state


class Card:
    def __init__(
        self, type: str, card_effect: Callable[[Player, GameState], GameState]
    ) -> None:
        self.type: str = type
        self.card_effect = card_effect

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.__str__()


class PlayerCard:
    def __init__(self, player: Player, card: Card) -> None:
        self.player = player
        self.card = card

    def play(self, game_state: GameState) -> GameState:
        updated_game_state = self.card.card_effect(self.player, game_state)
        updated_game_state["played_cards"].append(self)
        return updated_game_state

    def __str__(self):
        return f"{self.player} Card: {self.card}"

    def __repr__(self):
        return self.__str__()


class PlayerAction:
    def __init__(self, player: Player, card: Card) -> None:
        self.player = player
        self.card = card

    def __str__(self):
        return f"Player: {self.player}, Card: {self.card}"

    def __repr__(self):
        return self.__str__()


class Round:
    def __init__(
        self, p1_cards: Sequence[PlayerCard], p2_cards: Sequence[PlayerCard]
    ) -> None:
        self.p1_cards = p1_cards
        self.p2_cards = p2_cards

    def combos(self):
        all_cards = list()
        all_cards.extend(self.p1_cards)
        all_cards.extend(self.p2_cards)
        return itertools.permutations(all_cards)

    def to_json(self):
        return {
            "p1_cards": [str(card) for card in self.p1_cards],
            "p2_cards": [str(card) for card in self.p2_cards],
        }

    def __str__(self):
        return f"Player 1: {self.p1_cards}, Player 2: {self.p2_cards}"


class Game:
    def __init__(
        self, player1: Player, player2: Player, cards_played: Sequence[Card]
    ) -> None:
        self.player1: Player = player1
        self.player2: Player = player2
        self.cards_played: Sequence[Card] = cards_played
        self.game_state: GameState = self.calculate_outcome()

    def calculate_outcome(self):
        pass

    def __str__(self):
        return f"Player 1: {self.player1}, Player 2: {self.player2}, Cards Played: {self.cards_played}"


class GameBoard:
    def __init__(self, card_list: Sequence[PlayerCard]) -> None:
        self.card_list = card_list

    def evaluate(self) -> GameState:
        game_state: GameState = GameState.create_game_state()
        for card in self.card_list:
            game_state = card.play(game_state)
        return game_state


def main():
    p1_card_types = ["Attack", "Attack", "Block"]
    p2_card_types = ["Block", "Block", "Attack"]
    p1_cards = [
        PlayerCard(Player.P1, Card(card_type, CardFunctions.attack))
        for card_type in p1_card_types
    ]
    p2_cards = [
        PlayerCard(Player.P2, Card(card_type, CardFunctions.attack))
        for card_type in p2_card_types
    ]

    p1_card_combos: Iterator = itertools.permutations(p1_cards, 2)
    p2_card_combos: Iterator = itertools.permutations(p2_cards, 2)
    for round in itertools.product(p1_card_combos, p2_card_combos):
        round_obj = Round(round[0], round[1])
        print(round_obj)
        for combo in round_obj.combos():
            print(combo)


if __name__ == "__main__":
    main()
