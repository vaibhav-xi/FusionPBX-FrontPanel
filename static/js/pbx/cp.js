const socket = new WebSocket('ws://' + '138.201.188.127' + ':8001/ws/myconsumer/');

const new_socket = new WebSocket('ws://' + '138.201.188.127' + ':8005/ws/myconsumer/');

show_overlay();
$('#spinner_text').html('Connecting to server');


socket.onclose = function(event) {
    console.log('WebSocket connection closed.', event);
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

var notes = {};
var mydict = {};
var active_users = {};

var conferences = {};

var time_elements = {};

var mark;

var global_var;

var total_container = [];

var my_rsa = "";

var new_session = true;

var rooms = {};

var banners_color = {};

var banner_time = {};

function set_value(banner_id) {
    // console.log("BANNER CLICKED: ", banner_id);
    banner_clicked = banner_id.replace('-click', '');
    // console.log("BANNER CLICKED (MOD): ", banner_clicked);
    $('#colorModal').modal('show')
}

var store_response;

function closestElementByClass(element, className) {
    var parent = element.parentElement;

    while (parent) {
        if (parent.classList.contains(className)) {
            return parent;
        }
        parent = parent.parentElement;
    }

    return null;
}

function startTimer(timerElement, initialTime) {
    let time = initialTime;
    let intervalId;

    function updateTimer() {
        time++;

        if (time < 0) {
            clearInterval(intervalId);
            return;
        }

        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        timerElement.textContent = formattedTime;

        var closest_div = closestElementByClass(timerElement, 'draggable_banner').classList.item(4);

        // console.log("TIMER ELEMENT: ", closest_div);

        time_elements[closest_div] = time;
    }

    updateTimer();
    intervalId = setInterval(updateTimer, 1000);
}

function send_cmd(cmd) {

    console.log("TRANSFER CALL: ", cmd)

    fetch('/pbx/cmd_transfer/', {
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

                console.log("CONFERENCES SUCCESS: ", conferences);

            } else {
                console.log("failed");
            }
        });
}

function exin(cmd) {
    fetch('/pbx/exin_transfer/', {
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

function uuid_transfer(user_uuid, from_room, to_room) {

    console.log("DROP TRANSFER: ", user_uuid, from_room, to_room)

    remove_banner(user_uuid);

    fetch('/pbx/uuid_transfer/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': [user_uuid, from_room, to_room] })
        })
        .then((resp) => resp.json())
        .then(response => {

            console.log("FORWARD RES: ", response);

            received_data = JSON.parse(response);

            if ("success" in received_data) {
                mroom = received_data['success'];
                uid = received_data['uuid'];
                console.log("ForwardSuccess: ", received_data, mroom, uid);

                remove_banner(uid);

                socket.send(JSON.stringify({ 'message': "forwarded_room", 'data': mroom }));
            }
        });

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

                console.log("ORIGINAL:", [user_uuid, from_room, to_room]);

                // socket.send(JSON.stringify({'details':[caller_name_id, from_room, to_room]}));

                uuid_transfer(user_uuid, from_room, to_room);

            } else if (type === "internal") {

                var room = $(this).closest('.dropable-room').attr('id');

                // console.log("INTERNAL", "ROOM:", room);

                var caller_name_id = ui.draggable.attr('id');

                exin([room, caller_name_id, 'internal']);

            } else if (type === "external") {

                var room = $(this).closest('.dropable-room').attr('id');

                var caller_name_id = ui.draggable.attr('id');

                console.log("EXTERNAL", "ROOM:", room, "CALLER ID: ", caller_name_id);

                exin([room, caller_name_id, 'external']);

            }
        }
    });
}

show_overlay();
$('#spinner_text').html('Fetching Users');

fetch('/pbx/agents/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': ['external'] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        values = JSON.parse(Responsedata)

        for (const agent in values) {

            const imv = values[agent]

            // console.log(agent, values[agent]);

            $('#data_table').find('tbody').append(`<tr><td class="draggable_number external" id="${imv[0]}" ondblclick="edit_modal(this.id)"> <span id = "status-${imv[0]}" style="color: ${imv[1]}; font-size: 25px;">&#9679;</span> ${agent}</td></tr>`);

        }

        md();
        es();

    });

    fetch('/pbx/get_data/', {
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

    function dump_call(uuid, total_time, my_room) {

        console.log("DUMPING: ", uuid, total_time, my_room);

        fetch('/pbx/dump_call/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': [uuid, total_time, my_room] })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {
    
            console.log("CALL DUMPED: ", Responsedata, Responsedata["uuid"]);

            remove_banner(Responsedata["uuid"]);
        });
    }

    fetch('/pbx/get_data/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': ['call_centers'] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        $('#spinner_text').html('Fetching CallQueues..');

        show_overlay();

        crs = JSON.parse(Responsedata);

        console.log("CallCenters: ", crs);

        for (let i = 0; i < crs.length; i++) {
            user_data = crs[i]

            if (user_data[4] != 1943) {

                total_container.push(user_data[4]);

                room_html = `
            <div class="scrollbar dropable-room col-first col style-3" id="${user_data[4]}">
                <div class="room-heading ho" id="${user_data[0]}">
                    <div class="heading-${user_data[0]} inflex">${user_data[3].toUpperCase()}</div>
                    <div class="switch-inflex inflex" id = "switch-${user_data[4]}" onclick="toggleVisibility(this.id, true)" style = "display: none;">
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

function forward_room(my_data) {

    banner_uid = my_data.split('.')[1]

    remove_banner(banner_uid);

    fetch('/pbx/forward_call/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': my_data })
        })
        .then((resp) => resp.json())
        .then(response => {

            console.log("FORWARD RES: ", response);

            // received_data = JSON.parse(response);

            var forwardRes = JSON.parse(response.forward_res);
            var outboundRes = JSON.parse(response.outbound_res);

            if ("success" in forwardRes) {
                mroom = forwardRes['success'];
                console.log("ForwardSuccess: ", forwardRes, mroom);
            }
            if ("uuid" in forwardRes) {
                console.log("FORWARD_UUID: ", forwardRes["uuid"]);
                remove_banner(forwardRes["uuid"]);
            }
            
        });
}

function active_calls() {
    fetch('/pbx/activecalls/', {
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
                    callers.forEach(users_obj => {
                        const container = document.getElementById(room);
                        const myDiv = container.querySelector(`#users_obj-${users_obj[0]}`);

                        if (myDiv) {
                            // pass
                        } else {

                            raw_html = `
                            <div ondblclick = 'set_note(this.id)' style = "background-color:${total_active_calls[dict_key]['background']}; color:${total_active_calls[dict_key]['font']};" class="container draggable_banner noselect room-banner" id="users_obj-${users_obj[1]}">
                                <div class="text" id="${users_obj[1]}">${users_obj[0]}</div>
                                <div class="menu-wrap">
                                    <input type="checkbox" class="toggler">
                                    <div class="dots">
                                        <div></div>
                                    </div>
                                    <div class="menu">
                                        <div>
                                            <ul>
                                                <li><a class="link myurl" id="${users_obj[0]}-url" href="${total_active_calls[dict_key]['url']}" target="_blank">Url</a></li>
                                                <li><a class="link" id = '${users_obj[0]}-click' onclick = "set_value(this.id)" >Colour</a></li>
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
                            var id = divs[i].id.replace('users_obj-', "");
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

    // banner_id = document.getElementsByClassName(banner_clicked)[0].id;
    banner_id = document.getElementsByClassName(`users_obj-${banner_clicked}`)[0].id;

    $(`#${banner_id}`).css("background-color", background_color);
    $(`#${banner_id}`).css("color", font_color);

    banners_color[banner_clicked] = [font_color, background_color];

    socket.send(JSON.stringify({ 'message': "save_color", 'data': banners_color }));

    $('#colorModal').modal('hide')
});

$("#savenote").click(function() {
    var my_note = $("#mynote").val();

    notes[`${double_clicked}`] = my_note;

    var childDiv = document.getElementById(double_clicked);
    var parent = document.getElementById(childDiv.parentNode.id);

    wip = document.getElementById(double_clicked.replace('users_obj-', ''));

    let match = wip.innerHTML.match(/\(([\w\d]+)\)/);
    let result = match ? match[1] : null;


    console.log("SAVING NOTE: ", my_note);
    console.log("WIP: ", wip);

    if (parent.offsetWidth < 400) {
        console.log("CHANGING SMOL");
        document.getElementById(double_clicked.replace('users_obj-', '')).innerHTML = `${my_note.substring(0, 35)}`;
    } else {
        document.getElementById(double_clicked.replace('users_obj-', '')).innerHTML = `${my_note}`;
        console.log("CHANGING BIG");
    }

    socket.send(JSON.stringify({ 'message': "save_note", 'data': notes }));

    $('#noteModal').modal('hide')
});

$("#modal-close").click(function() {

    $('#colorModal').modal('hide')
});

$("#note-close").click(function() {

    $('#noteModal').modal('hide')
});

function expand_room(name) {
    var m_id = name.replace('expand-', 'users_obj-').replace('contract-', 'users_obj-')
    var childDiv = document.getElementById(m_id);
    var parent = document.getElementById(childDiv.parentNode.id);

    double_clicked = m_id;

    if (double_clicked) {

        wip = document.getElementById(double_clicked.replace('users_obj-', '')).innerHTML

        let match = wip.match(/\(([\w\d]+)\)/);
        let result = match ? match[1] : null;

        // console.log("DOUBLE CLICKED", double_clicked)
        // console.log("INNER HTML", document.getElementById(double_clicked.replace('users_obj-', '')).innerHTML)
        // console.log("WIP", wip);
        // console.log("MATCH", match);
        // console.log("RESULT:", result);

        my_note = notes[double_clicked];

        console.log("MY NOTE: ", my_note);

        if (parent.offsetWidth < 400) {
            parent.style.width = "900px";
            wip = `${my_note}`;
            $(`#${name}`).css('display', 'none');
            $(`#${name.replace('expand-', 'contract-')}`).css('display', 'block');
        } else {
            parent.style.width = "300px";
            wip = `${my_note.substring(0, 35)}`
            $(`#${name}`).css('display', 'none');
            $(`#${name.replace('contract-', 'expand-')}`).css('display', 'block');
        };
    }
}

function timeStringToSeconds(timeString) {
    const [minutes, seconds] = timeString.split(':').map(Number);
    const totalSeconds = minutes * 60 + seconds;
    return totalSeconds;
}

function update_time(div_id, seconds) {
    // Calculate minutes and seconds
    var minutes = Math.floor(seconds / 60);
    var remainingSeconds = seconds % 60;

    // Format minutes and seconds with leading zeros if necessary
    var formattedTime = (minutes < 10 ? '0' : '') + minutes + ':' + (remainingSeconds < 10 ? '0' : '') + remainingSeconds;

    mydiv = document.getElementById(div_id);
    
    if (mydiv) {
        mydiv.innerHTML = formattedTime;
    }
}

function forward_check(frooms) {
    console.log("FORWARD ROOMS: ", frooms);

    for (const dict_key in frooms) {
        console.log("FORWARD ROOM: ", dict_key);
        console.log("VALUES: ", frooms[dict_key]);

        if (frooms[dict_key]["destroyed"] == true && frooms[dict_key]["state"] == "timeout") {
            uuid_transfer(frooms[dict_key]["uuid"], "", "111");

            if (socket.readyState === WebSocket.OPEN) {
                // If it's open, send the message
                socket.send(JSON.stringify({ 'message': "delete_forward", 'data': {"room":dict_key} }));
            } else {
                // If it's not open, wait for the connection to be established
                socket.addEventListener('open', function() {
                    // Now that the socket is open, send the message
                    socket.send(JSON.stringify({ 'message': "delete_forward", 'data': {"room":dict_key} }));
                });
            }

            console.log("CALL TIMEOUT", "send home: ", frooms[dict_key]["uuid"]);
        }

        if (frooms[dict_key]["destroyed"] == true && frooms[dict_key]["state"] == "completed") {
            if (frooms[dict_key]["complete_time"] != false) {
                
                console.log("CALL COMPLETED", "TOTAL TIME: ", frooms[dict_key]["complete_time"], "Hangup: ", frooms[dict_key]["uuid"]);
                
                dump_call(frooms[dict_key]["uuid"], frooms[dict_key]["complete_time"], dict_key);

                if (socket.readyState === WebSocket.OPEN) {
                    // If it's open, send the message
                    socket.send(JSON.stringify({ 'message': "delete_forward", 'data': {"room":dict_key} }));
                } else {
                    // If it's not open, wait for the connection to be established
                    socket.addEventListener('open', function() {
                        // Now that the socket is open, send the message
                        socket.send(JSON.stringify({ 'message': "delete_forward", 'data': {"room":dict_key} }));
                    });
                }
            }
        }
    }
}

function new_data(conferences) {

    console.log("CONFERENCES: ", conferences);

    if ("forward_rooms" in conferences) {
        forward_check(conferences["forward_rooms"]);
    }

    // total_container.forEach(my_id => {
    //     var my_container = document.getElementById(my_id);
    //     const childNodes = my_container.childNodes;
    //     childNodes.forEach(node => {
    //         if (node.tagName === 'DIV' && node.classList.contains("room-banner")) {
    //             my_container.removeChild(node);
    //         }
    //     });
    // });

    for (const dict_key in conferences) {
        var room = dict_key;

        if (conferences[dict_key]['users']) {
            user_count = Object.keys(conferences[dict_key]['users']).length;
        } else {
            user_count = 0
        }

        rooms[room] = user_count;

        if (room != '1943' && conferences[dict_key]['users']) {

            callers = Object.values(conferences[dict_key]['users']);
            callers.forEach(users_obj => {

                console.log("Users: ", users_obj, "MY ROOM: ", room);
                console.log("Active Users: ", active_users, (users_obj['uuid'] in active_users));

                update_time(`${users_obj['uuid']}_timer`, users_obj['timer']);

                if (users_obj['uuid'] && !(users_obj['uuid'] in active_users)) {

                    const container = document.getElementById(room);

                    const myDiv = (container && users_obj['uuid']) ? container.querySelector(`#users_obj-${users_obj['uuid']}`) : null;

                    if (myDiv) {
                        // pass
                    } else {

                        active_users[users_obj['uuid']] = [room, users_obj['uuid']];

                        if (conferences[dict_key]['mark']) {
                            my_class = "text org"
                        } else {
                            my_class = `text mod dtmf-${users_obj['cid_name']} ${users_obj['cid_name']}`
                        }

                        console.log("deatils: ", conferences[dict_key]['background'], conferences[dict_key]['font']);

                        if (users_obj['cid_name'] in banners_color) {
                            //pass
                            console.log("Colors Already Exist");
                        } 
                        
                        else if (!("banner_color" in users_obj) && !("font_color" in users_obj)) {

                            console.log("BANNER DATA NOT THERE");

                            if (!(users_obj['cid_name'] in banners_color)) {

                                console.log("SETTING DEFAULT VALUE");

                                my_background = "#e6e6fa";
                                my_font = "#000000";

                                banners_color[users_obj['cid_name']] = [my_font, my_background];
                            }

                        } 
                        
                        else if ("banner_color" in users_obj && "font_color" in users_obj) {

                            console.log("BANNER DATA EXIST");

                            if (!(users_obj['cid_name'] in banners_color)) {

                                console.log("SETTING NEW DATA");

                                if (users_obj['banner_color'] == undefined || users_obj['banner_color'] == "" || users_obj['banner_color'] == 'None') {
                                    console.log("VALUES NULL, SETTING DEFAULT");
                                    my_background = "#e6e6fa";
                                } else {
                                    console.log("VALUES NOT NULL, SETTING IT");
                                    my_background = users_obj['banner_color'];
                                }
    
                                if (users_obj['font_color'] == undefined || users_obj['font_color'] == "" || users_obj['font_color'] == 'None') {
                                    console.log("VALUES NULL, SETTING DEFAULT");
                                    my_background = "#e6e6fa";
                                } else {
                                    console.log("VALUES NOT NULL, SETTING IT");
                                    my_font = users_obj['font_color'];
                                }
    
                                banners_color[users_obj['cid_name']] = [my_font, my_background];

                            }
                        }

                        console.log("BANNER COLORS: ", banners_color);

                        // if (socket.readyState === WebSocket.OPEN) {
                        //     // If it's open, send the message
                        //     socket.send(JSON.stringify({ 'message': "save_color", 'data': banners_color }));
                        // } else {
                        //     // If it's not open, wait for the connection to be established
                        //     socket.addEventListener('open', function() {
                        //         // Now that the socket is open, send the message
                        //         socket.send(JSON.stringify({ 'message': "save_color", 'data': banners_color }));
                        //     });
                        // }

                        if (`users_obj-${users_obj['uuid']}` in notes) {
                            console.log("NOTE EXIST: ", `users_obj-${users_obj['uuid']}`);

                            m_note = notes[`users_obj-${users_obj['uuid']}`];
                        } else {
                            console.log("SAVING NOTE: ", `${users_obj}`);

                            mnote = users_obj['description']

                            console.log(`SAVED NOTES: ${notes}`);

                            if (mnote == undefined) {
                                mnote = "";
                            }
 
                            m_note = `(${users_obj['cid_name']}) ${mnote}`;
                            notes[`users_obj-${users_obj['uuid']}`] = m_note;

                            if (socket.readyState === WebSocket.OPEN) {
                                // If it's open, send the message
                                socket.send(JSON.stringify({ 'message': "save_note", 'data': notes }));
                            } else {
                                // If it's not open, wait for the connection to be established
                                socket.addEventListener('open', function() {
                                    // Now that the socket is open, send the message
                                    socket.send(JSON.stringify({ 'message': "save_note", 'data': notes }));
                                });
                            }
                        }

                        raw_html = `
                            <div ondblclick = "set_note(this.id)" style = "background-color:${my_background}; color:${my_font};" class="container draggable_banner noselect room-banner users_obj-${users_obj['cid_name']}" id="users_obj-${users_obj['uuid']}">
                                <div class="timer" id="${users_obj['uuid']}_timer">00:00</div>
                                <div class="${my_class}" id="${users_obj['uuid']}">${m_note}</div>
                                <div class="room_action">
                                    <svg onclick = 'expand_room(this.id)' style = "display: block;" id = "expand-${users_obj['uuid']}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="expand_room bi bi-arrows-angle-expand" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M5.828 10.172a.5.5 0 0 0-.707 0l-4.096 4.096V11.5a.5.5 0 0 0-1 0v3.975a.5.5 0 0 0 .5.5H4.5a.5.5 0 0 0 0-1H1.732l4.096-4.096a.5.5 0 0 0 0-.707zm4.344-4.344a.5.5 0 0 0 .707 0l4.096-4.096V4.5a.5.5 0 1 0 1 0V.525a.5.5 0 0 0-.5-.5H11.5a.5.5 0 0 0 0 1h2.768l-4.096 4.096a.5.5 0 0 0 0 .707z"/>
                                    </svg>

                                    <svg onclick = 'expand_room(this.id)' style = "display: none;" id = "contract-${users_obj['uuid']}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="contract_room bi bi-arrows-angle-contract" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M.172 15.828a.5.5 0 0 0 .707 0l4.096-4.096V14.5a.5.5 0 1 0 1 0v-3.975a.5.5 0 0 0-.5-.5H1.5a.5.5 0 0 0 0 1h2.768L.172 15.121a.5.5 0 0 0 0 .707zM15.828.172a.5.5 0 0 0-.707 0l-4.096 4.096V1.5a.5.5 0 1 0-1 0v3.975a.5.5 0 0 0 .5.5H14.5a.5.5 0 0 0 0-1h-2.768L15.828.879a.5.5 0 0 0 0-.707z"/>
                                    </svg>
                                </div>
                                <div class="user_uuid menu-wrap" id = "${users_obj['uuid']}">
                                    <input type="checkbox" class="toggler">
                                    <div class="dots">
                                        <div></div>
                                    </div>
                                    <div class="menu">
                                        <div>
                                            <ul>
                                                <li><a class="link myurl" id="${users_obj['cid_name']}-url" href="${conferences[dict_key]['url']}" target="_blank">Url</a></li>
                                                <li><a class="link" id = '${users_obj['cid_name']}-click' onclick = "set_value(this.id)" >Colour</a></li>
                                                <li><a class="link" id = 'note-${users_obj['uuid']}' onclick = "set_note(this.id)" > Note </a></li>
                                                <li><a class="link" id = '${room}.${users_obj['uuid']}.${users_obj['initial_dest']}' onclick = "forward_room(this.id)" > Forward </a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>`

                        console.log("ADDING USER: ", users_obj['uuid']);

                        $(`#${room}`).append(raw_html);

                        $('.toggler').click(function() {
                            $('.toggler').not(this).prop('checked', false);
                        });

                        md();
                    }
                } else {
                    console.log("USER EXIST: ", users_obj['uuid']);
                }
            });
        }
    }
}


socket.onopen = function() {
    console.log('WebSocket connection established.');

    socket.send('{"message":"new_session"}');

    $('#spinner_text').html('connection established');

    // hide_overlay();
};

socket.onmessage = function(event) {

    const data = JSON.parse(event.data);

    if (data != "No Queues") {

        if ('DP' in data) {

            console.log("DATA RECEIVED: ", data);

            var dtmf_room = document.getElementById(data['DP'][0]);

            if (data['DP'][1] == "0") {

                dtmf_room.style.backgroundImage = "linear-gradient(to top, red 72%, #f2f2f2 72%)";

                toggleVisibility(`switch-${data['DP'][0]}`, false);

            } else if (data['DP'][1] == "5") {

                if (document.getElementById(data['DP'][2]).classList.contains('org')) {
                    m = true
                } else {
                    m = false
                }

                console.log("M TYPE: ", data['DP'][0], typeof data['DP'][0], document.getElementById(data['DP'][0]), document.getElementById(data['DP'][0]).classList.contains('org'));

                console.log("SENDING DATA: ", [data['DP'][2], data['DP'][0], '5555', m, 'user_uuid'])

                send_cmd([data['DP'][2], data['DP'][0], '5555', m, 'user_uuid']);
            }

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

            if ('message' in data && data['message'] == 'fetch') {

                console.log("DATA CHECK: ", data, typeof data, data['data'], typeof data['data'])

                if (typeof data['data'] == "string") {
                    mdata = JSON.parse(data['data'])
                } else {
                    mdata = data['data']
                }

                if ('remove_note' in data) {

                    if (data['remove_note'] in notes) {

                        delete notes[data['remove_note']];
                    }

                }
                if ('remove_color' in data) {

                    if (data['remove_color'] in banners_color) {

                        delete banners_color[data['remove_color']];

                    }

                }

                if ('add_note' in data) {
                    notes = data['add_note']
                }

                if ('add_color' in data) {
                    banners_color = data["add_color"]
                }

                if (Object.keys(mdata).length >= 1) {
                    new_data(mdata);
                } else {
                    new_data({});
                }


            }

            if (data['message'] == 'dump') {

                console.log("REMOVE USER DATA: ", data);

                if (typeof data['data'] == "string") {
                    banneruuid = JSON.parse(data['banner_uuid'])
                } else {
                    banneruuid = data['banner_uuid']
                }

                remove_banner(banneruuid);

            }
        }

    }

};

function remove_banner(banneruuid) {
    console.log("REMOVING USER: ", banneruuid);

    delete active_users[banneruuid];

    total_container.forEach(my_id => {
        var my_container = document.getElementById(my_id);
        const childNodes = my_container.childNodes;
        childNodes.forEach(node => {
            if (node.tagName === 'DIV' && node.classList.contains("room-banner")) {
                if (node.id == `users_obj-${banneruuid}`) {
                    my_container.removeChild(node);
                }
            }
        });
    });

}

function myFunction() {
    socket.send(JSON.stringify({ 'message': "fetch_data"}));
  }
  
  setInterval(myFunction, 1000);