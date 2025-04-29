# 🎮 XO Battle - Jeu de Morpion en Python

## 📋 Description du projet

**XO Battle** est un jeu de Morpion (Tic Tac Toe) développé en **Python** avec une interface graphique réalisée avec **Tkinter**.  
Il propose plusieurs modes de jeu :
- Joueur contre Joueur (local)
- Joueur contre l'ordinateur (IA)
- Joueur contre Joueur en ligne (réseau)

---

## 🛠️ Installation (avec Visual Studio Code)

1. **Installer Python 3.x** : [python.org](https://www.python.org/)
2. **Installer Visual Studio Code** : [code.visualstudio.com](https://code.visualstudio.com/)
3. **Installer l'extension Python** dans VS Code.
4. **Cloner ou copier** ce projet sur ton ordinateur.
5. **Ouvrir le projet** avec Visual Studio Code.
6. **Ouvrir `tictactoe.py`**.
7. **Lancer** (`▶️` en haut ou F5) pour démarrer le jeu.

---

## 🚀 Comment jouer

1. Lance le jeu.
2. Choisis ton mode de jeu :
   - Joueur contre Joueur
   - Joueur contre IA
   - Joueur contre Joueur en ligne
3. Clique sur "Start Game" pour commencer.
4. Clique sur une case pour jouer ton tour.
5. Le premier joueur à aligner 3 symboles gagne.

---

## 🌐 Mode en ligne

- **Host** : Héberge la partie et attends qu'un joueur se connecte.
- **Join** : Rejoins une partie en entrant l'**adresse IP** de l'hôte.

> Le réseau utilise **TCP** sur le **port 65432**.

---

## 🧩 Fonctionnement du code

### 1. Importations
- `tkinter` : Pour créer l'interface graphique.
- `socket` : Pour les connexions réseau.
- `threading` et `queue` : Pour gérer les échanges en ligne.
- `random` : Pour que l'IA joue automatiquement.

### 2. Principales classes

- **NetworkGame** : 
  - Gère l'hébergement, la connexion et l'envoi de coups en ligne.
- **TicTacToeApp** : 
  - Gère l'interface du jeu.
  - Gère la logique de jeu (joueur local, IA, réseau).
  - Détecte la victoire ou l'égalité.
  - Rafraîchit le plateau de jeu.

### 3. Boucle principale
```python
root = tk.Tk()
app = TicTacToeApp(root)
root.mainloop()
✨ Caractéristiques du jeu
Interface colorée (fond rose, X noirs, O gris clair).

Sons à chaque clic.

Texte de victoire en vert et défaite en rouge.

Support pour le jeu en ligne simple et rapide.

📢 Conseils pour le mode en ligne
Utiliser le même réseau Wi-Fi, ou ouvrir le port 65432 si nécessaire.

Vérifier que le pare-feu Windows autorise Python.

Donner l'adresse IP publique si vous jouez à distance.