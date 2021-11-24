const socket = io(location.origin)

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

function emit(event, data) {
    if (socket.connected) {
        socket.emit(event, data)
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

const DEADZONE = 5
const ANGLE_SPAN = 40
const MAX_ANGLE = ANGLE_SPAN * 2
const CAR_MAX_POSITION = 7
const CAR_MIN_POSITION = 0

let enableGyro = false
let carPosition = 3

function carPositionFrom(angle) {
    if (angle > ANGLE_SPAN) {
        return CAR_MAX_POSITION
    }
    if (angle < -ANGLE_SPAN) {
        return CAR_MIN_POSITION
    }
    if((angle > -DEADZONE) && (angle < DEADZONE)) {
        return carPosition
    }
    const absoluteAngle = angle + ANGLE_SPAN
    return Math.round((absoluteAngle / MAX_ANGLE * (CAR_MAX_POSITION - CAR_MIN_POSITION)) + CAR_MIN_POSITION)
}

function onOrientation(event){
        // const x = event.alpha
        const y = event.beta
        // const z = event.gamma
        const newCarPosition = carPositionFrom(y)
        if(newCarPosition != carPosition) {
            carPosition = newCarPosition
            emit('move_to', carPosition)
        }
}

function onToggleGyro() {
    enableGyro = !enableGyro
    button = document.getElementById("toggle-gyro-button")
    button.innerHTML = enableGyro ? "Disable Gyro" : "Enable Gyro"
    button.style.backgroundColor = enableGyro ? "green" : "rgb(78, 25, 25)"
    if(enableGyro) {
        window.addEventListener('deviceorientation', onOrientation)
    } else {
        window.removeEventListener('deviceorientation', onOrientation)
    }
}
