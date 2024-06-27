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

show_overlay();

function get_stats() {
    fetch('/agent_record/', {
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
