

var global_id = "";
var agent_name = "";

function getAgentName(tdId) {
    // Get the td element by its ID
    var tdElement = document.getElementById(tdId);

    // Clone the td element to avoid modifying the original one
    var clone = tdElement.cloneNode(true);

    // Remove the span element from the clone
    var spanElement = clone.querySelector('span');
    if (spanElement) {
        clone.removeChild(spanElement);
    }

    // Get the inner text without the span element
    var innerText = clone.innerText.trim();

    return innerText;
}

function edit_modal(elem_id){
    var color = document.getElementById(`status-${elem_id}`).style.color;
    var name = getAgentName(elem_id);

    // un = elem_id;
    // n = name;

    global_id = elem_id;
    agent_name = name;

    if (color == 'red') {
        $('#user_name').val(`${name}:  User Not Available`);
    } else if (color == 'green') {
        $('#user_name').val(`${name}:  User Available`);
    } else {
        $('#user_name').val('Error');
    }

    $('#details').modal('show');
    
}

$("#save_details").on("click", function() {
    
    change_status(agent_name, `status-${global_id}`);

    $('#details').modal('hide');
});