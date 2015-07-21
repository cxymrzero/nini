(function(){
    var eventType;
    /************check the broswer*****************/
    function checkBroswer(){
        var sUserAgent = navigator.userAgent.toLowerCase();
        var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
        var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
        var bIsMidp = sUserAgent.match(/midp/i) == "midp";
        var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
        var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
        var bIsAndroid = sUserAgent.match(/android/i) == "android";
        var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";
        var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
        if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) {
            return true;
        } else {
            return false;
        }
    }

    if(checkBroswer()){
        eventType = "tap";
    }else {
        eventType = "click";
    }

    /**************微信分享****************/
    function preload(){
        var shareData = {
            "appId": "", // 服务号可以填写appId
            "imgUrl": "http://nini.hustonline.net/static/images/share.jpg",
            "link": "http://nini.hustonline.net/",
            "desc": '匿名评师！说出你的心里话！',
            "title": '匿名评师！说出你的心里话！'
        };
        WeixinApi.ready(function(api) {
            api.hideToolbar();
            api.shareToTimeline(shareData, {});
        });
    }
    preload();
    /**************************************/
    $("#search").on(eventType,function(e){
        e.preventDefault();
        var text = $("#search-content").val();
        if(text==""){
            $("#tip").find("header").text("老师姓名呢？");
            $("#tip").fadeIn(100);
            return false;
        }else if(text.length>10){
            $("#tip").find("header").text("名字太长了吧！");
            $("#tip").fadeIn(100);
            return false;
        }else{
            $("#search-form").submit();
        }
    });

    /*****提示框的显隐*****/
    $("#tip footer").on(eventType,function(e){
        e.stopPropagation();
        $("#tip").fadeOut(200);
    });

    $("#tip section").on(eventType,function(e){
        e.stopPropagation();
    });
})();