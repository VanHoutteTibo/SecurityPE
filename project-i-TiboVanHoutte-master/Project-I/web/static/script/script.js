"use strict"

let teller = 0



function init() {

  let twister = document.querySelector("#twister");
  let colors = ["#4B8640", "#F7D824", "#2689D9", "red"]
  let header = document.querySelector('#header');
  create_mat(twister, colors);
};


function create_mat_hulp(twister, colors) {

  create_mat(twister, colors);
};

function create_mat(twister, colors) {
  for (let i = 0; i < colors.length; i++) {
    console.log(colors[i])
    create_row(colors[i], twister);
  }
}

function create_row(color, twister) {
  console.log(color)
  let content;
  let header = document.querySelector('#header');
  let width = header.offsetWidth;
  console.log(width)
  // if (width >= 992) {
  content = '<div class="c-twister__row">'
  for (let i = 0; i < 6; i++) {
    teller++;
    console.log("test")
    content += '<div class="c-twister__item">'
    content += '<svg viewBox="52 52 102 102"> <circle cx="103" cy="103" r="50" stroke="' + color + '" stroke-width="3" fill="white" class="" id="'+ teller +'"/> </svg>';
    content += '</div>'
  }
  // }
  content += '</div>'
  twister.innerHTML += content
  // } else if (width < 992 && width >= 768) {
  //   for (let i = 0; i < 6; i++) {
  //     console.log("test")
  //     twister.innerHTML += '<svg class="c-bol"> <circle cx="34" cy="34" r="30" stroke="' + color + '" stroke-width="3" fill="white" /> </svg>';
  //   }
  // } else if (width < 768 && width >= 576) {
  //   for (let i = 0; i < 6; i++) {
  //     console.log("test")
  //     twister.innerHTML += '<svg class="c-bol"> <circle cx="24" cy="24" r="20" stroke="' + color + '" stroke-width="3" fill="white" /> </svg>';
  //   }
  // } else if (width < 576) {
  //   for (let i = 0; i < 6; i++) {
  //     console.log("test")
  //     twister.innerHTML += '<svg class="c-bol"> <circle cx="19" cy="19" r="15" stroke="' + color + '" stroke-width="3" fill="white" /> </svg>';
  //   }
  // }
}
// twister.innerHTML = '<br>';


init()