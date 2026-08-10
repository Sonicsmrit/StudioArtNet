const buttons = document.querySelectorAll(".studio-options button")
const check_button = document.querySelector(".check")
const leaderboard = document.querySelector("#leaderboard")
const timerText = document.querySelector("#timer-text");
const leftLine = document.querySelector(".timer-left");
const rightLine = document.querySelector(".timer-right");
const screen = document.querySelector(".studio-art-snippet");
const predic = document.querySelector("#ai-prediction")
let playerScore = 0;
let aiScore = 0;
let timeLeft = 20;
let timer;
let startgaming = false;
let current_round = null;
let roundActive = false;
let lastAi_perd = null
let lastcorrect = null

async function  getResponse() {

    try{

        const response = await fetch("http://127.0.0.1:8000/predict")
        if (!response.ok) {
            throw new Error("API request failed");
        }
        const data = await response.json()

        return data
    }
    catch(error){
        console.error("API Error: ", error)
    }
    
}


buttons.forEach(function(button) {
    button.addEventListener("click", function() {

        const wasSelected = button.classList.contains("selected")

        buttons.forEach(function(btn){
            btn.classList.remove("selected");
        })

        if (!wasSelected) {
            button.classList.add("selected");
            check_button.classList.add("check-select");
        } 
        else {
            check_button.classList.remove("check-select");
        }
        
    });
});

function scoreRound(){

    const useranswer = document.querySelector(".studio-options button.selected")

    let selectedStudio;

    if (!useranswer) {
        selectedStudio = "idk";
    } 
    else {
        selectedStudio = useranswer.value;
    }
    
    if(selectedStudio === current_round.real_studio && current_round.studio_prediction === current_round.real_studio){

        playerScore+=1
        aiScore+=1

    }
    else if(selectedStudio === current_round.real_studio && current_round.studio_prediction !== current_round.real_studio){
        playerScore +=1
        
    }
    else if(selectedStudio !== current_round.real_studio && current_round.studio_prediction === current_round.real_studio){
        aiScore += 1
    }

}

check_button.addEventListener("click", function(){
    check_button.classList.add("selected");

    setTimeout(function(){
        check_button.classList.remove("selected");

    }, 2000)

    scoreRound();
    nextRound();

})

const updateleaderboard=()=>{

    if (playerScore >= aiScore) {
        leaderboard.innerHTML = `
            <p class="leaderboard-player">1. You — ${playerScore}</p>
            <p class="leaderboard-ai">2. AI — ${aiScore}</p>
        `;
    } else {
        leaderboard.innerHTML = `
            <p class="leaderboard-ai">1. AI — ${aiScore}</p>
            <p class="leaderboard-player">2. You — ${playerScore}</p>
        `;
    }

}

function startingScreen(){
    screen.innerHTML = `
    <div class="startingScreen">
    <h2>Wanna Start Beating the AI's Ass?</h2>
    <button value="startgame">Start Game</button>
    </div>
    `
    screen.style.backgroundColor = "black"
}

function nextRound(){
    if (!roundActive) return;

    roundActive = false;

    clearInterval(timer);
    updateleaderboard();

    buttons.forEach(function(btn){
        btn.classList.remove("selected");
    });
    check_button.classList.remove("check-select");

    setTimeout(startGame, 1500);
}


function settimer(){

    timeLeft = 20;
    roundActive = true
    timerText.textContent = timeLeft;

    leftLine.style.transform = "scaleX(1)";
    rightLine.style.transform = "scaleX(1)";

    timer = setInterval(function() {

        timeLeft--;

        timerText.textContent = timeLeft;

        const progress = timeLeft / 20;

        if(timeLeft<11){
            leftLine.style.backgroundColor = "yellow";
            rightLine.style.backgroundColor = "yellow";
        }

        if(timeLeft<6){
            leftLine.style.backgroundColor = "red";
            rightLine.style.backgroundColor = "red";

        }

        leftLine.style.transform = `scaleX(${progress})`;
        rightLine.style.transform = `scaleX(${progress})`;

        

        if (timeLeft <= 0) {
            clearInterval(timer);
            scoreRound();
            nextRound()
        }

    }, 1000);

}


async function startGame() {

    current_round = await getResponse();

    if (!current_round) {
        return;
    }

    screen.innerHTML = `<img src="${current_round.image}">`;

    if (lastAi_perd !== null) {
        predic.innerHTML = `<p class="ai">AI prediction was: ${lastAi_perd}</p>
        <h3 class="correct-answer">Correct studio was: ${lastcorrect}</h3>`;
    } else {
        predic.innerHTML = `<h3 class="firstround">First round: no previous guess yet</h3>`;
    }

    lastAi_perd = current_round.studio_prediction;
    lastcorrect = current_round.real_studio;


    settimer();
    
}

function game(){
    if(!startgaming){
        startingScreen()
    }
    
    const startButton = document.querySelector(".startingScreen button")

    startButton.addEventListener("click", async function(){
        startgaming = true
        document.querySelector(".startingScreen").remove();

        await startGame();
        


    })

}


game()
updateleaderboard()


