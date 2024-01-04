/*
Copyright (c) 2021
------------------------------------------------------------------
[Master Javascript]

Project: Wedding Template

-------------------------------------------------------------------*/
(function($) {
    "use strict";
    var wedding = {
        initialised: false,
        version: 1.0,
        mobile: false,
        init: function() {

            if (!this.initialised) {
                this.initialised = true;
            } else {
                return;
            }
            /*-------------- wedding Functions Calling ---------------------------------------------------
            ------------------------------------------------------------------------------------------------*/
            this.RTL();
            this.Revealslider();
            this.Fancybox();
            this.Countdown();
            // this.SmoothScroll();
            this.OwlCarousel();
            this.RsvpForm();
            this.MainPage();
            this.MainMenu();
            this.ClockCounting();
            // this.Stellar();

        },

        /*-------------- wedding Functions definition ---------------------------------------------------
        ---------------------------------------------------------------------------------------------------*/
        RTL: function() {
            // On Right-to-left(RTL) add class
            var rtl_attr = $("html").attr('dir');
            if (rtl_attr) {
                $('html').find('body').addClass("rtl");
            }
        },
        //Top Revolution Slider
        Revealslider: function() {
            var revapi;
            revapi = jQuery("#rev_slider").revolution({
                sliderType: "standard",
                sliderLayout: "fullscreen",
                fullScreenOffset: "50px",
                delay: 9000,
                navigation: {
                    arrows: {
                        enable: true
                    }
                },
                gridwidth: 1230,
                gridheight: 720
            });
        },
        //fancybox
        Fancybox: function() {
            $(".fancybox").fancybox();
            $("a.inline").fancybox({
                'hideOnContentClick': true,
                'overlayColor': '#6b0202',
                'overlayOpacity': 0.8
            });
        },
        //Countdown
        Countdown: function() {
            $('.timer').each(count);

            function count(options) {
                var $this = $(this);
                options = $.extend({}, options || {}, $this.data('countToOptions') || {});
                $this.countTo(options);
            }
        },
        //SmoothScroll
        SmoothScroll: function() {
            $.smoothScroll();
        },
        //OwlCarousel
        OwlCarousel: function() {
            var owl = $("#owl_man_family");
            owl.owlCarousel({
                items: 2, //10 items above 1000px browser width
                itemsDesktop: [1000, 2], //5 items between 1000px and 901px
                itemsDesktopSmall: [900, 2], // betweem 900px and 601px
                itemsTablet: [600, 2], //2 items between 600 and 0
                itemsMobile: false, // itemsMobile disabled - inherit from itemsTablet option
                loop: true
            });

            // var owl = $('#owl_man_family');
            // owl.owlCarousel({
            //     items:2,
            //     loop:true,
            //     margin:10,
            //     autoplay:true,
            //     nav: false,
            //     autoplayTimeout:1000,
            //     autoplayHoverPause:true
            // });
            // $('.play').on('click',function(){
            //     owl.trigger('play.owl.autoplay',[1000])
            // })
            // $('.stop').on('click',function(){
            //     owl.trigger('stop.owl.autoplay')
            // })


            var owl = $("#owl_woman_family");
            owl.owlCarousel({
                items: 2, //10 items above 1000px browser width
                itemsDesktop: [1000, 2], //5 items between 1000px and 901px
                itemsDesktopSmall: [900, 2], // betweem 900px and 601px
                itemsTablet: [600, 2], //2 items between 600 and 0
                itemsMobile: [250, 1], // itemsMobile disabled - inherit from itemsTablet option
                loop: true
            });
            //gallery
            var owl = $("#owl-gallery");

            owl.owlCarousel({
                loop: true,
                items: 4,
                dots: false,
                nav: false,
                autoHeight: true,
                touchDrag: true,
                mouseDrag: true,
                autoplay: true,
                navText: ['<i class="flaticon-direction196"></i>', '<i class="flaticon-right138"></i>'],
                responsive: {
                    0: {
                        items: 1,
                    },
                    480: {
                        items: 2,
                    },
                    768: {
                        items: 3,
                    },
                    1068: {
                        items: 4,
                    }
                }

            });
        },
        //rsvp section
        RsvpForm: function() {
            var theForm = document.getElementById('theForm');

            new stepsForm(theForm, {
                onSubmit: function(form) {
                    // hide form
                    classie.addClass(theForm.querySelector('.simform-inner'), 'hide');
                    /*
                    form.submit()
                    or
                    AJAX request (maybe show loading indicator while we don't have an answer..)
                    */
                    // let's just simulate something...
                    var messageEl = theForm.querySelector('.final-message');
                    messageEl.innerHTML = 'Thank you! Your Message is successfully sent.';
                    classie.addClass(messageEl, 'show');
                }
            });
        },
        //MainPage
        MainPage: function() {
            $(".page").hide();
            $(".onclick_show_site").click(function() {
                $(".page").fadeIn(4000);
                $(".wd_main_container").slideUp(1000);
            });
        },
        //For Menu Toggle
        MainMenu: function() {
            var $page = $('.page');
            $('.menu_toggle').on("click", function() {
                $page.toggleClass('wd_menu_container');
            });
            $('.content').on("click", function() {
                $page.removeClass('wd_menu_container');
            });
            $('a.page-scroll').on('click', function() {
                $('li a.active').removeClass('active');
                $(this).addClass('active');
				$page.removeClass('wd_menu_container');
            });
        },
        //For Clock Counting
        ClockCounting: function() {
            var clock1;
            var futureDate = new Date("Dec 31, 2024 05:02 PM EST");
            var currentDate = new Date();

            // Calculate the difference in seconds between the future and current date
            var diff = futureDate.getTime() / 1000 - currentDate.getTime() / 1000;

            // Calculate day difference and apply class to .clock for extra digit styling.
            function dayDiff(first, second) {
                return (second - first) / (1000 * 60 * 60 * 24);
            }

            if (dayDiff(currentDate, futureDate) < 100) {
                $('.clock1').addClass('twoDayDigits');
            } else {
                $('.clock1').addClass('threeDayDigits');
            }

            if (diff < 0) {
                diff = 0;
            }

            // Instantiate a coutdown FlipClock
            clock1 = $('.clock1').FlipClock(diff, {
                clockFace: 'DailyCounter',
                countdown: true
            });
        },
        // Stellar
        // Stellar: function() {
        //     $.stellar({
        //         horizontalScrolling: false,
        //         responsive: true
        //     });

        // },

    };
    wedding.init();
    // Load Event
    $(window).on('load', function() {
        //Preloader
        $("#preloader").delay(4000).fadeOut("slow");
    });
})(jQuery);
