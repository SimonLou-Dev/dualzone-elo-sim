import numpy as np
import matplotlib.pyplot as plt
import random

# Initialisation des joueurs et de leurs niveaux intrinsèques
np.random.seed(42)  # Pour reproductibilité

n_players = 26
player_names = [chr(i) for i in range(65, 65 + n_players)]  # A-Z
intrinsic_levels = np.linspace(2000, 1000, n_players)  # Les niveaux intrinsèques décroissants
initial_elo = 1500  # Tous les joueurs commencent à 1500 Elo

# Créer un dictionnaire pour stocker les informations des joueurs
players = {
    name: {
        "intrinsic_level": level,
        "elo": initial_elo,
        "games_played": 0,
        "elo_history": [initial_elo],
    }
    for name, level in zip(player_names, intrinsic_levels)
}

# Fonction pour calculer la probabilité qu'un joueur A batte un joueur B
def win_probability(elo_a, elo_b):
    return 10 ** (elo_a / 1000) / (10 ** (elo_a / 1000) + 10 ** (elo_b / 1000))

# Fonction pour calculer le facteur K en fonction des parties jouées et de l'Elo actuel
def calculate_k(games_played, current_elo):
    if games_played < 5:
        return 350
    elif games_played < 30:
        return 200
    elif current_elo > 3000:
        return 50
    else:
        return 100

# Fonction pour limiter les pertes Elo pour les joueurs en dessous de 1000
# Et pour éviter qu'un joueur ait moins de 500 Elo
def adjust_elo(elo, change):
    if elo < 1000 and change < 0:
        change *= 0.5  # Réduire la perte d'Elo si en dessous de 1000
    new_elo = max(500, elo + change)  # Elo minimum est 500
    return new_elo

# Simulation d'un tour de matchs
def play_round():
    random.shuffle(player_names)  # Mélange les joueurs pour former des paires aléatoires
    pairs = [(player_names[i], player_names[i + 1]) for i in range(0, len(player_names), 2)]

    for player_a, player_b in pairs:
        elo_a = players[player_a]["elo"]
        elo_b = players[player_b]["elo"]

        # Calcul des probabilités de victoire
        prob_a_wins = win_probability(elo_a, elo_b)
        prob_b_wins = 1 - prob_a_wins

        # Résultat du match (basé sur les niveaux intrinsèques avec un peu d'aléatoire)
        random_factor = np.random.uniform(-0.05, 0.05)  # Pour ajouter de la variabilité
        if players[player_a]["intrinsic_level"] + random_factor > players[player_b]["intrinsic_level"]:
            result_a, result_b = 1, 0  # Victoire de A
        else:
            result_a, result_b = 0, 1  # Victoire de B

        # Mise à jour des Elos
        k_a = calculate_k(players[player_a]["games_played"], elo_a)
        k_b = calculate_k(players[player_b]["games_played"], elo_b)

        elo_change_a = k_a * (result_a - prob_a_wins)
        elo_change_b = k_b * (result_b - prob_b_wins)

        # Limiter les pertes et garantir un minimum de 500 Elo
        players[player_a]["elo"] = adjust_elo(players[player_a]["elo"], elo_change_a)
        players[player_b]["elo"] = adjust_elo(players[player_b]["elo"], elo_change_b)

        # Mise à jour des parties jouées et historique
        players[player_a]["games_played"] += 1
        players[player_b]["games_played"] += 1
        players[player_a]["elo_history"].append(players[player_a]["elo"])
        players[player_b]["elo_history"].append(players[player_b]["elo"])

# Simulation complète
n_rounds = 1000
for _ in range(n_rounds):
    play_round()

# Visualisation des courbes d'évolution des Elos
plt.figure(figsize=(12, 8))

# Trier les joueurs par leur score final d'Elo
sorted_players = sorted(players.items(), key=lambda x: x[1]["elo"], reverse=True)

for name, data in sorted_players:
    plt.plot(data["elo_history"], label=name)

plt.title("Évolution des scores Elo des joueurs", fontsize=16)
plt.xlabel("Nombre de tours", fontsize=14)
plt.ylabel("Score Elo", fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid()
plt.tight_layout()
plt.show()
