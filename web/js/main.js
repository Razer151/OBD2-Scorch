var connection_button = document.getElementById("connect_button");
const RPM = document.getElementById("rpm");
const STATUS = document.getElementById("connectionStatus");
const FUEL = document.getElementById("fuel");
const SPEED = document.getElementById("speed");
const THROTTLE = document.getElementById("throttle");
const COOLANT = document.getElementById("coolant");
const WARNINGS = document.getElementById("warnings");
const SPINNER = document.getElementById("spinner");

connection_button.onclick = function() {
  updateStatus("...");
  eel.connect_obd();
}

eel.expose(promptAlerts);
function promptAlerts(description) {
  alert(description);
}

eel.expose(toggleWarning);
function toggleWarning(warn){
  if (warn) {
    WARNINGS.classList.remove("warningsOff");
    WARNINGS.classList.add("warningsOn");
  } else {
    WARNINGS.classList.remove("warningsOn");
    WARNINGS.classList.add("warningsOff");
  }
}

eel.expose(updateStatus);
function updateStatus(description) {
  STATUS.textContent = description;
}

eel.expose(play);
function play(filePath) {
  var audio = new Audio(filePath);
  audio.play();
}

eel.expose(updateReadout);
function updateReadout(rpm, throttle, coolant, speed, fuel) {
    RPM.textContent = rpm;
    FUEL.textContent = fuel;
    THROTTLE.textContent = throttle;
    COOLANT.textContent = coolant;
    SPEED.textContent = speed;
    SPINNER.style.opacity = (throttle*2)+"%";

}