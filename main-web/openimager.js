
function runBalance() {
    fetch('/run_balance')
        .then(response => response.text())
        .then(data => console.log(data));
}

function runAgility() {
    fetch('/run_agility')
        .then(response => response.text())
        .then(data => console.log(data));
}

function runDexterity() {
    fetch('/run_dexterity')
        .then(response => response.text())
        .then(data => console.log(data));
}


function showProgram(programName) {
    var callingCardImage = document.getElementById('calling-card-image');
    var title = document.getElementById('title');
    var infoCard = document.querySelector('.info-card');

    // Set image source, title, and description based on programName
    switch(programName) {
        case 'BALANCE':
            callingCardImage.src = "source/images/balance.png";
            title.textContent = "BALANCE";
            infoCard.innerHTML = "<p>Establishing a solid foundation of balance is often considered fundamental before advancing to more complex movements requiring agility and dexterity.</p>";
            break;
        case 'AGILITY':
            callingCardImage.src = "source/images/agility.png";
            title.textContent = "AGILITY";
            infoCard.innerHTML = "<p>Once a baseline of balance is achieved, agility training can help improve quickness, speed, and nimbleness in movements.</p>";
            break;
        case 'DEXTERITY':
            callingCardImage.src = "source/images/dexterity.png";
            title.textContent = "DEXTERITY";
            infoCard.innerHTML = "<p>Finally, dexterity can be honed to enhance fine motor skills and precision in tasks requiring intricate hand-eye coordination.</p>";
            break;
        default:
            callingCardImage.src = "";
            title.textContent = "";
            infoCard.innerHTML = "";
    }
}