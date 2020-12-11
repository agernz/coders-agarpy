var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var endRad = Math.PI << 1;

var CANVAS_WIDTH = 640;
var CANVAS_HEIGHT = 500;

var PLAYABLE_DISPLAY_WIDTH = 640;
var PLAYABLE_DISPLAY_HEIGHT = 320;

function drawCircle(x, y, radius, color) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, endRad);
    ctx.fillStyle = ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
}

function drawVisionCircle(x, y, color) {
    ctx.beginPath();
    ctx.strokeStyle = '#' + color;
    ctx.arc(x, y, 100, 0, 2 * Math.PI);
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

function drawPlayer(x, y, radius, name, color) {
    drawCircle(x, y, radius, '#' + color)
    // add sight circle
}

function drawScore(score, name, index) {
    ctx.font = "16px Arial";
    var yIndex = Math.floor(index / 5);
    xStartingPoint = 10;
    yOffset = 400;
    ctx.fillText(name + ' : ' + Math.round(score),
        xStartingPoint + (120 * index) % 600,
        yOffset + (yIndex * 30));
}

function sortPlayers(data) {
    new_data = data.sort((a, b) => {
        var sortOrder = 0;
        if (a[2] > b[2]) {
            sortOrder = 1
        } else if (a[2] < b[2]) {
            sortOrder = -1
        }
        return sortOrder
    });
    return new_data;
}

function drawGame(data) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // add end game scenario
    if (!data.running) {
        clearInterval(game_interval);
        return;
    }
    drawBoard();
    drawScoreBoard();
    data.player_data = sortPlayers(data.player_data).reverse()
    player_count = 0
    data.player_data.forEach(player => {
        drawPlayer(player[0], player[1], player[2], player[3], player[4]);
        drawVisionCircle(player[0], player[1], player[4]);
        drawScore(player[2], player[3], player_count);
        player_count += 1;
    });
    data.food_data.forEach(food => {
        drawCircle(food[0], food[1], food[2], 'black')
    });
    drawTimer(data['timer']);

}

function getGameState() {
    $.get('/updateGame', drawGame)
}

var game_interval = setInterval(getGameState, 100);
