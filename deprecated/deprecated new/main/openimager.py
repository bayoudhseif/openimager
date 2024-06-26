import webview
import subprocess

def run_balance():
    subprocess.Popen(["python", "levels/balance/balance.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "balance.py is running in a separate window."

def run_agility():
    subprocess.Popen(["python", "levels/agility/agility.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "agility.py is running in a separate window."

def run_dexterity():
    subprocess.Popen(["python", "levels/dexterity/dexterity.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "dexterity.py is running in a separate window."

def create_window():
    window = webview.create_window('Open Imager', fullscreen=True, html='''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Open Imager</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Add hover effect for buttons */
.level-container button:hover {
    transform: scale(1.1); /* Scale up on hover */
    transition: transform 0.3s ease; /* Smooth transition */
}

/* Add pulsating animation */
@keyframes pulse {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
    100% {
        transform: scale(1);
    }
}

.level-container button:focus {
    animation: pulse 1s infinite; /* Apply pulsating animation */
    outline: none; /* Remove default focus outline */
}

body {
    background: #1e1e1e url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAG0lEQVQYV2P8//+/FCMj4zMGJMCIzIGxKRQEAJgPBAbJqUVTAAAAAElFTkSuQmCC) repeat;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Montserrat', sans-serif;
}

.container {
    display: flex;
    align-items: flex-start;
}

.level-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.level-container button {
    margin: 10px;
    width: 200px;
    height: 200px;
    border: none;
    background-color: #ffffff7a;
    cursor: pointer;
    
}

.level-container button img {
    max-width: 80%;
    max-height: 80%;
}

.calling-card {
    margin: 10px;
    width: 450px;
    height: 640px;
    background-color: #ffffff7a; /* Changed background color */
    background-size: contain;
    background-position: center;
    font-size: 1rem; /* Set font size for text inside the calling card */
    text-align: center; /* Center-align text */
    overflow: hidden; /* Hide overflowing text */
    position: relative; /* Make the position relative for absolute positioning */
}

.calling-card img {
    max-width: 80%; /* Ensure the image doesn't exceed the boundaries of the calling card */
    max-height: 80%; /* Ensure the image doesn't exceed the boundaries of the calling card */
    position: absolute; /* Position the image absolutely within the calling card */
    top: 0; /* Position the image at the top of the calling card */
    left: 0; /* Position the image at the left of the calling card */
    bottom: 0; /* Position the image at the bottom of the calling card */
    right: 0; /* Position the image at the right of the calling card */
    margin: auto; /* Center the image horizontally and vertically */
}

.index {
    margin: 10px;
    width: 210px;
    height: 120px;
    background-color: #ffffff7a; /* Changed background color */
    background-size: contain;
    background-position: center;
    font-size: 2rem; /* Set font size for text inside the index */
    font-weight: 600; /* Set font weight for text inside the index */
    text-align: center; /* Center-align text */
    overflow: hidden; /* Hide overflowing text */
    color: #222222;

    /* Add flexbox properties */
    display: flex;
    justify-content: center;
    align-items: center;
}

.title {
    margin: 10px;
    width: 520px;
    height: 120px;
    background-color: #ffffff7a; /* Changed background color */
    background-size: contain;
    background-position: center;
    font-size: 3rem; /* Set font size for text inside the title */
    font-weight: 600; /* Set font weight for text inside the title */
    text-align: center; /* Center-align text */
    overflow: hidden; /* Hide overflowing text */
    color: #222222;

    /* Add flexbox properties */
    display: flex;
    justify-content: center;
    align-items: center;
}

.info-card {
    margin: 10px;
    padding: 20px; /* Add padding for better readability */
    width: 750px;
    height: 500px;
    background-color: #ffffff7a; /* Changed background color */
    font-size: 1.2rem; /* Increase font size for better readability */
    text-align: justify; /* Justify-align text for a cleaner look */
    overflow: hidden; /* Hide overflowing text */
}

.program-description {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.a {
    display: flex;
    align-items: center;
}

.program-container {
    display: flex;
    align-items: flex-start;
}

</style>
</head>
<body>

    <body onload="showProgram('BALANCE')">  <!-- Set the initial program to 'BALANCE' -->
        
    <div class="container">
        <div class="level-container">
            <button aria-label="BALANCE" onclick="showProgram('BALANCE')">
                <img src="source/images/balance.png" alt="balance">
            </button>
            <button aria-label="AGILITY" onclick="showProgram('AGILITY')">
                <img src="source/images/agility.png" alt="agility">
            </button>
            <button aria-label="DEXTERITY" onclick="showProgram('DEXTERITY')">
                <img src="source/images/dexterity.png" alt="dexterity">
            </button>
        </div>
        <div class="calling-card" id="calling-card">
            <img id="calling-card-image" src="" alt="Calling Card Image">
        </div>
        
        <div class="program-description">
            <div class="a">
                <div class="title" id="title"></div>
                <button class="index" onclick="pywebview.api.run_balance()">START</button>
            </div>
            <div class="info-card"></div>
        </div>
    </div>
    <div>
        <button onclick="pywebview.api.run_balance()">Run balance</button>
        <button onclick="pywebview.api.run_agility()">Run agility</button>
        <button onclick="pywebview.api.run_dexterity()">Run dexterity</button>
    </div>
    

<script>
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
</script>
</body>
</html>


    ''')
    window.expose(run_balance, run_agility, run_dexterity)
    webview.start()

if __name__ == '__main__':
    create_window()
