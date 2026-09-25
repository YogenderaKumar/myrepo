document.addEventListener("DOMContentLoaded", () => {
  const moves = {
    rock: { label: "Rock", icon: "✊", beats: "scissors" },
    paper: { label: "Paper", icon: "✋", beats: "rock" },
    scissors: { label: "Scissors", icon: "✌️", beats: "paper" }
  };
  const moveNames = Object.keys(moves);
  const playerScore = document.getElementById("player-score");
  const computerScore = document.getElementById("computer-score");
  const playerChoice = document.getElementById("player-choice");
  const computerChoice = document.getElementById("computer-choice");
  const resultMessage = document.getElementById("result-message");
  const resultDetail = document.getElementById("result-detail");
  const roundLabel = document.getElementById("round-label");
  const moveButtons = document.querySelectorAll("[data-move]");
  const resetButton = document.getElementById("reset-game");

  let scores = { player: 0, computer: 0 };
  let round = 1;

  function playRound(playerMove) {
    const computerMove = moveNames[Math.floor(Math.random() * moveNames.length)];
    const playerData = moves[playerMove];
    const computerData = moves[computerMove];
    const isDraw = playerMove === computerMove;
    const playerWon = !isDraw && playerData.beats === computerMove;

    if (isDraw) {
      resultMessage.textContent = "It's a draw!";
      resultDetail.textContent = `Both chose ${playerData.label.toLowerCase()}.`;
    } else if (playerWon) {
      scores.player += 1;
      resultMessage.textContent = "You win!";
      resultDetail.textContent = `${playerData.label} beats ${computerData.label.toLowerCase()}.`;
    } else {
      scores.computer += 1;
      resultMessage.textContent = "Computer wins!";
      resultDetail.textContent = `${computerData.label} beats ${playerData.label.toLowerCase()}.`;
    }

    playerScore.textContent = scores.player;
    computerScore.textContent = scores.computer;
    playerChoice.textContent = playerData.icon;
    computerChoice.textContent = computerData.icon;
    playerChoice.classList.toggle("is-winner", playerWon);
    computerChoice.classList.toggle("is-winner", !isDraw && !playerWon);
    roundLabel.textContent = `ROUND ${round}`;
    round += 1;
  }

  function resetGame() {
    scores = { player: 0, computer: 0 };
    round = 1;
    playerScore.textContent = "0";
    computerScore.textContent = "0";
    playerChoice.textContent = "?";
    computerChoice.textContent = "?";
    playerChoice.classList.remove("is-winner");
    computerChoice.classList.remove("is-winner");
    resultMessage.textContent = "Make a move!";
    resultDetail.textContent = "First to throw?";
    roundLabel.textContent = "ROUND 1";
  }

  moveButtons.forEach((button) => {
    button.addEventListener("click", () => playRound(button.dataset.move));
  });

  document.addEventListener("keydown", (event) => {
    const keyMoves = { r: "rock", p: "paper", s: "scissors" };
    const selectedMove = keyMoves[event.key.toLowerCase()];
    if (selectedMove) playRound(selectedMove);
  });

  resetButton.addEventListener("click", resetGame);
});
