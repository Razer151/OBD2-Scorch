var connection_button = document.getElementById("connect_button");
const RPM = document.getElementById("rpm");
const STATUS = document.getElementById("connectionStatus");
const FUEL = document.getElementById("fuel");
const SPEED = document.getElementById("speed");
const THROTTLE = document.getElementById("throttle");
const COOLANT = document.getElementById("coolant");
const WARNINGS = document.getElementById("warnings");
const POPUP = document.getElementById("popup");
const RPMTAC = document.getElementById("rpmTac");
const SPEEDTAC = document.getElementById("speedTac");

const GASBAR = document.getElementById("gasBar");
const THROTTLEBAR = document.getElementById("throttleBar");
var TOGGLE = true;


connectButton.onclick = function() {
  eel.connect_obd();
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

preset2.onclick = function() {
  eel.connect_obd_test();
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
  //STATUS.textContent = description;
}

eel.expose(play);
function play(filePath) {
  var audio = new Audio(filePath);
  audio.play();
}

eel.expose(updateReadout);
function updateReadout(rpm, throttle, coolant, speed, fuel, tac1, tac2) {
    RPM.textContent = rpm;
    FUEL.textContent = fuel;
    THROTTLE.textContent = throttle;
    COOLANT.textContent = coolant;
    SPEED.textContent = speed;


    RPMTAC.src= tac1;
    SPEEDTAC.src= tac2;
    //RPM.textContent = 'img/'+tacPercentage(rpm, 7500)+'.png';

    GASBAR.style.width = fuel+"%";
    THROTTLEBAR.style.width = throttle+"%";

}
