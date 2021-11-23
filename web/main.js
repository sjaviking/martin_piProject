const socket = io("http://pearpie.is-very-sweet.org:5001/" || location.origin)

connectionStatusText = document.getElementById("connection-status")
connectionStatusText.style.color = "orange"

socket.on('connect', () => {
    connectionStatusText.innerHTML = "Status: Connected"
    connectionStatusText.style.color = "green"

});

socket.on('disconnect', () => {
    connectionStatusText.innerHTML = "Status: Disconnected. Refresh page to reconnect"
    connectionStatusText.style.color = "red"
});

function emit(event) {
    if (socket.connected) {
        socket.emit(event)
    }
}

function colorize(direction, color) {
    document.getElementById(direction + '-arrow').style.color = color
}

window.addEventListener('keydown', (event) => {
    if (!event.repeat) {
        switch (event.key) {
            case "ArrowLeft":
                emit('move_left')
                colorize("left", "red")
                // Left pressed
                break;
            case "ArrowRight":
                emit('move_right')
                colorize("right", "red")
                break;
            case "ArrowUp":
                // Up pressed
                break;
            case "ArrowDown":
                // Down pressed
                break;
        }
    }
})

window.addEventListener('keyup', (event) => {
    if (!event.repeat) {
        switch (event.key) {
            case "ArrowLeft":
                emit('stop_moving_left')
                colorize("left", "inherit")
                break;
            case "ArrowRight":
                emit('stop_moving_right')
                colorize("right", "inherit")
                break;
            case "ArrowUp":
                // Up pressed
                break;
            case "ArrowDown":
                // Down pressed
                break;
        }
    }
})