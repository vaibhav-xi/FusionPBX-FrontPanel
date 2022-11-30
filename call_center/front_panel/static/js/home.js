$(document).ready(function() {
    // $(".draggable_number").draggable({
    //     snap: "dropable-roomm"
    // });

    // $(".dropable-roomm").on({
    //     drop: function(e) {
    //         console.log("basket drop");
    //     }
    // });

    $(".draggable_number").draggable({
        revert: "invalid",
        helper: "clone",
        snap: "dropable-room",
        zIndex: 5
    });

    $(".dropable-room").droppable({
        activeClass: "ui-state-highlight_drop",
        drop: function(event, ui) {
            var div = document.createElement('div');
            // div.className = 'room-banner';

            div.classList.add('room-banner', 'noselect', 'draggable_banner');

            var draggable = ui.draggable;
            var id = draggable.attr("id");

            div.setAttribute('id', `${id}`);

            var dn = document.getElementById(id).innerHTML;

            console.log("NAME:", dn);

            console.log("TARGET:", event.target.classList[4])

            var room = event.target.classList[4];

            send_c([room, id])

            // d = document.createTextNode(`${id}`);

            d = document.createTextNode(`${dn}`);

            div.appendChild(d);

            child = document.getElementById(id);

            console.log(child);
            console.log(this.contains(child));

            if (this.contains(child)) {
                console.log('YAS')
            } else {
                console.log('NOI')
                this.appendChild(div);
            }

            if ($(this).children(id).length > 0){ 
                console.log("HOIII");
              }


            div.addEventListener("dblclick", function() {
                console.log('Hoii')
            });
        }
    });
});

var un = "";
var n = "";

function edit_modal(elem_id){
    var name = document.getElementById(elem_id);
    un = elem_id;
    n = name;
    $('#details').modal('show');
    $('#user_name').val(name.innerHTML);
    $('#user_phone').val(elem_id);
}

$("#save_details").on("click", function() {
    cun = $('#user_name').val();
    cn = $('#user_phone').val();
    var name = document.getElementById(un);
    name.innerHTML = cun;
    $(n).attr("id",cn)
    $('#details').modal('hide');
});