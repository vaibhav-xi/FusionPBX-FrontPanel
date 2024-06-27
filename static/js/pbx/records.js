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

function formatTime(seconds) {
    if (typeof seconds === "string") {
        seconds = parseInt(seconds);
    }
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    const formattedHours = hours < 10 ? "0" + hours : hours;
    const formattedMinutes = minutes < 10 ? "0" + minutes : minutes;
    const formattedSeconds =
        remainingSeconds < 10 ? "0" + remainingSeconds : remainingSeconds;

    return `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
}

function formatTimestamp(timestamp) {
    // Create a new Date object from the timestamp
    const date = new Date(timestamp);

    // Define month names
    const monthNames = [
        "January", "February", "March",
        "April", "May", "June", "July",
        "August", "September", "October",
        "November", "December"
    ];

    // Get individual components of the date
    const day = date.getDate();
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    // Format the date and time
    const formattedDate = `${month} ${day}, ${year}`;
    const formattedTime = `${hours}:${minutes}:${seconds}`;

    // Combine date and time
    return `${formattedDate}, ${formattedTime}`;
}

function subtractTimes(startTime, endTime) {
    // Create Date objects from the provided timestamps
    const start = new Date(startTime);
    const end = new Date(endTime);

    // Calculate the difference in milliseconds
    let difference = end - start;

    // Convert the difference from milliseconds to hours, minutes, and seconds
    const hours = Math.floor(difference / (1000 * 60 * 60));
    difference -= hours * (1000 * 60 * 60);
    const minutes = Math.floor(difference / (1000 * 60));
    difference -= minutes * (1000 * 60);
    const seconds = Math.floor(difference / 1000);

    // Format the result as HH:MM:SS
    const formattedTime = [
        String(hours).padStart(2, '0'),
        String(minutes).padStart(2, '0'),
        String(seconds).padStart(2, '0')
    ].join(':');

    return formattedTime;
}

function get_flow(flow_uuid) {
    console.log(flow_uuid);

    window.location.href = `/pbx/records/${flow_uuid}`;
}

show_overlay();

function get_stats() {
    fetch('/call_stats/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': ['records'] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        data = JSON.parse(Responsedata);

        console.log("RECORDS: ", data, typeof data)

        data.forEach(elem => {

            $('#records_table').find('tbody').append(`<tr onclick="get_flow(this.id)" id = "${elem[3]}"><td> ${elem[0] }</td> <td> ${elem[1] }</td> <td> ${elem[2] }</td> <td> ${elem[4] }</td> <td> ${elem[5] }</td> <td> ${elem[6]}</td> <td> ${elem[7]}</td>  <td> ${elem[8]}</td>  <td> ${elem[9]}</td>  <td> ${formatTimestamp(elem[10])}</td>  <td> ${formatTimestamp(elem[11])}</td>  <td> ${subtractTimes(elem[10], elem[11])}</td></tr>`);

            hide_overlay();
        });

    });
}

// fetch('/pbx/get_data/', {
//         method: 'POST',
//         headers: {
//             'Content-type': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({ 'details': ['records'] })
//     })
//     .then((resp) => resp.json())
//     .then(function(Responsedata) {

//         // console.log(Responsedata);

//         values = JSON.parse(Responsedata)

//         for (let i = 0; i < values.length; i++) {
//             user_data = values[i]

//             $('#records_table').find('tbody').append(`<tr><td> ${user_data[0]}</td> <td> ${user_data[3] }</td> <td> ${user_data[4] }</td> <td> ${user_data[5] }</td> <td> ${user_data[6] }</td> <td> ${user_data[7] }</td> <td> ${formatTime(user_data[8])}</td> <td> ${user_data[9]}</td> </tr>`);

//         }

//         $('#total').text(`${values.length}`);

//         // console.log("LENGTH:", values.length())

//         hide_overlay();
//     });


function sortTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("inputField");
    filter = input.value.toUpperCase();
    table = document.getElementById("records_table");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td");

        for (var j = 0; j < td.length; j++) {
            var cell = td[j];
            if (cell) {
                txtValue = cell.textContent || cell.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break;
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}

get_stats();