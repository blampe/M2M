// Setup for the pages

$(function(){
    // set min-height of container
    $('#container').css('min-height',$(window).height()-25);
    $(window).resize(function(){
        $('#container').css('min-height',$(window).height()-25)
    });
    // move params around
    $('#searchParams').css('left',function(index,value){
                $(this).width(function(){
                    return 15 + Math.max.apply(Math, $('#searchParams select').map(function(){ return $(this).width(); }).get());
                });
                // gets rid of ugly whitespace below the options bar
                $(this).css('marginBottom',function(){
                    return 0 - $(this).height();
                });
                return -31 - parseInt($(this).width());
            }).css('visibility','visible');
            
    // move, replace searchbar stuff with images
    $('#searchbarActual').prepend($('ul#modifiers'));
    $('ul#modifiers li a').html(function(){
        return "<img src='/media/images/"+$(this).attr('id')+".png'/>"
    });
    
    // move subset lists out of navbar
    $('#subsetHold').prepend($('ul#subset'));
    
    // make navbar opaque, prettily
    $(window).scroll(function(){
        if($(window).scrollTop() > 350){
            $('#sitewide').css('backgroundColor','rgba(70, 130, 180,1)');
        } else if ($(window).scrollTop() == 0){
            $('#sitewide').css('backgroundColor','rgba(70, 130, 180,0.5)'); 
        } else {
            $('#sitewide').css('backgroundColor','rgba(70, 130, 180,'+(0.5+$(window).scrollTop()/700)+')');
        }
    });
});