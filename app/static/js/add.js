/**
 * Created by sanxing on 2014/12/26.
 */
(function(){
    var eventType;
    var teacher_info={};
    teacher_info.school= "华中科技大学";
    teacher_info.major="";
    teacher_info.school = document.getElementById("school-name").innerHTML;


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

    /**************微信分享****************/
    function preload(){
        var shareData = {
            "appId": "", // 服务号可以填写appId
            "imgUrl": "http://nini.hustonline.net/static/images/share.jpg",
            "link": "http://nini.hustonline.net/",
            "desc": '匿名评师！快来添加你认识的老师吧！',
            "title": '匿名评师！快来添加你认识的老师吧！'
        };
        WeixinApi.ready(function(api) {
            api.hideToolbar();
            api.shareToTimeline(shareData, {});
        });
    }
    preload();
    /**************************************/

    /***去除字符串首尾的空格**/
    function trim(str){
        return str.replace(/^\s+|\s+$/g,"");
    }

    if(checkBroswer()){
        eventType = "tap";
    }else {
        eventType = "click";
    }
    $("#teacher-name").on("focus",function(){
        $(this).val("");
    });

    $("#list-item").on(eventType,"li",function(e){
        e.stopPropagation();
        if(!$(this).hasClass("active")){
            $("#list-item li").removeClass("active")
            $(this).addClass("active");
        }
        var major = $(this).attr("dept-id");
        teacher_info.major=major;
        $("#mask").fadeOut();
        $("#major").text($(this).text());
    });

    $("#major").on(eventType,function(){
        $("#mask").fadeIn(200);
    });

    $("#mask").on(eventType,function(){
        $(this).fadeOut();
    });

    $("#major-window").on(eventType,function(e){
        e.stopPropagation();
    });

    $("#add-submit").on(eventType,function(){
        teacher_info.name=$("#teacher-name").val();
        if(trim(teacher_info.name)==""||trim(teacher_info.major)==""){
            $("#tip").find("header").text("忘记什么了吧？");
            $("#tip").fadeIn(100);
        }else if(trim(teacher_info.name).length>4){
            $("#tip").find("header").text("名字太长了吧？");
            $("#tip").fadeIn(100);
        }
        else{
            $.post("/teacher/add",{name:teacher_info.name,school:teacher_info.school,dept_name:teacher_info.major},function(result){
                if(result == "teacher exists"){
                    $("#tip").find("header").text("教师已存在");
                    $("#tip").fadeIn(100);
                }else{
                    window.location.href="/teacher/"+result;
                }
            });
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