$(window).load(function () {
    // shuffle
    var $main = $("#shuffle-wrapper");
    $main.shuffle({
        itemSelector: ".item", // the selector for the items in the grid
    });

    /* reshuffle when user clicks a filter item */
    $("#filter a").click(function (e) {
        e.preventDefault();

        // set active class
        $("#filter a").removeClass("active");
        $(this).addClass("active");

        // get group name from clicked item
        var groupName = $(this).attr("data-group");

        // reshuffle grid
        $main.shuffle("shuffle", groupName);
    });

    // donate box
    if (
        $("#donate-modal").length &&
        $(".buttonDonate").length &&
        $(".donate-modal-close").length
    ) {
        $(document).on("click", ".buttonDonate", function () {
            $("#donate-modal").show();
        });
        $(document).on("click", ".donate-modal-close", function () {
            $("#donate-modal").hide();
        });
        $(document).on("click", "body", function (e) {
            if (e.target.id == $("#donate-modal").attr("id")) {
                $("#donate-modal").hide();
            }
        });
    }
});

$(function () {
    // window.scroll menu ite activated
    $(window).scroll(function () {
        activeMenuItem();
    });

    // function for active menuitem
    var sections = $("section"),
        nav = $("#nav"),
        nav_height = nav.outerHeight();

    function activeMenuItem() {
        var cur_pos = $(window).scrollTop() + 2;
        sections.each(function () {
            var top = $(this).offset().top - nav_height,
                bottom = top + $(this).outerHeight();

            if (cur_pos >= top && cur_pos <= bottom) {
                nav.find("ul > li > a").parent().removeClass("active");
                nav.find('a[href="#' + $(this).attr("id") + '"]')
                    .parent()
                    .addClass("active");
            } else if (cur_pos == 2) {
                nav.find("ul > li > a").parent().removeClass("active");
            }
        });
    }

    // smooth-scrolling click menu item
    $(function () {
        $("#navbar > ul > li > a").click(function () {
            if (
                location.pathname.replace(/^\//, "") ==
                    this.pathname.replace(/^\//, "") &&
                location.hostname == this.hostname
            ) {
                var target = $(this.hash);
                target = target.length
                    ? target
                    : $("[name=" + this.hash.slice(1) + "]");
                if (target.length) {
                    $("html, body").animate(
                        {
                            scrollTop: target.offset().top - 100,
                        },
                        500
                    );
                    return false;
                }
            }
        });
    });

    // home-slider
    $(".slider").owlCarousel({
        singleItem: true,
        autoPlay: true,
        navigation: true,
        navigationText: [
            '<i class="fa fa-angle-left">',
            '<i class="fa fa-angle-right">',
        ],
        mouseDrag: false,
    });

    // event animation
    $("#event .content .row:first .col:first").each(function () {
        var $this = $(this);
        var myVal = $(this).data("value");

        $this.appear(function () {
            $("#event #first-row .col:first").addClass("animated fadeInLeft");
        });
    });

    $("#event #second-row .col:last").each(function () {
        var $this = $(this);
        var myVal = $(this).data("value");

        $this.appear(function () {
            $("#event #second-row .col:last").addClass("animated fadeInRight");
        });
    });

    $("#event #last-row .col:last").each(function () {
        var $this = $(this);
        var myVal = $(this).data("value");

        $this.appear(function () {
            $("#event #last-row .col:first").addClass("animated fadeInLeft");
        });
    });

    // journal
    $(".journal .frame a").click(function (e) {
        e.preventDefault();
    });

    // gift-slider
    $(".gift-slider").owlCarousel({
        autoPlay: true,
        items: 3,
        itemsDesktop: [1199, 3],
        itemsDesktopSmall: [991, 2],
        itemsTabletSmall: [767, 1],
        pagination: false,
        mouseDrag: false,
    });

    // about Lightbox pluging
    $(".gallery .col a").nivoLightbox({allowfullscreen: true});

    // video-bg Lightbox pluging
    $(".video-bg a").nivoLightbox({allowfullscreen: true});

});
if ($("#wish-form").length) {
    $("#wish-form").validate({
        submitHandler: function (form) {
            // Let's find the input to check
            $.ajax({
                type: "GET",
                url: "/weddings/gui_loi_chuc/",
                success: function (data) {
                    if (data.token){
                        $.ajax({
                            type: "POST",
                            url: "/weddings/gui_loi_chuc/",
                            headers: {"X-CSRFToken": data.token},
                            data: $(form).serialize(),
                            success: function (data) {
                                if (data.is_valid) {
                                    form.reset();
                                    $("#wish-success").slideDown("slow");
                                } else {
                                    $("#wish-error").slideDown("slow");
                                    setTimeout(function () {
                                        $("#wish-error").slideUp("slow");
                                    }, 5000);
                                }
                            },
                            error: function () {
                                console.log('Error');
                                $("#wish-error").slideDown("slow");
                                setTimeout(function () {
                                    $("#wish-error").slideUp("slow");
                                }, 5000);
                            }
                        });
                    }
                }
            });
            return false;
        }
    });
}
