const socket = io(location.origin)

pixelContainer = document.getElementById("pixels")
scoreText = document.getElementById('score')
totalScoreText = document.getElementById('total-score')
lowFuelBox = document.getElementById("low-fuel")
fuelBar = document.getElementById('fuel')
connectionStatusText = document.getElementById("connection-status")
connectionStatusText.style.color = "orange"

const FUEL_MAX = 8
function drawFuel(fuel) {
    const fuelPercentage = fuel / FUEL_MAX * 100
    fuelBar.style.width = fuelPercentage + 'px'
}

colors = [
    ["red", [255, 0, 0]],
    ["orange", [255, 165, 0]],
    ["yellow", [255, 255, 0]],
    ["green", [0, 255, 0]],
    ["blue", [0, 0, 255]],
    ["indigo", [75, 0, 130]],
    ["violet", [238, 130, 238]],
    ["white", [255, 255, 255]],
]

let selectedColorButton = null
colors.forEach(([colorName, rgb]) => {
    const colorButton = document.createElement("button")
    colorButton.className = "color-button"
    const [r, g, b] = rgb
    colorButton.style.backgroundColor = `rgb(${r}, ${g}, ${b})`
    colorButton.addEventListener("click", () => {
        emit("change_color", rgb)
        if(selectedColorButton) {
            selectedColorButton.classList.remove("color-button-selected")
        }
        selectedColorButton = colorButton
        selectedColorButton.classList.add("color-button-selected")
    })
    document.getElementById("colors").appendChild(colorButton)
})

function getRange(min, max) {
    return Array.from({length: max - min + 1}, (_, i) => min + i)
}

getRange(0, 7).forEach(y => {
    const row = document.createElement("div")
    row.className = "row-" + y
    pixelContainer.appendChild(row)
    getRange(0, 7).forEach(x => {
        const pixel = document.createElement("div")
        pixel.id = "pixel-" + (y * 8 + x)
        pixel.className = "pixel"
        row.appendChild(pixel)
    })
})

socket.on('connect', () => {
    connectionStatusText.innerHTML = "Status: Connected"
    connectionStatusText.style.color = "green"

});

socket.on('disconnect', () => {
    connectionStatusText.innerHTML = "Status: Disconnected. Refresh page to reconnect"
    connectionStatusText.style.color = "red"
});

socket.on('low_fuel', (isLowFuel) => {
    if(isLowFuel) {
        lowFuelBox.classList.add("low-fuel-active")
    } else {
        lowFuelBox.classList.remove("low-fuel-active")
    }
});

socket.on('fuel', (fuel) => {
    drawFuel(fuel)
});

socket.on('score', (score) => {
    scoreText.innerHTML = "Score: " + score
});

socket.on('total_score', (totalScore) => {
    totalScoreText.innerHTML = "Total Score: " + totalScore
});

socket.on('pixels', (pixels) => {
    if(pixels) {
        pixels.forEach(([r, g, b], index)=>{
            const pixel = document.getElementById(`pixel-${index}`)
            pixel.style.backgroundColor = `rgb(${r}, ${g}, ${b})`
        })
    }
})

socket.on('reset', () => {
    scoreText.innerHTML = "Score: " + 0
    totalScoreText.innerHTML = "Total Score: " + 0
    lowFuelBox.disabled = true
    drawFuel(FUEL_MAX)
});

function emit(event, data) {
    if (socket.connected) {
        socket.emit(event, data)
    }
}

function changeColor(color) {
    emit('change_color', color)
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
