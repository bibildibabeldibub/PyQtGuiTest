import random

def direction(player = None, opponent = None):
    """:var player Player to compute direction for
    :var opponent Player to be defended
    :return angle the player should move to"""

    return random.uniform(180-45, 180+45)


