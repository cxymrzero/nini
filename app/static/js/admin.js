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

    /*********点击提交按钮*********/
    $("#submit-teacher").on(eventType, function(e) {
        var teacher_url = $("#teacher-url").val();
        $.post("/admin/dt", {teacher_url: teacher_url}, function(data) {
            alert(data);
            location.reload();
//            $('#teacher-error').html(data);
        });

    });

    $("#submit-comment").on(eventType, function(e) {
        var comment_url = $('#comment-url').val();
        $.post('/admin/dc', {comment_url: comment_url}, function(data) {
            alert(data);
            location.reload();
//            $('#comment-error').html(data);
        });
    });
})();