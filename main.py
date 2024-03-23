import itertools
from enum import Enum
from typing import Callable, Iterator, Sequence, TypedDict


class Player(Enum):
    P1 = 1
    P2 = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class GameState(TypedDict):
    p1_damage_dealt: int
    p2_damage_dealt: int
    p1_damage_received: int
    p2_damage_received: int
    p1_damage_blocked: int
    p2_damage_blocked: int
    played_cards: Sequence["PlayerCard"]

    @staticmethod
    def create_game_state():
        game_state = GameState()
        game_state["p1_damage_dealt"] = 0
        game_state["p2_damage_dealt"] = 0
        game_state["p1_damage_received"] = 0
        game_state["p2_damage_received"] = 0
        game_state["p1_damage_blocked"] = 0
        game_state["p2_damage_blocked"] = 0
        return game_state


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


class PlayerState(TypedDict):
    damage_dealt: int
    damage_received: int
    damage_blocked: int


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
    game_state = GameState.create_game_state()
    print(game_state)
    p1_card_types = ["Attack", "Attack", "Block"]
    p2_card_types = ["Block", "Block", "Attack"]
    p1_cards = [
        PlayerCard(Player.P1, Card(card_type, lambda x: x))
        for card_type in p1_card_types
    ]
    p2_cards = [
        PlayerCard(Player.P2, Card(card_type, lambda x: x))
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
