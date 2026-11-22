// ===============================
// Show Selected File Name
// ===============================

const fileInput = document.querySelector('input[type="file"]');

if(fileInput){

    fileInput.addEventListener("change",function(){

        if(this.files.length>0){

            alert("Selected File : " + this.files[0].name);

        }

    });

}

// ===============================
// Upload Animation
// ===============================

const form=document.querySelector("form");

if(form){

form.addEventListener("submit",function(){

const button=document.querySelector(".upload-btn");

button.innerHTML="⏳ Predicting...";

button.disabled=true;

});

}

// ===============================
// Card Animation
// ===============================

const cards=document.querySelectorAll(".card");

cards.forEach(function(card){

card.addEventListener("mouseenter",function(){

this.style.transform="translateY(-8px)";

});

card.addEventListener("mouseleave",function(){

this.style.transform="translateY(0px)";

});

});

// ===============================
// Result Cards
// ===============================

const resultCards=document.querySelectorAll(".result-card");

resultCards.forEach(function(card){

card.addEventListener("mouseenter",function(){

this.style.transform="scale(1.04)";

});

card.addEventListener("mouseleave",function(){

this.style.transform="scale(1)";

});

});