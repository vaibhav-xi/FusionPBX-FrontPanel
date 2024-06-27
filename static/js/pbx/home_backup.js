$(document).ready(function() {
    // $(".draggable_number").draggable({
    //     snap: "dropable-roomm"
    // });

    // $(".dropable-roomm").on({
    //     drop: function(e) {
    //         console.log("basket drop");
    //     }
    // });

    function make_draggable() {
        $(".draggable_banner").draggable({
            snap: "dropable-room",
            zIndex: 5
        });
    }

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

            d = document.createTextNode(`${id}`);

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

            if ($(this).children(id).length > 0) {
                console.log("HOIII");
            }


            div.addEventListener("dblclick", function() {
                console.log('Hoii')
            });

            make_draggable();
        }
    });
});