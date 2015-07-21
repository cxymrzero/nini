(function(){
    var eventType;
    var comment={};
    comment.score= -1;
    comment.id = $("#teacher").attr("teacher-id");
    comment.name=$("#teacher").find(".name").text();

    $(function() {
        FastClick.attach(document.body);
    });

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

    /***去除字符串首尾的空格**/
    function trim(str){
        return str.replace(/^\s+|\s+$/g,"");
    }
    /**************微信分享****************/
    function preload(){
        var shareData = {
            "appId": "", // 服务号可以填写appId
            "imgUrl": "http://nini.hustonline.net/static/images/share.jpg",
            "link": "http://nini.hustonline.net/teacher/"+comment.id,
            "desc": '匿名评师！来看看大家对“'+comment.name+'“老师的看法吧！',
            "title": '匿名评师！来看看大家对“'+comment.name+'“老师的看法吧！'
        };
        WeixinApi.ready(function(api) {
            api.hideToolbar();
        });
        WeixinApi.ready(function(api) {
            api.shareToTimeline(shareData, shareData);
        });
    }
    preload();
    /**************************************/
    function checkWordNum(obj){
        var num = obj.length;
        for(var i=0;i<num;i++){
            var temp = $(obj[i]).find("p");
            var text=temp.text();
            if(text.length>=50){
                text=text.substr(0,50)+"......";
            }
            temp.text(text);
            //console.log(text);
        }
    }

    checkWordNum($(".comment-item"));

    /********最新评论和最热评论之间的切换****************/
    $("#hottest").on(eventType, function () {
        if($(this).hasClass("active")){
            return ;
        }
        $("#comment-label").find("span").removeClass("active");
        $(this).addClass("active");
        $("#comment-new-wrap").fadeOut(0,function(){
            $("#comment-hot-wrap").fadeIn(0);
        })
    });

    $("#newest").on(eventType, function () {
        if($(this).hasClass("active")){
            return ;
        }
        $("#comment-label").find("span").removeClass("active");
        $(this).addClass("active");
        $("#comment-hot-wrap").fadeOut(0,function(){
            $("#comment-new-wrap").fadeIn(0);
        })
    });

    /************不同窗口之间的切换**************/
    $("#comment-make").on(eventType,function(){
        $("#comment-mask").fadeIn(200,function(){
            $("#comment-content").focus();
        });
        $("#teacher-wrap").fadeOut(0);
    });

    var once = {};
    once.comment=1;
    $("#comment-submit").on(eventType,function(){
        if(once.comment==1){
            var text = trim($("#comment-content").val());
            if(text==""){
                alert("好像还没评论呢");
            }else{
                comment.content = text;
                $("#comment-window").fadeOut(0,function(){
                    $("#score-window").fadeIn(0);
                    once.comment++;
                });
            }
        }else{
            return ;
        }

    });

    $("#score-window").on(eventType,function(e){
        e.stopPropagation();
    });
    $("#comment-window").on(eventType,function(e){
        e.stopPropagation();
    });

    /***** 评论中顶和踩的点击****/
    $("#comment-hot-wrap").on(eventType,".ding",function(){
        var cmt_id = $(this).attr("cmt-id");
        var $this = $(this);
        $.get("/comment/vote",{cmt_id:cmt_id,method:"up"},function(result){
            if(result == "already voted"){
                $("#tip").find("header").text("投过票了");
                $("#tip").fadeIn(100);
            }else if(result == "ok"){
                if($this.hasClass("active")||$(this).next().next().hasClass("active")){
                    return ;
                }
                var num=parseInt($this.next().text())+1;
                $this.next().text(num);
                $this.addClass("active");
            }
        });
    });
    $("#comment-hot-wrap").on(eventType,".cai",function(){
        var cmt_id = $(this).attr("cmt-id");
        var $this = $(this);
        $.get("/comment/vote",{cmt_id:cmt_id,method:"down"},function(result) {
            if (result == "already voted") {
                $("#tip").find("header").text("投过票了");
                $("#tip").fadeIn(100);
            } else {
                if ($this.hasClass("active") || $this.prev().prev().hasClass("active")) {
                    return;
                }
                var num = parseInt($this.prev().text()) - 1;
                $this.prev().text(num);
                $this.addClass("active");
            }
        });
    });
    $("#comment-new-wrap").on(eventType,".ding",function(){
        var cmt_id = $(this).attr("cmt-id");
        var $this = $(this);
        $.get("/comment/vote",{cmt_id:cmt_id,method:"up"},function(result){
            if(result =="already voted"){
                $("#tip").find("header").text("投过票了");
                $("#tip").fadeIn(100);
            }else{
                if($this.hasClass("active")||$this.next().next().hasClass("active")){
                    return ;
                }
                var num=parseInt($this.next().text())+1;
                $this.next().text(num);
                $this.addClass("active");
            }
        });
    });
    $("#comment-new-wrap").on(eventType,".cai",function(){
        var cmt_id = $(this).attr("cmt-id");
         var $this = $(this);
        $.get("/comment/vote",{cmt_id:cmt_id,method:"down"},function(result) {
            if (result == "already voted") {
                $("#tip").find("header").text("投过票了");
                $("#tip").fadeIn(100);
            } else {
                if ($this.hasClass("active") || $this.prev().prev().hasClass("active")) {
                    return;
                }
                var num = parseInt($this.prev().text()) - 1;
                $this.prev().text(num);
                $this.addClass("active");
            }
        });
    });

    /************score-submit and no-score-submit*****************/
    once.score = 1;
    $("#list-item").on(eventType,".score",function(e){
        e.stopPropagation();
        e.preventDefault();
        if(once.score==1&&(!$("#list-item li").hasClass("active"))){
            $(this).addClass("active");
            var score = parseInt($(this).text());
            comment.score = score;
            $.post("/teacher/"+comment.id,{point:comment.score,content:comment.content},function(result){
                if(result == "ok"){
                    once.score++;
                    $("#teacher-wrap").fadeIn(0);
                    $("#comment-mask").fadeOut(200);
                    window.location.href="/teacher/"+comment.id;
                }else{
                    $("#tip").fadeIn(100);
                }
            });
        }else{
            return ;
        }
    });

    $("#no-score-submit").on(eventType,function(e){
        e.stopPropagation();
        e.preventDefault();
        if(once.score == 1&&(!$("#list-item li").hasClass("active"))){
            $(this).addClass("active");
            $.post("/teacher/"+comment.id,{point:-1,content:comment.content},function(result){
                if(result == "ok"){
                    once.score++;
                    $("#teacher-wrap").fadeIn(0);
                    $("#comment-mask").fadeOut(200);
                    window.location.href="/teacher/"+comment.id;
                }else{
                    $("#tip").fadeIn(100);
                }
            });
        }else{
            return ;
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
