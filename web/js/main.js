var connection_button = document.getElementById("connect_button");
const RPM = document.getElementById("rpm");
const STATUS = document.getElementById("connectionStatus");
const FUEL = document.getElementById("fuel");
const SPEED = document.getElementById("speed");
const THROTTLE = document.getElementById("throttle");
const COOLANT = document.getElementById("coolant");
const WARNINGS = document.getElementById("warnings");
const SPINNER = document.getElementById("spinner");
const POPUP = document.getElementById("popup");
var TOGGLE = true;

connectButton.onclick = function() {
  updateStatus("...");
  eel.connect_obd();
}

toggleButton.onclick = function() {
  TOGGLE = !TOGGLE;
  toggleWarning(TOGGLE);

}

playLine1.onclick = function() {
    toggleCritical(true);
    toggleWarning(true);
    TOGGLE = true;
    play("../voices/scorch/d" + 1 + ".mp3");
}
playLine2.onclick = function() {
  toggleCritical(false);
  toggleWarning(false);
    play("../voices/scorch/" + 1 + ".mp3");
}
preset1.onclick = function() {
  document.documentElement.style.setProperty('--trim1', 'orange');
  document.documentElement.style.setProperty('--trim2', 'cyan');
}
preset2.onclick = function() {
  document.documentElement.style.setProperty('--trim1', 'red');
  document.documentElement.style.setProperty('--trim2', 'red');
}
preset3.onclick = function() {
  document.documentElement.style.setProperty('--trim1', 'white');
  document.documentElement.style.setProperty('--trim2', 'white');
}
preset4.onclick = function() {
  document.documentElement.style.setProperty('--trim1', 'purple');
  document.documentElement.style.setProperty('--trim2', 'purple');
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

eel.expose(toggleCritical);
function toggleCritical(critical){
  if(critical){
    POPUP.classList.remove("popupOff");
    POPUP.classList.add("popupOn");
  } else {
    POPUP.classList.remove("popupOn");
    POPUP.classList.add("popupOff");
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
