"""Rock, Paper, Scissors game with terminal and Tkinter interfaces.

Run ``python RPC.py`` for the terminal game or ``python RPC.py --gui`` for
the desktop interface.
"""

import argparse
import random
import tkinter as tk
from tkinter import ttk


# Public game data used by both interfaces.
CHOICES = ("rock", "paper", "scissors")
CHOICE_ICONS = {"rock": "✊", "paper": "✋", "scissors": "✌"}
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def play_round(player: str, computer: str | None = None) -> tuple[str, str]:
    """Resolve one game round.

    Args:
        player: The player's move: ``rock``, ``paper``, or ``scissors``.
        computer: An optional computer move. When omitted, a random valid move
            is selected. Supplying a move makes the function deterministic
            and useful for tests.

    Returns:
        A tuple containing the computer's move and the winner identifier.
        The winner is ``"player"``, ``"computer"``, or ``"draw"``.

    Raises:
        ValueError: If either move is not one of the supported choices.
    """
    if player not in CHOICES:
        raise ValueError(f"Unknown move: {player}")

    computer = computer or random.choice(CHOICES)
    if computer not in CHOICES:
        raise ValueError(f"Unknown move: {computer}")

    if player == computer:
        result = "draw"
    elif BEATS[player] == computer:
        result = "player"
    else:
        result = "computer"
    return computer, result


def play() -> None:
    """Start the interactive terminal version of the game."""
    print("Rock, Paper, Scissors")

    while True:
        player = input("Choose rock (r), paper (p), scissors (s), or quit: ").strip().lower()
        player = {"r": "rock", "p": "paper", "s": "scissors"}.get(player, player)
        if player == "quit":
            print("Thanks for playing!")
            break
        if player not in CHOICES:
            print("Invalid choice. Try again.")
            continue

        computer, result = play_round(player)
        print(f"Computer chose {computer}.")
        print({"draw": "It's a tie!", "player": "You win!", "computer": "You lose!"}[result])

        if input("Play again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break


class RockPaperScissorsApp:
    """Tkinter desktop interface for Rock, Paper, Scissors.

    Args:
        root: The Tkinter root window that owns the application widgets.

    The application keeps scores for the current session and delegates the
    rules for each round to :func:`play_round`.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Create the game window and initialize a new score."""
        self.root = root
        self.root.title("Rock, Paper, Scissors")
        self.root.geometry("520x520")
        self.root.minsize(420, 460)
        self.root.configure(bg="#f8faff")

        self.player_score = 0
        self.computer_score = 0
        self.round_number = 1

        self.player_move = tk.StringVar(value="?")
        self.computer_move = tk.StringVar(value="?")
        self.round_label = tk.StringVar(value="ROUND 1")
        self.result = tk.StringVar(value="Make a move!")
        self.detail = tk.StringVar(value="Choose rock, paper, or scissors.")
        self.player_score_text = tk.StringVar(value="0")
        self.computer_score_text = tk.StringVar(value="0")

        self._configure_styles()
        self._build_interface()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Page.TFrame", background="#f8faff")
        style.configure("Title.TLabel", background="#f8faff", foreground="#202f49",
                        font=("Arial", 28, "bold"))
        style.configure("Subtitle.TLabel", background="#f8faff", foreground="#78849a",
                        font=("Arial", 11))
        style.configure("ScoreLabel.TLabel", background="#ffffff", foreground="#78849a",
                        font=("Arial", 9, "bold"))
        style.configure("Score.TLabel", background="#ffffff", foreground="#202f49",
                        font=("Arial", 28, "bold"))
        style.configure("ComputerScore.TLabel", background="#ffffff", foreground="#4666f4",
                        font=("Arial", 28, "bold"))
        style.configure("Move.TButton", font=("Arial", 12, "bold"), padding=(14, 10))
        style.configure("Action.TButton", font=("Arial", 10), padding=(10, 6))

    def _build_interface(self) -> None:
        page = ttk.Frame(self.root, style="Page.TFrame", padding=28)
        page.pack(fill="both", expand=True)

        ttk.Label(page, text="ROCK, PAPER, SCISSORS", style="Title.TLabel").pack(pady=(8, 4))
        ttk.Label(page, text="Read the room. Make your move.", style="Subtitle.TLabel").pack()

        score_card = tk.Frame(page, bg="#ffffff", highlightbackground="#e5e9f2",
                              highlightthickness=1, padx=30, pady=16)
        score_card.pack(fill="x", pady=(28, 16))
        score_card.columnconfigure(0, weight=1)
        score_card.columnconfigure(1, weight=1)
        score_card.columnconfigure(2, weight=1)
        self._add_score(score_card, "YOU", self.player_score_text, 0)
        tk.Label(score_card, text="VS", bg="#ffffff", fg="#9ba5b7",
                 font=("Arial", 10, "bold")).grid(row=0, column=1, rowspan=2)
        self._add_score(score_card, "COMPUTER", self.computer_score_text, 2, computer=True)

        arena = tk.Frame(page, bg="#ffffff", highlightbackground="#e5e9f2",
                         highlightthickness=1, padx=18, pady=18)
        arena.pack(fill="x")
        arena.columnconfigure(0, weight=1)
        arena.columnconfigure(1, weight=1)
        arena.columnconfigure(2, weight=1)
        self._add_fighter(arena, "YOU", self.player_move, 0)
        middle = tk.Frame(arena, bg="#ffffff")
        middle.grid(row=0, column=1, sticky="nsew")
        tk.Label(middle, textvariable=self.round_label, bg="#ffffff", fg="#4666f4",
                 font=("Arial", 9, "bold")).pack(pady=(7, 8))
        tk.Label(middle, textvariable=self.result, bg="#ffffff", fg="#202f49",
                 font=("Arial", 15, "bold"), wraplength=150).pack()
        tk.Label(middle, textvariable=self.detail, bg="#ffffff", fg="#78849a",
                 font=("Arial", 9), wraplength=150).pack(pady=(5, 0))
        self._add_fighter(arena, "COMPUTER", self.computer_move, 2, computer=True)

        ttk.Label(page, text="Choose your move", style="Subtitle.TLabel").pack(
            anchor="w", pady=(24, 8))
        buttons = ttk.Frame(page, style="Page.TFrame")
        buttons.pack(fill="x")
        for index, choice in enumerate(CHOICES):
            buttons.columnconfigure(index, weight=1)
            ttk.Button(
                buttons,
                text=f"{CHOICE_ICONS[choice]}  {choice.title()}",
                style="Move.TButton",
                command=lambda move=choice: self.play_round(move),
            ).grid(row=0, column=index, padx=4, sticky="ew")

        ttk.Button(page, text="↻  Reset game", style="Action.TButton",
                   command=self.reset_game).pack(pady=(22, 0))

    @staticmethod
    def _add_score(parent: tk.Frame, label: str, value: tk.StringVar, column: int,
                   computer: bool = False) -> None:
        tk.Label(parent, text=label, bg="#ffffff", fg="#78849a",
                 font=("Arial", 9, "bold")).grid(row=0, column=column)
        tk.Label(parent, textvariable=value, bg="#ffffff",
                 fg="#4666f4" if computer else "#202f49",
                 font=("Arial", 28, "bold")).grid(row=1, column=column, pady=(3, 0))

    @staticmethod
    def _add_fighter(parent: tk.Frame, label: str, move: tk.StringVar, column: int,
                     computer: bool = False) -> None:
        background = "#edf1ff" if computer else "#f6f7fb"
        tk.Label(parent, textvariable=move, bg=background, fg="#202f49",
                 font=("Arial", 30), width=3, height=1).grid(row=0, column=column, pady=(3, 8))
        tk.Label(parent, text=label, bg="#ffffff", fg="#78849a",
                 font=("Arial", 9)).grid(row=1, column=column)

    def play_round(self, player: str) -> None:
        """Play a round from the GUI and update its score and status labels.

        Args:
            player: The player's move: ``rock``, ``paper``, or ``scissors``.

        Raises:
            ValueError: If an invalid move is passed to the shared game logic.
        """
        computer, result = play_round(player)
        self.player_move.set(CHOICE_ICONS[player])
        self.computer_move.set(CHOICE_ICONS[computer])
        self.round_label.set(f"ROUND {self.round_number}")
        self.round_number += 1

        if result == "draw":
            self.result.set("It's a draw!")
            self.detail.set(f"Both chose {player}.")
        elif result == "player":
            self.player_score += 1
            self.player_score_text.set(str(self.player_score))
            self.result.set("You win!")
            self.detail.set(f"{player.title()} beats {computer}.")
        else:
            self.computer_score += 1
            self.computer_score_text.set(str(self.computer_score))
            self.result.set("Computer wins!")
            self.detail.set(f"{computer.title()} beats {player}.")

    def reset_game(self) -> None:
        """Reset scores, round state, move indicators, and result text."""
        self.player_score = 0
        self.computer_score = 0
        self.round_number = 1
        self.player_score_text.set("0")
        self.computer_score_text.set("0")
        self.player_move.set("?")
        self.computer_move.set("?")
        self.round_label.set("ROUND 1")
        self.result.set("Make a move!")
        self.detail.set("Choose rock, paper, or scissors.")


def launch_gui() -> None:
    """Create and run the Tkinter desktop interface."""
    root = tk.Tk()
    RockPaperScissorsApp(root)
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Rock, Paper, Scissors.")
    parser.add_argument("--gui", action="store_true", help="launch the desktop interface")
    args = parser.parse_args()
    if args.gui:
        launch_gui()
    else:
        play()
