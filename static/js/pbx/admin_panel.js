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

function admin_data(ds) {

    console.log("SENDING DATA: ", ds);

    fetch('/admin_data/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': ds })
        })
        .then((resp) => resp.json())
        .then(response => {

            console.log("RESPONSE: ", response);

            parsed_data = JSON.parse(response);
            console.log(parsed_data);
        });
}

$("#user_submit").on("click", function() {

    client_address = document.getElementById("client_address").value;
    section1 = document.getElementById("address_section1").value;
    section2 = document.getElementById("address_section2").value;
    section3 = document.getElementById("address_section3").value;
    billing_period = document.getElementById("billing_period").value;
    client_name = document.getElementById("client_name").value;

    admin_data([client_address, section1, section2, section3, billing_period, client_name]);

});