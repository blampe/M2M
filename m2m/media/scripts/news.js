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

$(function(){
    // attach toggles to togglebots
    //$(".togglebot").click(dispToggle($(this).attr('id')));
    
    $("div.postmeta").css('left',function(){
        $(this).css('marginBottom',-$(this).height());
        return -$(this).width() - 10 - parseInt($(".postWrap,.detailwrap").css('padding-left'));
    });

});