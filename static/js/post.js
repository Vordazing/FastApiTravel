// var contentCards = document.getElementsByClassName("content-card");
// var content = document.querySelector('.section-show-record');
// var closeButton_icone = document.querySelector('.section-show-record .icon-close');
//
// for (var i = 0; i < contentCards.length; i++) {
//     contentCards[i].addEventListener('click', function() {
//         content.style.display = 'block';
//     });
// }
//
// closeButton_icone.addEventListener('click', function() {
//     content.style.display = 'none';
// });

var contentCards = document.getElementsByClassName("content-card");
var content = document.querySelector('.section-show-record');
var closeButton_icone = document.querySelector('.section-show-record .icon-close');

for (var i = 0; i < contentCards.length; i++) {
    contentCards[i].addEventListener('click', function() {
        var postId = this.getAttribute('data-post-id'); // Получение значения data-post-id
        content.style.display = 'block';

        // Здесь вы можете выполнить POST-запрос к серверу, используя полученный postId
        // и вставить данные в открытое меню
        fetch('/' + postId, {
            method: 'POST'
        }) // Замените URL на ваше API-оконечное
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                // Вставка данных в открытое меню
                document.querySelector('.section-show-tittle h2').textContent = data.name;
                document.querySelector('.section-show-tittle a').textContent = data.data;
                document.querySelector('.show-info-Bd h4:nth-of-type(1)').textContent = data.country_name;
                document.querySelector('.show-info-Bd h4:nth-of-type(2)').textContent = data.territory_name;
                document.querySelector('.show-info-Bd h4:nth-of-type(3)').textContent = data.locality_name;
                document.querySelector('.show-info-Bd h4:nth-of-type(4)').textContent = data.category_name;

                document.querySelector('.text-description p').textContent = data.description;
            })
            .catch(function(error) {
                console.log(error);
            });
    });
}

closeButton_icone.addEventListener('click', function() {
    content.style.display = 'none';
    document.querySelector('.section-show-tittle h2').textContent = '';
    document.querySelector('.section-show-tittle a').textContent = '';
    document.querySelector('.show-info-Bd h4:nth-of-type(1)').textContent = '';
    document.querySelector('.show-info-Bd h4:nth-of-type(2)').textContent = '';
    document.querySelector('.show-info-Bd h4:nth-of-type(3)').textContent = '';
    document.querySelector('.show-info-Bd h4:nth-of-type(4)').textContent = '';
    document.querySelector('.text-description p').textContent = '';
});


