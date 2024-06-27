function show_overlay(){
    $('#overlay').fadeIn();
    document.getElementsByTagName("body")[0].style = "overflow: hidden;"
}

function hide_overlay(){
    $('#overlay').fadeOut();
    document.getElementsByTagName("body")[0].style = ""
}