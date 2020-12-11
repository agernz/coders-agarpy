var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var endRad = Math.PI * 2;

var CANVAS_WIDTH = 640;
var CANVAS_HEIGHT = 500;

var PLAYABLE_DISPLAY_WIDTH = 640;
var PLAYABLE_DISPLAY_HEIGHT = 320;

function onStartButton() {
  socket.emit('restart', {});
}

function drawCircle(x, y, radius, color) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, endRad);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
}

function drawVisionCircle(x, y, color) {
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.arc(x, y, 100, 0, endRad);
    ctx.stroke();
    ctx.closePath()
}

function drawBoard() {
    for (var x = 0; x <= PLAYABLE_DISPLAY_WIDTH; x += 40) {
        ctx.moveTo(0.5 + x, 0);
        ctx.lineTo(0.5 + x, PLAYABLE_DISPLAY_HEIGHT);
    }

    for (var x = 0; x <= PLAYABLE_DISPLAY_HEIGHT; x += 40) {
        ctx.moveTo(0, 0.5 + x);
        ctx.lineTo(PLAYABLE_DISPLAY_WIDTH, 0.5 + x);
    }
    ctx.strokeStyle = "lightgrey";
    ctx.stroke();
}

function drawScoreBoard() {
    ctx.beginPath();
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 320, 640, 180);
    ctx.closePath();
}

function drawTimer(time) {
    ctx.font = "30px Arial";
    ctx.fillText(time + ' seconds left', 220, 360);
}

function drawPlayer(x, y, radius, color) {
    drawCircle(x, y, radius, color);
    drawVisionCircle(x, y, color);
}

function drawScore(score, name, index) {
    ctx.font = "16px Arial";
    var yIndex = Math.floor(index / 5);
    var xStartingPoint = 10;
    var yOffset = 400;
    ctx.fillText(name + ' : ' + Math.round(score),
        xStartingPoint + (120 * index) % 600,
        yOffset + (yIndex * 30));
}

function drawGame(data) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (!data.running) {
      ctx.font = "50px Arial";
      ctx.fillText(data.top_player + ' Wins!', 200, 260);
      return;
    }
    drawBoard();
    drawScoreBoard();
    var player_count = 0;
    data.player_data.forEach(player => {
        var player_color = '#' + player.color;
        drawPlayer(player.x, player.y, player.radius, player_color);
        drawScore(player.score, player.name, player_count);
        player_count += 1;
    });
    data.food_data.forEach(food => {
        drawCircle(food[0], food[1], food[2], 'black');
    });
    drawTimer(data['timer']);
}

var socket = io();
socket.on('connect', function() {
    socket.emit('connected', {data: 'Socket connection established!'});
});

socket.on('update_game', drawGame);