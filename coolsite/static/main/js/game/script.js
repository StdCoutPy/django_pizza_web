const cardContents = [
  "lollipop",
  "lollipop",
  "cat",
  "cat",
  "bat",
  "bat",
  "potion",
  "potion",
  "mummy",
  "mummy",
  "pumpkin",
  "pumpkin",
  "ghost",
  "ghost",
  "witch",
  "witch"
];

const referenceTable = [
  {
    name: "lollipop",
    image: "https://i.ibb.co/4V69tNC/lollipop.png"
  },
  {
    name: "cat",
    image: "https://i.ibb.co/wcQK3PT/black-cat.png"
  },
  {
    name: "bat",
    image: "https://i.ibb.co/Wfh0fkz/bat.png"
  },
  {
    name: "potion",
    image: "https://i.ibb.co/3B710fy/potion.png"
  },
  {
    name: "mummy",
    image: "https://i.ibb.co/6PnwXHx/mummy.png"
  },
  {
    name: "pumpkin",
    image: "https://i.ibb.co/PFRwFVg/pumpkin.png"
  },
  {
    name: "ghost",
    image: "https://i.ibb.co/RP4TWh1/ghost.png"
  },
  {
    name: "witch",
    image: "https://i.ibb.co/tchtW0p/witch.png"
  }
];

var winConditionMet = false;
var totalFlips = 0
var cardsFlipped = 0;
const cardList = Array.from(document.querySelectorAll('.card'))
const cards = Array.from(document.getElementsByClassName("back"));

const ogLength = cardContents.length;
const resetBtn = document.getElementById('restart')
const replayBtn = document.getElementById('replay')
const newGame = document.getElementById('new_game')
// pseudocode
// shuffle array contents and divide them amongst the cards
// when a card is clicked reveal it
// keep a count of number of cards revealed
// when another card is clicked reveal it
// if the names of the cards match, turn them orange and leave them flipped, reset number, disable click
// if they dont match turn them back around and reset number


function shuffle(){
  winConditionMet = false;
  totalFlips = 0
document.getElementById('num_flips').innerHTML = totalFlips
  const currentArray = [...cardContents]
  cardList.forEach(card=>{       if(card.classList.contains('flipped') || card.classList.contains('success')){
     
     setTimeout(function(){
card.classList.remove('success')
       card.querySelector(".back").style.backgroundColor = "#E5E5E5"
       card.querySelector('.card_inner').style.transform = "none"   
  card.style.removeProperty('pointer-events')            
    card.classList.remove('flipped')
         
}, 100); 
          }
        })
  for (let i = 0; i < ogLength; i++) {
  var randomElement =
    currentArray[Math.floor(Math.random() * currentArray.length)];

  //we now have a random element
  //look for this element in the reference table
  let relevantObj = referenceTable.find((obj) => obj.name === randomElement);
  let relevantImage = relevantObj.image;
  //   put this image on the back of the card
  cards[i].innerHTML = "<img src=" + relevantImage + "/>";
  //remove this element from the original array we were working with
  let index = currentArray.indexOf(randomElement);
  currentArray.splice(index, 1);
}
}

//lets add a click functionality and

// lets add a flipped count
document.querySelectorAll(".card").forEach((item) => {
  item.addEventListener("click", () => {
    let child = item.querySelector(".card_inner");
    if (cardsFlipped < 2) {
      totalFlips++
      document.getElementById('num_flips').innerHTML = totalFlips
      child.style.transform = "rotateY(180deg)";
      item.classList.add("flipped");
    }
    if (cardsFlipped == 1) {
      //compare and reset
      let currentFlipped = document.querySelectorAll(".flipped");
      //time to compare
      const first = currentFlipped[0].querySelector("img").getAttribute("src");
      const second = currentFlipped[1].querySelector("img").getAttribute("src");
      if (first === second) {
        //match!
        currentFlipped.forEach((current) => {
         setTimeout(function(){
            current.querySelector(".back").style.backgroundColor = "#FCA311";
         },150)
          current.style.pointerEvents = "none";
          current.classList.remove("flipped");
          current.classList.add("success")
          
          

          //reset
          cardsFlipped = -1;
        });
      }else if(first !== second){
        //hide all the cards again
        cardsFlipped = -1
        //take all the cards
        let cardlist = document.querySelectorAll('.card')
        cardlist.forEach(card=>{       if(card.classList.contains('flipped')){
     setTimeout(function(){card.querySelector('.card_inner').style.transform = "none"
         
}, 300); card.classList.remove('flipped')
          }
        })
        
      }
      
    }
    
    cardsFlipped++;
    
//have all the cards been found?
          let successfulFlips = Array.from(document.querySelectorAll('.success'))
          if(successfulFlips.length === ogLength){
  winConditionMet = true;          document.getElementById('shield').style.display = 'block'
            document.getElementById('success_modal').style.display='block'
          }
                                     
  });
});


  resetBtn.addEventListener('click',()=>{
    shuffle()
  })

replayBtn.addEventListener('click',()=>{ document.getElementById('shield').style.display = 'none'
            document.getElementById('success_modal').style.display='none'
      
                                        shuffle()
  
})

newGame.addEventListener('click',()=>{

  shuffle()
})

//on page load
shuffle()