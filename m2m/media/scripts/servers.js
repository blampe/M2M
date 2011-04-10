function dispTogglejQ(id){
    id = "#"+id;
    var toggleID = "#"+id+"l";
    var sizeID = "#"+id+"s";
    
    var $toggler = $(toggleID);
    
    if($(id).css('display') == "none"){
        $(id).css('display',"inline");
        $(sizeID).css('display',"inline");
        $toggler.html("Less...");
    } else {
        $(id).css('display', "none");
        $(sizeID).css('display', "none");
        $toggler.html("More...");
    }
}

function dispToggle(id){
    var toggleID = id + "l";
    var sizeID = id+"s";
    
    var seeMe = document.getElementById(id).style.display;
    var toggler = document.getElementById(toggleID);
    
    if(seeMe == "none"){
        document.getElementById(id).style.display = "inline";
        document.getElementById(sizeID).style.display = "inline";
        toggler.innerHTML = "Less...";
    } else {
        document.getElementById(id).style.display = "none";
        document.getElementById(sizeID).style.display = "none";
        toggler.innerHTML = "More...";
    }
}