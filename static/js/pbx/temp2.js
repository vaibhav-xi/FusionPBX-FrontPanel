const socket = new WebSocket('ws://' + '138.201.188.127' + ':8001/ws/myconsumer/');

show_overlay();
$('#spinner_text').html('Connecting to server');


socket.onclose = function(event) {
    console.log('WebSocket connection closed.');
    $('#spinner_text').html('Connecting to Server...');
    show_overlay();
};

var csrftoken = getCookie('csrftoken');

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

var banner_clicked = '';
var double_clicked = '';
var current_drag = '';

var notes = {}
var mydict = {}
var active_users = {}

var conferences = {}

var mark;

var global_var;

var total_container = [];

var my_rsa = "";

var new_session = true;

function set_value(banner_id) {
    banner_clicked = banner_id.replace('note', 'element');
    $('#colorModal').modal('show')
}

var store_response;

function m_room(my_room) {

    console.log("SENDING MUTE INFO: ", my_room);

    fetch('/algo_m/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': my_room })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            console.log("MUTE RESPONSE:", Responsedata);

        });
}

function send_cmd(cmd) {

    fetch('/cmd_transfer/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': cmd })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            console.log("RESPONSE:", Responsedata);

            prased = JSON.parse(Responsedata)

            if ("success" in prased) {

                // console.log("CHECK1: ", conferences[cmd[1]])
                // console.log("CHECK2: ", conferences[cmd[1]]['users'])
                // console.log("CHECK3: ", conferences[cmd[1]]['users'][cmd[4]])

                // delete conferences[cmd[1]]['users'][cmd[4]]

                // if (Object.keys(conferences[cmd[1]]['users']).length == 0) {
                //     delete conferences[cmd[1]]
                // }

                // console.log("MODIFIED CONFERENCES: ", conferences);

                m_room(prased["success"]);

            } else {
                console.log("failed");
            }
        });
}

function exin(cmd) {
    fetch('/exin_transfer/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': cmd })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            console.log("RESPONSE:", Responsedata);

            prased = JSON.parse(Responsedata)

            if ("success" in prased) {
                if (prased["success"] in active_users) {
                    console.log("PRESENT");
                    socket.send(`{"remove":"${active_users[prased["success"]]}"}`)
                }
            } else {
                console.log("failed");
            }
        });
}

function set_note(bannerid) {
    double_clicked = bannerid.replace('note', 'element');

    if (double_clicked in notes) {
        $("#mynote").val(notes[double_clicked]);
    } else {
        $("#mynote").val('');
    }

    $('#noteModal').modal('show')
}

function change_status(myid) {
    var circle = document.getElementById(myid);

    if (circle.style.color === "red") {
        circle.style.color = "green";
    } else {
        circle.style.color = "red";
    }
}

function es() {
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

function toggleVisibility(my_id, prio) {
    var el = document.getElementById(my_id);

    if (el.style.display === "none") {

        el.style.display = "block";

    } else {

        document.getElementById(my_id.split('-')[1]).style.backgroundImage = "";

        el.style.display = "none";

        if (prio) {

            my_rsa = Math.floor(Math.random() * 10000) + 1;

            socket.send(`{"change":"['${my_id}', '${my_rsa}']"}`)
        }
    }
}

function md() {

    $(".room-banner").draggable({
        revert: "invalid",
        helper: "clone",
        snap: "dropable-room",
        start: function(event, ui) {
            var roomId = $(this).closest('.dropable-room').attr('id');

            $(ui.helper).data('type', 'room_banner');

            $(ui.helper).data('room-id', roomId);

            console.log("ROOM ID:", roomId);

            $('.dropable-room').css("overflow-y", "hidden");
        },
        stop: function() {
            $('.dropable-room').css("overflow-y", "auto");
        },
        helper: function() {
            return $(this).clone().css({
                'width': '250px'
            });
        }
    });

    $(".draggable_number").draggable({
        revert: "invalid",
        helper: "clone",
        snap: "dropable-room",
        start: function(event, ui) {

            if (this.classList.contains('internal')) {

                $(ui.helper).data('type', 'internal');

            } else if (this.classList.contains('external')) {

                $(ui.helper).data('type', 'external');

            }

            $(ui.helper).data('banner-id', this.id);

            $('.phone-number').css("overflow", "visible");
            $('.dropable-room').css("overflow-y", "hidden");
        },
        stop: function() {

            // console.log("STOPPED");

            $('.phone-number').css("overflow", "hidden");
            $('.phone-number').css("overflow-y", "scroll");
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

            var type = ui.helper.data('type');

            if (type == "room_banner") {
                var to_room = event.target.id;

                var caller_name_id = ui.draggable.find('.text').attr('id');

                var user_uuid = ui.draggable.find('.user_uuid').attr('id');

                var from_room = ui.helper.data('room-id');

                if (document.getElementById(caller_name_id).classList.contains('org')) {
                    m = true
                } else {
                    m = false
                }

                console.log("ORIGINAL:", [caller_name_id, from_room, to_room, m]);

                // socket.send(JSON.stringify({'details':[caller_name_id, from_room, to_room]}));

                send_cmd([caller_name_id, from_room, to_room, m, user_uuid]);

            } else if (type === "internal") {

                var room = $(this).closest('.dropable-room').attr('id');

                // console.log("INTERNAL", "ROOM:", room);

                var caller_name_id = ui.draggable.attr('id');

                exin([room, caller_name_id, 'internal']);

            } else if (type === "external") {

                var room = $(this).closest('.dropable-room').attr('id');

                // console.log("EXTERNAL", "ROOM:", room);

                var caller_name_id = ui.draggable.attr('id');

                exin([room, caller_name_id, 'external']);

            }
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
        body: JSON.stringify({ 'details': ['extensions'] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log(Responsedata);

        values = JSON.parse(Responsedata)

        for (let i = 0; i < values.length; i++) {
            user_data = values[i]

            $('#data_table').find('tbody').append(`<tr><td class="draggable_number internal" id="${user_data[3]}" ondblclick="edit_modal(this.id)"> <span id = "status-${user_data[3]}" style="color: red; font-size: 25px;">&#9679;</span> <a class = 'user_names' id = 'user_name-${user_data[3]}' > ${user_data[1]} </a> </td></tr>`);

        }

        md();
        es();

        // hide_overlay();
    });

fetch('/fetch_agent/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': 'data' })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        values = JSON.parse(Responsedata)['agents']

        console.log("USER VALUES: ", values);

        for (let i = 0; i < values.length; i++) {
            user_data = values[i]

            $('#data_table').find('tbody').append(`<tr><td class="draggable_number internal" id="${user_data[2]}" ondblclick="edit_modal(this.id)"> <span id = "status-${user_data[2]}" style="color: red; font-size: 25px;">&#9679;</span> <a class = 'user_names' id = 'user_name-${user_data[2]}' > ${user_data[1]} </a> </td></tr>`);

        }

        md();
        es();
    });

fetch('/get_data/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': ['external'] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log(Responsedata);

        values = JSON.parse(Responsedata)

        for (let i = 0; i < values.length; i++) {
            user_data = values[i]

            $('#data_table').find('tbody').append(`<tr><td class="draggable_number external" id="${user_data[0]}" ondblclick="edit_modal(this.id)"> <span id = "status-${user_data[0]}" style="color: red; font-size: 25px;">&#9679;</span> ${user_data[1]}</td></tr>`);

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
        body: JSON.stringify({ 'details': ['conferences'] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        $('#spinner_text').html('Fetching Conference Rooms..');

        show_overlay();

        crs = JSON.parse(Responsedata);

        for (let i = 0; i < crs.length; i++) {
            user_data = crs[i]

            if (user_data[1] != 1943) {

                // var div = document.createElement('div');

                // var hr = document.createElement('hr');

                // div.classList.add('scrollbar', 'dropable-room', 'col-first', 'col', 'style-3');

                // div.setAttribute('id', `${user_data[1]}`);
                ``
                // var ind = document.createElement('div');

                // ind.classList.add('room-heading', 'ho');

                // ind.setAttribute('id', `${user_data[0]}`);

                // d = document.createTextNode(`${user_data[0].toUpperCase()}`);

                // ind.appendChild(d);

                // div.appendChild(ind);

                // div.appendChild(hr);

                total_container.push(user_data[1]);

                room_html = `
            <div class="scrollbar dropable-room col-first col style-3" id="${user_data[1]}">
                <div class="room-heading ho" id="${user_data[0]}">
                    <div class="heading-${user_data[0]} inflex">${user_data[0].toUpperCase()}</div>
                    <div class="switch-inflex inflex" id = "switch-${user_data[1]}" onclick="toggleVisibility(this.id, true)" style = "display: none;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="#000000" class="bi bi-stop-fill" viewBox="0 0 16 16">
                            <path d="M5 3.5h6A1.5 1.5 0 0 1 12.5 5v6a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 11V5A1.5 1.5 0 0 1 5 3.5z"></path>
                        </svg>
                    </div>
                </div>
                <hr>
            </div>
            `

                document.getElementById('bg_container').innerHTML += room_html;
            }

        }

        md();
        es();
        hide_overlay();
    });


function active_calls() {
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

            if (total_active_calls != "No Queues") {
                const keys = Object.keys(total_active_calls);

                for (const dict_key in total_active_calls) {
                    var room = dict_key;
                    callers = values(d[dict_key]['users']);
                    callers.forEach(element => {
                        const container = document.getElementById(room);
                        const myDiv = container.querySelector(`#element-${element[0]}`);

                        if (myDiv) {
                            // pass
                        } else {

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

                            $('.toggler').click(function() {
                                $('.toggler').not(this).prop('checked', false);
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

$("#saveColor").click(function() {
    var font_color = $("#fontColorPicker").val();
    var background_color = $("#backgroundColorPicker").val();

    $(`#element-${banner_clicked}`).css("background-color", background_color);
    $(`#${banner_clicked}`).css("color", font_color);

    $('#colorModal').modal('hide')
});

$("#savenote").click(function() {
    var my_note = $("#mynote").val();

    notes[`${double_clicked}`] = my_note;

    var childDiv = document.getElementById(double_clicked);
    var parent = document.getElementById(childDiv.parentNode.id);

    wip = document.getElementById(double_clicked.replace('element-', '')).innerHTML

    let match = wip.match(/\(([\w\d]+)\)/);
    let result = match ? match[1] : null;

    // console.log("DOUBLE CLICKED", double_clicked)
    // console.log("INNER HTML", document.getElementById(double_clicked.replace('element-', '')).innerHTML)
    // console.log("WIP", wip);
    // console.log("MATCH", match);
    // console.log("RESULT:", result);

    if (parent.offsetWidth < 400) {
        document.getElementById(double_clicked.replace('element-', '')).innerHTML = `(${result})` + ` ${my_note.substring(0, 15)}`;
    } else {
        document.getElementById(double_clicked.replace('element-', '')).innerHTML = `(${result})` + ` ${my_note}`;
    }

    $('#noteModal').modal('hide')
});

$("#modal-close").click(function() {

    $('#colorModal').modal('hide')
});

$("#note-close").click(function() {

    $('#noteModal').modal('hide')
});

function expand_room(name) {
    var childDiv = document.getElementById(name);
    var parent = document.getElementById(childDiv.parentNode.id);

    double_clicked = name;

    if (double_clicked) {

        wip = document.getElementById(double_clicked.replace('element-', '')).innerHTML

        let match = wip.match(/\(([\w\d]+)\)/);
        let result = match ? match[1] : null;

        // console.log("DOUBLE CLICKED", double_clicked)
        // console.log("INNER HTML", document.getElementById(double_clicked.replace('element-', '')).innerHTML)
        // console.log("WIP", wip);
        // console.log("MATCH", match);
        // console.log("RESULT:", result);

        my_note = notes[double_clicked]

        if (parent.offsetWidth < 400) {
            parent.style.width = "900px";
            document.getElementById(double_clicked.replace('element-', '')).innerHTML = `(${result})` + ` ${my_note}`;
        } else {
            parent.style.width = "300px";
            document.getElementById(double_clicked.replace('element-', '')).innerHTML = `(${result})` + ` ${my_note.substring(0, 15)}`
        };
    }
}

socket.onopen = function() {
    console.log('WebSocket connection established.');

    $('#spinner_text').html('connection established');

    // hide_overlay();
};

socket.onmessage = function(event) {

    console.log("EVENT", event.data)

    const data = JSON.parse(event.data);

    // console.log("CONTAINERS: ", total_container)

    if (data != "No Queues") {

        console.log("DATA: ", data);

        if ('DP' in data) {

            console.log("DATA RECEIVED: ", data);

            // console.log("DATA SORTED: ", data['DP']);

            // console.log("USER: ", data['DP'][0]);

            var dtmf_room = document.getElementById(data['DP'][0]);

            if (data['DP'][1] == "0") {

                dtmf_room.style.backgroundImage = "linear-gradient(to top, red 72%, #f2f2f2 72%)";

                toggleVisibility(`switch-${data['DP'][0]}`, false);

            }

            // console.log("DTMF ROOM: ", dtmf_room);

        } else if ('change_room' in data) {

            if (data['change_room'][1] != my_rsa) {

                toggleVisibility(data['change_room'][0], false);

                console.log("ROOM CHANGE:", data['change_room']);
            };

        } else if ('active_agents' in data) {

            data['active_agents'].forEach(elem => {
                change_status(`status-${elem}`);
            });

            console.log("STATUS CHANGE:", data['active_agents']);

        } else if ('exception_room' in data) {

            var exp_user = data['exception_room'][0];
            var user_room = data['exception_room'][0];

            if (document.getElementById(exp_user).classList.contains('org')) {
                m = true
            } else {
                m = false
            }

            console.log("SWITCH ROOM:", exp_user, "ORG: ", m, "ROOM: ", user_room);

            // send_cmd([exp_user, user_room, to_room, m]);

        } else {

            console.log("INITIAL CONFERENCE: ", conferences);

            if ('add' in data) {

                if (data['add'][1] in conferences) {
                    console.log("EXISTING CONFERENCE");

                    conferences[data['add'][1]]['users'][data['add'][3]] = [data['add'][4], data['add'][5], data['add'][3]]

                } else {
                    console.log("NEW CONFERENCE");

                    // var channel_uuid = data['add'][3];
                    var users_dict = {
                        [data['add'][3]]: [data['add'][4], data['add'][5], data['add'][3]]
                    }

                    conferences[data['add'][1]] = {
                        "conference_uuid": data['add'][2],
                        "users": users_dict,
                        "font": data['add'][6],
                        "background": data['add'][7],
                        "url": data['add'][8],
                        "mark": data['add'][0]
                    };
                }
            } else if ('remove' in data) {
                var rr = data['remove'][0]
                var ro = conferences[rr]['users']
                var ri = data['remove'][1]

                // console.log("VALUES: ", rr, ro, ri);

                delete ro[ri]

                if (Object.keys(ro).length == 0) {
                    delete conferences[data['remove'][0]]
                }
            }

            global_var = conferences;

            total_container.forEach(my_id => {
                var my_container = document.getElementById(my_id);
                const childNodes = my_container.childNodes;
                childNodes.forEach(node => {
                    if (node.tagName === 'DIV' && node.classList.contains("room-banner")) {
                        my_container.removeChild(node);
                    }
                });
            });

            for (const dict_key in conferences) {
                var room = dict_key;
                // store_response = room;

                console.log("ROOM : ", room)
                room = room.replace(/@138.201.188.127|%138.201.188.127|138.201.188.127/g, '');

                if (room != '1943') {

                    callers = Object.values(conferences[dict_key]['users']);
                    callers.forEach(element => {

                        // console.log("ELEMENT NEW: ", element)

                        const container = document.getElementById(room);
                        const myDiv = container.querySelector(`#element-${element[1]}`);

                        // console.log("ELEMENT:", element, "ROOM ID: ", room, "myDiv: ", myDiv, "ELEMENT: ", element[1]);

                        if (myDiv) {
                            // pass
                        } else {

                            active_users[element[1]] = [room, element[2]];

                            if (conferences[dict_key]['mark']) {
                                my_class = "text org"
                            } else {
                                my_class = `text mod dtmf-${element[0]}`
                            }

                            raw_html = `
                                <div ondblclick = 'expand_room(this.id)' style = "background-color:${conferences[dict_key]['background']}; color:${conferences[dict_key]['font']};" class="container draggable_banner noselect room-banner" id="element-${element[1]}">
                                    <div class="${my_class}" id="${element[1]}">(${element[0]})</div>
                                    <div class="user_uuid menu-wrap" id = "${data['add'][3]}">
                                        <input type="checkbox" class="toggler">
                                        <div class="dots">
                                            <div></div>
                                        </div>
                                        <div class="menu">
                                            <div>
                                                <ul>
                                                    <li><a class="link myurl" id="${element[0]}-url" href="${conferences[dict_key]['url']}" target="_blank">Url</a></li>
                                                    <li><a class="link" id = '${element[0]}-click' onclick = "set_value(this.id)" >Colour</a></li>
                                                    <li><a class="link" id = 'note-${element[1]}' onclick = "set_note(this.id)" > Note </a></li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>`

                            $(`#${room}`).append(raw_html);

                            $('.toggler').click(function() {
                                $('.toggler').not(this).prop('checked', false);
                            });

                            md();
                        }
                    });
                }
            }
        }

    }

};

// if (new_session) {
//     socket.send("{'new_session':[]}")
// }

// new_session = false;