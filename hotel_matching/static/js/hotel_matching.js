$(document).ready(function(){
    $("div#namepopup").hide();

    $(".hotel_name").mouseover(function(){
        $("#namepopup",this).show();
    }).mouseout(function(){
            $("#namepopup",this).hide();
        });
    $("div#addpopup").hide();

    $(".hotel_add").mouseover(function(){
        $("#addpopup",this).show();
    }).mouseout(function(){
            $("#addpopup",this).hide();
        });

//    Irrelevant Request
    $(".cross").live("click", function(){
        var csrf = $("#csrf-token").attr('value');
        var hid = this.id;
        var attr = this;
        $.ajax({
            type: "POST",
            url: '/irrelevant/',
            data: {csrfmiddlewaretoken:csrf, 'irr_id': hid},
            success: function(html){
                var li = $("#"+hid).parent('li').html();
                $("#"+hid).parent('li').remove();
                var irr_num = parseInt($("#irrelevant").text().split("(")[1].split(")")[0])+1;
                var sug_num = parseInt($("#suggestions").text().split("(")[1].split(")")[0])-1;
                $("#irrelevant").text("irrelevant("+irr_num+")");
                if($(attr).parent("li").hasClass("left")){
                    $("#suggestions").text("suggestions("+sug_num+")");
                }
                if($("#irrelevant").css("color") == "rgb(0, 0, 0)"){
			$("#hotel_details").children("ul").append('<li>'+li+'</li>');
	                $("#map"+hid).html('<span></span>');
        	        var cords = $(attr).parent("li").children("div").children("div").children(".match_btn").attr("name");
                	initialize2(cords, hid);
			$("#"+hid).css({display: "none"});
                }
            }
        });
    });


//    Match Request
    $(".match_btn").live("click", function(){
        var csrf = $("#csrf-token").attr('value');
        var hid = this.id;
        var this2 = this;
        $.ajax({
            type: "POST",
            url: "/match/",
            data: {csrfmiddlewaretoken: csrf, 'match_id': hid},
            success: function(html){
                var li = $("#"+hid).parent('li').html();
                $("#"+hid).parent('li').remove();
                $("#hotel_details_right").children("ul").append('<li>'+li+'</li>');
                $("#map"+hid).html('<span></span>');
                var cords = $(this2).attr("name");
                initialize2(cords, hid);
                $("#"+hid).css({display: "block"});
                if($("#irrelevant").css("color") == "rgb(0, 0, 0)"){
                    var irr_num = parseInt($("#irrelevant").text().split("(")[1].split(")")[0])-1;
                    $("#irrelevant").text("irrelevant("+irr_num+")");
                }else{
                    var sug_num = parseInt($("#suggestions").text().split("(")[1].split(")")[0])-1;
                    $("#suggestions").text("suggestions("+sug_num+")");
                }
            }
        });
    });

    function initialize2(cords2, hid) {
        var cords = cords2.split(',');
        var myLatlng = new google.maps.LatLng(cords[0], cords[1]);
        var mapOptions = {
            zoom: 18,
            center: myLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map"+hid), mapOptions);
    }

    //    Save Request
    $(".save_btn").live("click", function(){
        var csrf = $("#csrf-token").attr('value');
        var mid = this.id;
        var hids = [];
        $("#hotel_details_right").children("ul").children("li").children(".cross").each(function(){
            hids.push(this.id);
        });
        $.ajax({
            type: "POST",
            url: "/save/",
            data: {csrfmiddlewaretoken: csrf, 'mid': mid, 'hids': hids},
            success: function(html){
                window.location = $('#skip').attr('href');
            }
        });
    });


    $("a#inline").fancybox({
        'hideOnContentClick': false, // so you can handle the map
        'overlayColor'      : '#ccffee',
        'overlayOpacity'    : 0.8,
        'autoDimensions': true
    });
    $("a#inline").live("click", function(){
        initialize();
    });

    var bounds = null;
    function initialize() {
        var cords = $(".save_btn").attr("name").split(',');
        var myLatlng = new google.maps.LatLng(cords[0], cords[1]);
        var mapOptions = {
            zoom: 8,
            center: myLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("data"), mapOptions);
        bounds = new google.maps.LatLngBounds();
        TestMarker();
        map.fitBounds(bounds);
        map.panToBounds(bounds);
        }
    function addMarker(location, title, num, color) {
        marker = new google.maps.Marker({
            position: location,
            map: map,
            icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld="+num+"|"+color+"|000000",
            title: title
        });
    }

    // Testing the addMarker function
    function TestMarker() {
        $(".match_btn").each(function(){
            var hcords = $(this).attr("name").split(',');
            var htitle = $(this).parent("div").parent("div").children("div").children("h4").text();
            Hinfo = new google.maps.LatLng(hcords[0], hcords[1]);
            bounds.extend(Hinfo);
            var num = htitle.split(".")[0];
            var color = $(this).parent("div").parent("div").parent("li").attr("name");
            if($(this).parent("div").parent("div").parent("li").parent("ul").hasClass("right-matches")){
                color = "#0000FF"
            }
            addMarker(Hinfo, htitle, num, color.split("#")[1]);
        });
        var mcords = $(".save_btn").attr("name").split(',');
        var mtitle = $(".save_btn").parent("div").parent("div").children("div").children("h4").text();
        Minfo = new google.maps.LatLng(mcords[0], mcords[1]);
        bounds.extend(Minfo);
        addMarker(Minfo, mtitle, "R", "0000FF");
    }


//    Mouse wheel function
    /** This is high-level function.
     * It must react to delta being more/less than zero.
     */
    function handle(delta) {
        var y = $("#hotel_details").scrollTop();  //your current y position on the page
        if (delta < 0){
            $("#hotel_details").scrollTop(y+150);
        }else{
            $("#hotel_details").scrollTop(y-150);
        }
    }

    /** Event handler for mouse wheel event.
     */
    function wheel(event){
        var delta = 0;
        if (!event) /* For IE. */
            event = window.event;
        if (event.wheelDelta) { /* IE/Opera. */
            delta = event.wheelDelta/120;
        } else if (event.detail) { /** Mozilla case. */
            /** In Mozilla, sign of delta is different than in IE.
             * Also, delta is multiple of 3.
             */
            delta = -event.detail/3;
        }
        /** If delta is nonzero, handle it.
         * Basically, delta is now positive if wheel was scrolled up,
         * and negative, if wheel was scrolled down.
         */
        if (delta)
            handle(delta);
        /** Prevent default actions caused by mouse wheel.
         * That might be ugly, but we handle scrolls somehow
         * anyway, so don't bother here..
         */
        if (event.preventDefault)
            event.preventDefault();
        event.returnValue = false;
    }

    /** Initialization code.
     * If you use your own event management code, change it as required.
     */
    if (window.addEventListener)
        /** DOMMouseScroll is for mozilla. */
        window.addEventListener('DOMMouseScroll', wheel, false);
    /** IE/Opera. */
    window.onmousewheel = document.onmousewheel = wheel;
});
