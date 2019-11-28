$(".carousel-control-prev").mouseEnter(function (event) {
    $(this).addClass("animated bounce");
});
$(document).ready(function () {
    $('.carousel-control-prev').hover(function () {
        $(this).addClass('animated bounce');
    });
});