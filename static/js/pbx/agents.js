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

function clear_entries() {

    $("#agent_name").val('');

    $("#agent_number").val('');

    $("#agent_pin").val('');
}

show_overlay(); 

$("#saveagent").click(function(){
    var name = $("#agent_name").val();

    var number = $("#agent_number").val();

    var pin = $("#agent_pin").val();

    $('#AgentModal').modal('hide')

    var send_data = [name, number, pin]

    console.log("SENDING: ", send_data);

    clear_entries();

    fetch('/save_agent/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': send_data })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log("RESPONSE:", Responsedata);
    
        // prased = JSON.parse(Responsedata)

        if ("success" in JSON.parse(Responsedata)) {
            // console.log('WORKED');

            location.reload()

        } else {
            console.log("failed");
        }
    });
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

    // console.log("RESPONSE:", Responsedata);
    // console.log("RESPONSE TYPE:", typeof Responsedata);

    var table = document.getElementById('AgentsTable');

    var agent_num = 1;

    JSON.parse(Responsedata)['agents'].forEach(element => {

        // Create a new row
        var row = table.insertRow();

        // Create a new cell and add some content

        var cell0 = row.insertCell();

        cell0.innerHTML = `${element[0]}`;

        var cell1 = row.insertCell();

        cell1.innerHTML = `${element[1]}`;

        var cell2 = row.insertCell();

        cell2.innerHTML = `${element[2]}`;

        var cell3 = row.insertCell();

        cell3.innerHTML = `${element[3]}`;
        agent_num += 1;
        
    });

    // prased = JSON.parse(Responsedata)

    // if ("success" in Responsedata) {
    //     console.log('WORKED')
    // } else {
    //     console.log("failed");
    // }

    clear_entries();
    
    hide_overlay();
});

function get_name(user_number) {

    fetch('/get_data/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': ['extensions', user_number] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {
    
        console.log(Responsedata);
    
        values = JSON.parse(Responsedata);

    });
}