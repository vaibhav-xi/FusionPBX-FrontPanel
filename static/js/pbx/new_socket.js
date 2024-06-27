new_socket.onclose = function(event) {
    console.log('WebSocket connection closed.', event);
    $('#spinner_text').html('Connecting to Server...');
    show_overlay();
};

new_socket.onopen = function() {
    console.log('NewSocket connection established.');

    $('#spinner_text').html('connection established');
};

new_socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    console.log("NEW SOCKET DATA: ", data);

    if (data['message'] == 'dump') {

        console.log("REMOVE USER DATA: ", data);

        if (typeof data['data'] == "string") {
            banneruuid = JSON.parse(data['banner_uuid'])
        } else {
            banneruuid = data['banner_uuid']
        }

        remove_banner(banneruuid);

    }
};