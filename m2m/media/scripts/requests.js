function likeHandler(){
    $('.likeform').submit(function(){
        cid = $(this).attr('id');
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/requests/like/"+cid+"/{{page}}",
            cache: false,
            dataType:'html',
            success: function(html,textStatus){
                $('#'+cid+" em").load('{% url requests.views.open page%} #'+cid+' em');
                $('#'+cid+" button").replaceWith("Thanks!");
            },
            error: function( XMLHttpRequest, textStatus, errorThrown){
                $('#'+cid+" button").replaceWith("Sorry, no");
            }
        
        });
        return false;
    });
}

function extraRequestHandler(){
    $('#miniRequester').click(function(){
        $('#extraForm').slideToggle("slow");
        $('#requestForm').slideToggle("slow");
    });

    // if they click out, get rid of it:
    $('#container').click(function(){
        $('#extraForm').slideUp("slow");
        $('#requestForm').slideDown("slow");
        });
}

$(document).ready(function(){ 
    likeHandler();
    
    // make sure the request form is positioned properly
    $("#requestForm").width(function(){
        return $("#requestComment").width() + $("#noncommentrequest").width()+10;
    });
    $("#submitrequest").click(function(){
        $('#requester').submit();
    });
    
    // setup followtab
    $("#followTab").css('left',function(){
            return $(window).width() - 3*$(this).height();
        });
    $("#followTab").css('top',function(){
        return $(window).height()/2;
    });
    $(window).resize(function(){
        $("#followTab").css('left',function(){
            return $(window).width() - 3*$(this).height();
        });
        $("#followTab").css('top',function(){
            return $(window).height()/2;
        });
    });
    $("#tabform").click(function(){
        target = $("div#simpleModal");
        target.prepend($("form#requester"));
        target.addClass("show");
        target.css('width',function(){
            return $("div#requestForm").width();
        });
        $(this).hide();
        return false;
    });
    $("#closeSimple").click(function() {
        $("div#requestForm").prepend($("form#requester"));
        $("div#simpleModal").removeClass("show");
        $("#tabform").show();
        return false;
    });
   
});