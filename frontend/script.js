const buttons = document.querySelectorAll(".studio-options button")
const check_button = document.querySelector(".check")

buttons.forEach(function(button) {
    button.addEventListener("click", function() {

        buttons.forEach(function(btn){
            btn.classList.remove("selected");
        })

        button.classList.add("selected");
        
        check_button.classList.add("check-select");
    });
});

check_button.addEventListener("click", function(){
    check_button.classList.add("selected");

    setTimeout(function(){
        check_button.classList.remove("selected");

    }, 2000)
    
})


