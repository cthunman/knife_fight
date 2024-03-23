from main import Player, GameState


class CardFunctions:
    def __init__(self):
        pass

    @staticmethod
    def attack(player: Player, game_state: GameState) -> GameState:
        new_game_state = game_state.copy()
        hero = game_state.get_hero(player)
        opponent = game_state.get_opponent(player)
        hero["damage_dealt"] += 2
        opponent["current_block"] -= 2
        while opponent["current_block"] < 0:
            opponent["damage_received"] += 1
            opponent["current_block"] += 1
        return new_game_state

    @staticmethod
    def block(player: Player, game_state: GameState) -> GameState:
        new_game_state = game_state.copy()
        hero = game_state.get_hero(player)
        hero["current_block"] += 2
        return new_game_state
