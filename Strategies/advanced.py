import math

def betrag(vec: list):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

def strat(defender, attacker, scene):
    """
    @param attacker: zugeordneter Angreifer
    @param scene: Spielszene
    @return: Position to move
    """
    print("Starting ADvanced Pos (Thread)----------------------------------------------------")
    attacker_pos = attacker.getLocation()
    goal_pos = [450, 0]
    vec = [goal_pos[0] - attacker_pos[0], goal_pos[1] - attacker_pos[1]]
    n = 250 / betrag(vec)
    naiv_pos = [attacker_pos[0] + vec[0]*n, attacker_pos[1] + vec[1]*n]
    defender.new_pos = naiv_pos

    return naiv_pos

