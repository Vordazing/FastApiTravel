var text1Element = document.getElementById("text1");
var text2Element = document.getElementById("text2");

var texts1 = ["Никогда не останавливайся", "Путешествуй", "Покоряй горы, плавай в море"];
var texts2 = ["Исследуя мир!", "чтобы найти себя и узнать мир вокруг тебя", "и исследуй мир своими глазами!"];

var counter1 = 0;
var counter2 = 0;

function changeTexts() {
    text1Element.style.opacity = 0;
    text2Element.style.opacity = 0;

    setTimeout(function() {
        text1Element.textContent = texts1[counter1];
        text2Element.textContent = texts2[counter2];

        text1Element.style.opacity = 1;
        text2Element.style.opacity = 1;
    }, 500);

    counter1++;
    counter2++;

    if (counter1 >= texts1.length) {
        counter1 = 0;
    }

    if (counter2 >= texts2.length) {
        counter2 = 0;
    }
}

setInterval(changeTexts, 3000);

var toggleElement = document.querySelector('.toggle');
var menuElement = document.querySelector('.menu');

toggleElement.addEventListener('click', function() {
    toggleElement.classList.toggle('active');
    menuElement.classList.toggle('active');
});


const loginButton = document.querySelector('#login a');
const loginSection = document.querySelector('.wrapper');
const homeLink = document.querySelector('.menu li.home a');
const helpLink = document.querySelector('.menu li:nth-child(3) a');
const closeButton = document.querySelector('.icon-close');
const searchSection = document.querySelector('.input-search-filter-container');


loginButton.addEventListener('click', function(event) {
    event.preventDefault();

    loginSection.style.display = 'block';
    loginButton.style.color = 'limegreen';
    homeLink.style.color = 'white';
    document.body.style.overflow = 'hidden';

    helpLink.style.pointerEvents = 'none';
    searchSection.classList.add('disabled');


});

closeButton.addEventListener('click', function() {
    loginSection.style.display = 'none';
    loginButton.style.color = '';
    homeLink.style.color = '';
    helpLink.style.pointerEvents = '';
    closeButton.removeEventListener('click', this);
    document.body.style.overflow = 'auto';
    searchSection.classList.remove('disabled');

});

