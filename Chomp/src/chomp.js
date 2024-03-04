let turn = 0;
const player = ["first", "second"];

function chomp(matrix, r, c) {
  for (let i = r; i < matrix.length; i += 1) {
    matrix[i].splice(c, matrix[i].length - c);
  }
  return matrix.filter((row) => row.length > 0);
}

function checkWinner(matrix) {
  return matrix.length === 1 && matrix[0].length === 1;
}

function selectBlock(gameboard, row, col) {
  if (!(row === 0 && col === 0)) {
    const newGameboard = chomp(gameboard, row, col);
    if (checkWinner(newGameboard)) {
      document.getElementById("message").innerText = `The winner is the ${
        player[turn % 2]
      } player!`;
    } else {
      turn += 1;
      document.getElementById("message").innerText = `The ${
        player[turn % 2]
      } player turn to select!`;
    }
    return newGameboard;
  }
  if (!checkWinner(gameboard)) {
    document.getElementById(
      "message"
    ).innerText = `You can not choose the poisonous cell, still ${
      player[turn % 2]
    } player turn to select!`;
  }
  return gameboard;
}

function printChocolateBar(gameboard, noListener) {
  const gameboardHolder = document.getElementById("gameboardHolder");
  // Rensar tidigare innehåll
  gameboardHolder.innerHTML = "";
  for (let i = 0; i < gameboard.length; i += 1) {
    const divrow = document.createElement("div");
    divrow.setAttribute("class", "row");
    for (let j = 0; j < gameboard[i].length; j += 1) {
      const divblock = document.createElement("div");
      divblock.innerHTML = gameboard[i][j];
      divrow.appendChild(divblock);
      if (noListener === undefined)
        divblock.addEventListener("click", () => {
          const newGameboard = selectBlock(gameboard, i, j);
          printChocolateBar(newGameboard);
        });
    }
    gameboardHolder.appendChild(divrow);
  }
  gameboardHolder.appendChild(document.createElement("br"));
}

// Funktion för att skapa board
function createChocolateBar(r, c) {
  if (r > 0 && c > 0) {
    const matrix = []; // gör en tom array

    for (let i = 0; i < r; i += 1) {
      matrix[i] = []; // för varje index i den arrayen skapar vi ännu en tom array, så att vi får matrisform
      for (let j = 0; j < c; j += 1) {
        matrix[i][j] = `${i + 1}${j + 1}`;
      }
    }

    matrix[0][0] = "P ";
    printChocolateBar(matrix);
    return matrix;
  }
  return undefined;
}

const gameboard = createChocolateBar(6, 7);
printChocolateBar(gameboard);

document.getElementById("message").innerText = `Welcome to Chomp! The ${
  player[turn % 2]
} player starts to select`;
