function dispToggle(id){
    teaser = document.getElementById(id+'t');
    body = document.getElementById(id);
    hider = document.getElementById(id+'h');
    
    if(body.style.display == "none"){
        teaser.style.display = 'none';
        body.style.display = 'block';
        hider.style.display = 'block';
    } else {
        body.style.display = 'none';
        hider.style.display = 'none';
        teaser.style.display = 'block';
    }
}
function bindPostCommentHandler(){
    $('#commentForm form').submit(function(){
       $.ajax({
            type: "POST",
            data: $('#commentForm form').serialize(),
            url: "{%comment_form_target%}",
            cache: false,
            dataType: "html",
            success: function(html, textStatus){
                $('#commentForm form').replaceWith("Thanks for your comment!");
                bindPostCommentHandler();
                $('#commentContainer').load('{{object.get_absolute_url}} #commentLister')
            },
            error: function( XMLHttpRequest,textStatus,errorThrown){
                if($('#commentForm form #id_comment').value == ''){
                    $('#commentForm form #id_comment').value = "Please write a comment!";
                }
            }
        });
       return false;
    });
}

var edited = false;
    function toggleText(id){
        if($(id)){
            var $target = $(id);
            if($target.attr('value') == "Anonymous" && edited == false){
                $target.attr('value', "");
            } else if(edited == false){
                $target.attr('value',"Anonymous");
            }
        }
    }

$(function(){
    // attach toggles to togglebots
    //$(".togglebot").click(dispToggle($(this).attr('id')));
    
    $("div.postmeta").css('left',function(){
        $(this).css('marginBottom',-$(this).height());
        return -$(this).width() - 10 - parseInt($(".postWrap,.detailwrap").css('padding-left'));
    });
    
    
    // news comment form
    $("#id_comment").width(function(){
        return $(this).parents("td:first").width()
    });
    
    $("#submitcomment").click(function(){
        $(this).parents("form:first").submit();
        return false;
    });
    
    bindPostCommentHandler();
});