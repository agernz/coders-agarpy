var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var endRad = Math.PI << 1;

function drawCircle(x, y, radius, color) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, endRad);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
}

function drawPlayer(x, y, radius, name) {
  drawCircle(x, y, radius, 'green')
  // add name
  // add sight circle
}

function drawGame(data) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // add end game scenario
  if (!data.running) {
    clearInterval(game_interval);
    return;
  }
  data.player_data.forEach(player => {
    drawPlayer(player[0], player[1], player[2], player[3])
  })
  data.food_data.forEach(food => {
    drawCircle(food[0], food[1], food[2], 'blue')
  })
}

function getGameState() {
    $.get('/updateGame', drawGame)
}

var game_interval = setInterval(getGameState, 100);