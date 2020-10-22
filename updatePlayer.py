"""
Docs:
    Player:
        - is_in_danger -> if a player is close by and bigger,returns the distance to
            the larger palyer, otherwise returns 0

        - run_away -> moves away from the nearest player

        - attack_nearest_player -> move towards the nearest player

        - eat_food -> move towards the nearest food blob

        - get_nearest_player_size -> returns the size of the nearest player

        - get_nearest_player_distance -> returns the distance to the nearest player

        - get_food_points -> returns the point value of nearest food blob

        - get_food_distance -> returns the distance to the nearest food blob
"""

def update_player(player):
    if player.is_in_danger():
        player.run_away()
    elif player.get_nearest_player_distance() < player.get_food_distance():
        player.attack_nearest_player()
    else:
        player.eat_food()
