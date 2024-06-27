const socket = new WebSocket('ws://' + '138.201.188.127' + ':8001/ws/myconsumer/');

show_overlay();
$('#spinner_text').html('Connecting to server');

socket.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log(data);
  console.log(typeof data);
  if (data.type === 'update') {
    // handle the incoming update
  }
};

socket.onclose = function(event) {
  console.log('WebSocket connection closed.');
};

var csrftoken = getCookie('csrftoken');
var total_container = [];
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// fetch('/get_data/', {
//     method: 'POST',
//     headers: {
//         'Content-type': 'application/json',
//         'X-CSRFToken': csrftoken,
//     },
//     body: JSON.stringify({ 'details': 'conferences' })
// })
// .then((resp) => resp.json())
// .then(response => {

    
//     show_overlay();
//     $('#spinner_text').html('Fetching Users');

//     values = JSON.parse(response)

//     console.log(response.values);
//     console.log(response);
//     console.log(typeof response);

//     // console.log(response)

//     // for (let i = 0; i < response.length; i++) {
//     //     user_data = response[i]
    
//     //     for (let j = 0; j < user_data.length; j++) {
//     //         // user_data[j]
//     //         $('#data_table').find('tbody').append(`<tr><td id="${user_data[3]}" ondblclick="edit_modal(this.id)">${user_data[1]}</td></tr>`);
//     //     }
//     // }

//     hide_overlay();
// });

var banner_clicked = '';
var double_clicked = '';
var current_drag = '';
var notes = {}

var mydict = {}

function set_value(banner_id) {
    banner_clicked = banner_id.replace('note', 'element');
    $('#colorModal').modal('show')
}

function set_note(bannerid) {
    double_clicked = bannerid.replace('note', 'element');

    if (double_clicked in notes){
        $("#mynote").val(notes[double_clicked]);
    } else {
        $("#mynote").val('');
    }

    $('#noteModal').modal('show')
}

function es(){
    // Add Search to table 

    var $rows = $('#data_table tr');
    $('#search_input').keyup(function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        
        $rows.show().filter(function() {
            var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
            return !~text.indexOf(val);
        }).hide();
    });
}

function md(){
    // console.log('ENABLING DRAG');

    $(".room-banner").draggable({
        revert: "invalid",
        helper: "clone",
        snap: "dropable-room",
        start: function(event, ui){
            var roomId = $(this).closest('.dropable-room').attr('id');
            $(ui.helper).data('room-id', roomId);

            console.log("ROOM ID:", roomId);

            $('.dropable-room').css("overflow-y", "hidden");
        },
        stop: function(){
            $('.dropable-room').css("overflow-y", "auto");
        },
        helper: function() {
            return $(this).clone().css({
                'width': '250px'
            });
        }
    });
    
    $(".dropable-room").droppable({
        activeClass: "ui-state-highlight_drop",
        drop: function(event, ui) {
    
            var to_room = event.target.id;

            var caller_id = ui.draggable.attr('id');
            var caller_name_id = ui.draggable.find('.text').attr('id');
            var caller_url_id = ui.draggable.find('.link').attr('id');

            var from_room = ui.helper.data('room-id');

            console.log(caller_id);
            console.log(caller_name_id);
            console.log(caller_url_id);
    
            // send_c([id, room])
    
            console.log([caller_name_id, from_room, to_room]);

            // APPEND BANNER TO ROOM
    
            // caller_name = document.getElementById(caller_name_id).innerHTML;

            // raw_html = `
            //         <div class="container draggable_banner noselect room-banner" id="${caller_id}">
            //             <div class="text" id="${caller_name_id}">${caller_name}</div>
            //             <div class="menu-wrap">
            //                 <input type="checkbox" class="toggler">
            //                 <div class="dots">
            //                     <div></div>
            //                 </div>
            //                 <div class="menu">
            //                     <div>
            //                         <ul>
            //                             <li><a class="link myurl" id="${caller_url_id}" href="">Url</a></li>
            //                             <li><a class="link" onclick = "$('#colorModal').modal('show')" >Colour</a></li>
            //                         </ul>
            //                     </div>
            //                 </div>
            //             </div>
            //         </div>`

            // if ($(`#${room}`).find(`#${caller_id}`).length) {
            //     // console.log('IT CONTAINS DIV');
            // } else {
            //     $('#' + room).append(raw_html);

            //     $('.toggler').click(function(){
            //         $('.toggler').not(this).prop('checked',false);
            //     });
            // }

            // $('#' + room).append(raw_html);

            // $('.toggler').click(function(){
            //     $('.toggler').not(this).prop('checked',false);
            // });

            // md();
        }
    });
}

show_overlay();
$('#spinner_text').html('Fetching Users');

fetch('/get_data/', {
    method: 'POST',
    headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'details': 'extensions' })
})
.then((resp) => resp.json())
.then(function(Responsedata) {

    // show_overlay();
    // $('#spinner_text').html('Fetching Users');

    // console.log(Responsedata)

    values = JSON.parse(Responsedata)
    // console.log('Values:', values)
    // console.log(typeof values)

    for (let i = 0; i < values.length; i++) {
        user_data = values[i]
    
        $('#data_table').find('tbody').append(`<tr><td class="draggable_number" id="${user_data[3]}" ondblclick="edit_modal(this.id)">${user_data[1]}</td></tr>`);
        
    }

    md();
    es();

    // hide_overlay();
});

fetch('/get_data/', {
    method: 'POST',
    headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'details': 'conferences' })
})
.then((resp) => resp.json())
.then(function(Responsedata) {

    $('#spinner_text').html('Fetching Conference Rooms..');
    
    show_overlay();

    crs = JSON.parse(Responsedata);

    // console.log('CONFERENCES:', crs);

    for (let i = 0; i < crs.length; i++) {
        user_data = crs[i]
    
        var div = document.createElement('div');

        var hr = document.createElement('hr');

        div.classList.add('scrollbar', 'dropable-room', 'col-first', 'col', 'style-3');

        div.setAttribute('id', `${user_data[1]}`);

        var ind = document.createElement('div');

        ind.classList.add('room-heading', 'ho');

        ind.setAttribute('id', `${user_data[0]}`);

        total_container.push(user_data[1]);

        d = document.createTextNode(`${user_data[0].toUpperCase()}`);

        ind.appendChild(d);

        div.appendChild(ind);

        div.appendChild(hr);

        document.getElementById('bg_container').appendChild(div);
        
    }

    md();
    es();
    hide_overlay();
});


function active_calls(){
    fetch('/activecalls/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify('Hoi')
    })
    .then((resp) => resp.json())
    .then(response => {

        console.log(response);
        
        total_active_calls = JSON.parse(response)
        // console.log(total_active_calls);

        if (total_active_calls != "No Queues") {
            const keys = Object.keys(total_active_calls);

            for (const dict_key in total_active_calls) {
                // console.log(dict_key);
                var room = dict_key;
                // callers = total_active_calls[dict_key]['users'];
                callers = values(d[dict_key]['users']);
                callers.forEach(element => {
                    // console.log(element);
                    const container = document.getElementById(room);
                    const myDiv = container.querySelector(`#element-${element[0]}`);
    
                    if (myDiv) {
                        // pass
                    }
                    else {

                        raw_html = `
                            <div ondblclick = 'set_note(this.id)' style = "background-color:${total_active_calls[dict_key]['background']}; color:${total_active_calls[dict_key]['font']};" class="container draggable_banner noselect room-banner" id="element-${element[1]}">
                                <div class="text" id="${element[1]}">${element[0]}</div>
                                <div class="menu-wrap">
                                    <input type="checkbox" class="toggler">
                                    <div class="dots">
                                        <div></div>
                                    </div>
                                    <div class="menu">
                                        <div>
                                            <ul>
                                                <li><a class="link myurl" id="${element[0]}-url" href="${total_active_calls[dict_key]['url']}" target="_blank">Url</a></li>
                                                <li><a class="link" id = '${element[0]}-click' onclick = "set_value(this.id)" >Colour</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>`

                        $('#' + room).append(raw_html);

                        $('.toggler').click(function(){
                            $('.toggler').not(this).prop('checked',false);
                        });

                        md();
                    }

                    const divs = container.querySelectorAll("div");
                    for (let i = 0; i < divs.length; i++) {
                        var id = divs[i].id.replace('element-', "");
                        var div_class = divs[i].classList.contains("room-banner")
                        if (!callers.includes(id)) {
                            if (div_class) {
                                divs[i].remove();
                            }
                        }
                    }
                });
            }

        } 
    });
}

$("#saveColor").click(function(){
    var font_color = $("#fontColorPicker").val();
    var background_color = $("#backgroundColorPicker").val();

    $(`#element-${banner_clicked}`).css("background-color", background_color);
    $(`#${banner_clicked}`).css("color", font_color);

    $('#colorModal').modal('hide')
});

$("#savenote").click(function(){
    var my_note = $("#mynote").val();

    notes[`${double_clicked}`] = my_note;

    $('#noteModal').modal('hide')
});

$("#modal-close").click(function(){

    $('#colorModal').modal('hide')
});

$("#note-close").click(function(){

    $('#noteModal').modal('hide')
});

function expand_room(name) {
    var childDiv = document.getElementById(name);
    var parent = document.getElementById(childDiv.parentNode.id);

    if (parent.offsetWidth < 400) {
        parent.style.width = "900px";
    } else {
        parent.style.width = "300px";
    }

}

socket.onopen = function() {
    console.log('WebSocket connection established.');
  
    $('#spinner_text').html('connection established');
  
    // hide_overlay();
  };
  
  socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    // console.log(data);
    
    total_container.forEach(my_id => {
        // console.log(my_id);
        var my_container = document.getElementById(my_id);
        const childNodes = my_container.childNodes;
        childNodes.forEach(node => {
            if(node.tagName === 'DIV' && node.classList.contains("room-banner")){
                my_container.removeChild(node);
            }
        });
    });

    // console.log(data);
  
    if (data != "No Queues") {

        console.log("DATA: ", data);

        if ('DP' in data) {

            console.log(data);

        } else {

            for (const dict_key in data) {
                // console.log("DICT KEY:", dict_key);
                var room = dict_key;
                // callers = data[dict_key]['users'];
    
                // console.log('VALUES: ', Object.values(data[dict_key]));
    
                callers = Object.values(data[dict_key]['users']);
                callers.forEach(element => {
                    // console.log("ELEMENT: ", element);
                    // console.log("ROOM: ", room);
                    // console.log("ELEMENT 0: ", element[0]);
                    const container = document.getElementById(room);
                    const myDiv = container.querySelector(`#element-${element[0]}`);
      
                    if (myDiv) {
                        // pass
                        // console.log('WRONG AREA')
                    }
                    else {
      
                        // console.log('CORRECT AREA')
    
                        raw_html = `
                            <div ondblclick = 'expand_room(this.id)' style = "background-color:${data[dict_key]['background']}; color:${data[dict_key]['font']};" class="container draggable_banner noselect room-banner" id="element-${element[1]}">
                                <div class="text" id="${element[1]}">${element[0]}</div>
                                <div class="menu-wrap">
                                    <input type="checkbox" class="toggler">
                                    <div class="dots">
                                        <div></div>
                                    </div>
                                    <div class="menu">
                                        <div>
                                            <ul>
                                                <li><a class="link myurl" id="${element[0]}-url" href="${data[dict_key]['url']}" target="_blank">Url</a></li>
                                                <li><a class="link" id = '${element[0]}-click' onclick = "set_value(this.id)" >Colour</a></li>
                                                <li><a class="link" id = 'note-${element[1]}' onclick = "set_note(this.id)" > Note </a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>`
    
                        // console.log("RAW HTML: ", raw_html);
      
                        $(`#${room}`).append(raw_html);
      
                        $('.toggler').click(function(){
                            $('.toggler').not(this).prop('checked',false);
                        });
      
                        md();
                    }
                });
            }
        }
  
    } 
    
  };