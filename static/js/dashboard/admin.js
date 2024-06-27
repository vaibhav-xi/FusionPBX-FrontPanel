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

var selected;
var user;
var selected_agent = "none";
var selected_agent_room = "all";

function user_settings(m) {
    var url = '/get_settings/'

    selected = m;
    // data = [myname, message, mydate]

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'user_name': m })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            var settings_data = Responsedata["user_settings"];

            console.log("USER SETTINGS: ", Responsedata, settings_data, typeof settings_data);

            // if (settings_data[0]) {}

            // $('#daily_stats').bootstrapToggle('on');

            for (var key in settings_data) {
                if (settings_data.hasOwnProperty(key)) {
                    var my_id = key;
                    var mval = settings_data[key];
                    if (typeof mval == 'boolean') {

                        console.log("KEYS: ", my_id);

                        var my_val = mval ? "on" : "off";

                        $('#' + my_id).bootstrapToggle(my_val);
                    } else {
                        // $('#free_min').val(settings_data['free_min']);
                        // $('#free_calls').val(settings_data['free_calls']);
                    }
                }
            }
        })
}

function generate_invoice(m) {
    $("#des_invoice").val(m);
    $('#GenerateInvoice').modal('show');
}

function c_invoice(m) {
    $("#cli_name").val(m);
    $('#ClientInvoice').modal('show');
}

$('#gen_invoice').on('click', function() {

    var url = '/client_invoice/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': [$("#des_invoice").val(),
            $("#des_startdate").val(), $("#des_enddate").val(), "destintaion"] })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {
            console.log(Responsedata['message']);

            window.location.href = `/download_invoice/${Responsedata['message']}`;
        })
});

$('#client_invoice').on('click', function() {

    var url = '/client_invoice/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': [$("#cli_name").val(),
            $("#cli_startdate").val(), $("#cli_enddate").val(), "client"] })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {
            console.log(Responsedata['message']);

            window.location.href = `/download_invoice/${Responsedata['message']}`;
        })
});

$('#get_ivr_records').on('click', function() {

    var url = '/ivr_records/'

    show_overlay();

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': ['ivr_record', $("#ivr_startdate").val(), 
                $("#ivr_enddate").val(), $("#ivr_number").val()] })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            Resp_data = JSON.parse(Responsedata);

            $('#ivr_records_table').find('tbody').empty();

            $('#ivr_records_table').find('tbody').append(`<tr> 
                <td> ${$("#ivr_startdate").val() } </td> 
                <td> ${$("#ivr_enddate").val() } </td>
                <td> ${$("#ivr_number").val() } </td>
                <td> ${parseFloat(Resp_data[0]).toFixed(2).toString().replace(".", ",") } sec </td>
                <td> ${parseFloat(Resp_data[1]).toFixed(2).toString().replace(".", ",") } sec </td>
                <td> ${addNumbers(Resp_data[0], 0) } Mins </td>
                </tr>`);

            hide_overlay();

        })
});

function addNumbers(time1, time2) {
    // Convert time1 and time2 to numbers if they are strings
    let t1 = parseFloat(time1);
    let t2 = parseFloat(time2);

    // Handle NaN cases
    if (isNaN(t1) || isNaN(t2)) {
        return "Invalid input";
    }

    // Add the times
    let totalTime = t1 + t2;

    var minutes = Math.floor(totalTime / 60);
    var remainingSeconds = totalTime % 60;
    var decimalMinutes = minutes + remainingSeconds / 60;
    
    // Format the result to two decimal places
    var result = decimalMinutes.toFixed(2).toString().replace(".", ",");
    
    return result;
}

$('#client_details').on('click', function() {

    data = [selected,
        $("#daily_stats").prop("checked"),
        $("#weekly_stats").prop("checked"),
        $("#monthly_stats").prop("checked"),
        $("#invoice_creation").prop("checked"),
        $("#form_function").prop("checked"),
        $("#imp_sw").prop("checked"),
        $("#diss_sw").prop("checked"),
        $("#sales_sw").prop("checked"),
    ];

    console.log("SWITCH DATA: ", data);

    fetch('/update_settings/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'update_settings': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            // console.log(Responsedata);

            window.location.href = "";
        })
});

$('#save_price').on('click', function() {

    data = ["per_min",$("#selected_desname").val(),
        $("#selected_desprice").val()
    ];

    fetch('/update_des_price/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'save_price': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            // console.log(Responsedata);

            window.location.href = "";
        })
});

$('#des_settings').on('click', function() {

    data = [$("#selected_desname").val(),
        $("#des_ppc").val(), $("#des_ppm").val(),
        $("#des_fc").val(), $("#des_fm").val(), 
        $("#monhtly_fees").val(),
        $("#monthly_fee").prop("checked"),
        $("#charge_pc").prop("checked"),
        $("#charge_pm").prop("checked"),
        $("#forward_des").val(),
        $("#forward_cost").val(),
        $("#forward_number").val(),
    ];

    fetch('/update_des_price/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'save_price': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            // console.log(Responsedata);

            window.location.href = "";
        })
});

function getdes_settings() {
    data = [$("#selected_desname").val()];

    fetch('/fetch_des_settings/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'data': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            var settings_data = Responsedata["data"];

            console.log("USER SETTINGS: ", Responsedata, settings_data, typeof settings_data);

            for (var key in settings_data) {
                if (settings_data.hasOwnProperty(key)) {
                    var my_id = key;
                    var mval = settings_data[key];
                    if (typeof mval == 'boolean') {

                        console.log("KEYS: ", my_id);

                        var my_val = mval ? "on" : "off";

                        $('#' + my_id).bootstrapToggle(my_val);
                    } else {
                        $('#des_ppc').val(settings_data['ppc']);
                        $('#des_ppm').val(settings_data['ppm']);
                        $('#des_fc').val(settings_data['fc']);
                        $('#des_fm').val(settings_data['fm']);
                        $('#monhtly_fees').val(settings_data['mf']);

                        $('#forward_des').val(settings_data['forward_des']);
                        $('#forward_cost').val(settings_data['forward_cost']);
                        $('#forward_number').val(settings_data['forward_number']);
                        $('#forward_seconds').val(settings_data['forward_seconds']);
                    }
                }
            }
        })
}

$('#edit_userdetails').on('click', function() {

    data = [
        $("#edit_username").val(),
        $("#edit_useremail").val(),
        $("#edit_invoiceemail").val(),
        $("#edit_userstreet").val(),
        $("#edit_userzip").val(),
        $("#edit_userplace").val(),
        $("#edit_companyname").val(),
        $("#edit_usertax").val()
    ];

    fetch('/update_client/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'edit_client': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            // console.log(Responsedata);

            window.location.href = "";
        })
});

function edit_user(user_name) {

    fetch('/getuserdetails/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'username': user_name.replace("-edit", "") })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            $("#edit_username").val(Responsedata[0]);
            $("#edit_useremail").val(Responsedata[1]);
            $("#edit_invoiceemail").val(Responsedata[2]);
            $("#edit_userstreet").val(Responsedata[3]);
            $("#edit_userzip").val(Responsedata[4]);
            $("#edit_userplace").val(Responsedata[5]);
            $("#edit_companyname").val(Responsedata[6]);
            $("#edit_usertax").val(Responsedata[7]);
        })
}

function filter(word) {
    let items = document.getElementsByClassName("mysearch_item");

    let length = items.length
    let collection = []
    let hidden = 0

    // console.log("DETAILS: ", items, length);

    for (let i = 0; i < length; i++) {
        if (items[i].value) {
            // console.log("VALUE: ", items[i].value, word);
            // console.log("CALCULATION: ", items[i].value.toLowerCase().startsWith(word))
            if (items[i].value.toLowerCase().startsWith(word)) {
                $(items[i]).show()
            } else {
                // console.log("HIDING: ", items[i])
                $(items[i]).hide()
                hidden++
            }
        }
    }

    //If all items are hidden, show the empty view
    if (hidden === length) {
        $('.empty').show()
    } else {
        $('.empty').hide()
    }
}

function filter_cus(word) {
    let items = document.getElementsByClassName("mysearch_item2");

    let length = items.length
    let collection = []
    let hidden = 0

    // console.log("DETAILS: ", items, length);

    for (let i = 0; i < length; i++) {
        if (items[i].value) {
            // console.log("VALUE: ", items[i].value, word);
            // console.log("CALCULATION: ", items[i].value.toLowerCase().startsWith(word))
            if (items[i].value.toLowerCase().startsWith(word)) {
                $(items[i]).show()
            } else {
                // console.log("HIDING: ", items[i])
                $(items[i]).hide()
                hidden++
            }
        }
    }

    //If all items are hidden, show the empty view
    if (hidden === length) {
        $('.empty1').show()
    } else {
        $('.empty1').hide()
    }
}

show_overlay();

fetch('/get_destinations/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': ['destinations_sorted'] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log(Responsedata);

        values = JSON.parse(Responsedata)

        let contents = []
        for (let name of values) {
            contents.push('<input type="button" class="dropdown-item mysearch_item" type="button" value="' + name + '"/>')
        }
        $('#menuItems').append(contents.join(""))
        $('#menuItems1').append(contents.join(""))

        //Hide the row that shows no items were found
        $('.empty').hide()
        $('.empty1').hide()

        let searchFields = document.querySelectorAll(".des_drop");

        let searchFields2 = document.querySelectorAll(".cus_drop");

        searchFields.forEach(function(search) {
            search.addEventListener('input', function() {
                if (search.value) {
                    // console.log("VALUE", search.value); 
                    filter(search.value.trim().toLowerCase());
                }
            });
        });


        searchFields2.forEach(function(search2) {
            search2.addEventListener('input', function() {
                if (search2.value) {
                    // console.log("VALUE", search.value); 
                    filter_cus(search2.value.trim().toLowerCase());
                }
            });
        });

        // for (let i = 0; i < values.length; i++) {
        //     user_data = values[i]

        //     $('#records_table').find('tbody').append(`<tr><td> ${user_data[0]}</td> <td> ${user_data[3] }</td> <td> ${user_data[4] }</td> <td> ${user_data[5] }</td> <td> ${user_data[6] }</td> <td> ${user_data[7] }</td> <td> ${formatTime(user_data[8])}</td> </tr>`);

        // }

        $('#total').text(`${values.length}`);

        // console.log("LENGTH:", values.length())

        hide_overlay();
    });


$('.des_menu').on('click', '.mysearch_item', function() {
    // console.log("CLICKED", $(this)[0].value);
    $('.drop_btn').text($(this)[0].value)
    $(".drop_btn").dropdown('toggle');
})

$('.agr_des_menu').on('click', '.agr_search_item', function() {
    // console.log("CLICKED", $(this)[0].value);
    $('.agr_drop_btn').text($(this)[0].value)
    $(".agr_drop_btn").dropdown('toggle');

    selected_agent = $(this)[0].id;
})

$('.agrm_des_menu').on('click', '.agrm_search_item', function() {
    // console.log("CLICKED", $(this)[0].value);
    $('.agrm_drop_btn').text($(this)[0].value)
    $(".agrm_drop_btn").dropdown('toggle');

    selected_agent_room = $(this)[0].id;
})

$('.cus_menu').on('click', '.mysearch_item', function() {
    // console.log("CLICKED", $(this)[0].value);
    $('.drop_btn1').text($(this)[0].value)
    $(".drop_btn1").dropdown('toggle');
})

$('.empty').hide()
$('.empty1').hide()

$('#search_agent').on('click', function() {

    if (selected_agent === "none") {
        alert("Agent not selected");
        console.log("AGENT IS NULL");
        return;
    } 

    post_data = ['agent_active_mins', selected_agent.replace("+49", ""), 
        selected_agent_room, $("#agent_records_startdate").val(), 
        $("#agent_records_enddate").val()];

    // console.log("POST DATA: ", post_data);

    fetch('/search_agent/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': post_data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            console.log("AGENT RESPONSE: ", Responsedata, selected_agent, selected_agent_room);

            // new_agent_number = selected_agent.replace("+", "");

            var agent_name = $("#agents_dropdown").text().trim()

            if (selected_agent_room == "all") {
                sel_room = "All Rooms"
            } else {
                sel_room = $(`#${selected_agent_room}`).val()
            }

            // R_data = JSON.parse(Responsedata)
            
            $('#agent_records_table').find('tbody').empty();

            $('#agent_records_table').find('tbody').append(`<tr> 
                <td> ${agent_name }</td> 
                <td> ${sel_room }</td>
                <td> Conference </td>
                <td> ${(parseFloat(Responsedata[0]) - parseFloat(Responsedata[1])).toFixed(2).toString().replace(".", ",")} sec</td>
                <td> ${(Responsedata[1]).toFixed(2).toString().replace(".", ",")} sec</td>
                </tr>`);
            
        })
});

$('#assign_destination').on('click', function() {

    data = [$('#selected_customer').html(),
        $('#selected_destination').html(),
        $('#destination_name').val().replace(/\s+/g, '_')
    ];

    fetch('/assign_diss/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            // console.log(Responsedata);

            window.location.href = "";
        })
});

function get_agent(ai) {
    $("#agent_og").val(ai);
    $('#edit_agent').modal('show');

    fetch('/get_agent/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'agent_data': [$("#agent_og").val()] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        $("#estreet").val(Responsedata[0]);
        $("#ezip").val(Responsedata[1]);
        $("#ecity").val(Responsedata[2]);
        $("#eeamil").val(Responsedata[3]);
        $("#etaxnum").val(Responsedata[4]);
        $("#esalestax").val(Responsedata[5]);
        $("#eaccountnum").val(Responsedata[6]);
        $("#ebankname").val(Responsedata[7]);
        $("#eiban").val(Responsedata[8]);
        $("#ebic").val(Responsedata[9]);
        $("#ephone").val(Responsedata[10]);
        $("#ename").val(Responsedata[11]);
        $("#epin").val(Responsedata[12]);
        $("#eccode").val(Responsedata[13]);
    })
}

$('#save_agent').on('click', function() {

    data = [$('#aname').val(),
        $('#astreet').val(),
        $('#azip').val(),
        $('#acity').val(),
        $('#aeamil').val(),
        $('#ataxnum').val(),
        $('#asalestax').val(),
        $('#aaccountnum').val(),
        $('#abankname').val(),
        $('#aiban').val(),
        $('#abic').val(),
        $('#aphone').val(),
        $('#apin').val(),
        $('#accode').val(),
    ];

    fetch('/create_agent/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'agent_data': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            // console.log(Responsedata);

            window.location.href = "";
        })
});

$('#save_gateway').on('click', function() {

    data = [
        $('#gateway_name').val(),
        $('#gateway_start').val(),
        $('#gateway_end').val(),
    ];

    fetch('/create_gateway/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'gateway_data': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            // console.log(Responsedata);

            window.location.href = "";
        })
});

$('#editagent').on('click', function() {

    data = [
        $('#estreet').val(),
        $('#ezip').val(),
        $('#ecity').val(),
        $('#eeamil').val(),
        $('#etaxnum').val(),
        $('#esalestax').val(),
        $('#eaccountnum').val(),
        $('#ebankname').val(),
        $('#eiban').val(),
        $('#ebic').val(),
        $('#ephone').val(),
        $('#ename').val(),
        $('#agent_og').val(),
        $('#epin').val(),
        $('#eccode').val()
    ];

    fetch('/edit_agent/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'agent_data': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            // console.log(Responsedata);

            window.location.href = "";
        })
});

function del_agent(magent) {
    fetch('/delete_agent/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'agent_data': [magent] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        // console.log(Responsedata);

        window.location.href = "";
    })
}

function reduce_work(searchValue, searchResult, searchCounter, noResult) {
    $(`.${searchValue}`).keyup(function() {
        var searchTerm = $(this).val().toLowerCase();
        var listItem = $(`.${searchResult} tbody`).children('tr');
        var searchSplit = searchTerm.replace(/ /g, "'):containsi('");

        $.extend($.expr[':'], {
            'containsi': function(elem, i, match, array) {
                return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
            }
        });

        listItem.each(function() {
            var text = $(this).text().toLowerCase();
            if (text.indexOf(searchTerm) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });

        var jobCount = $(`.${searchResult} tbody tr:visible`).length;
        $(`.${searchCounter}`).text(jobCount + ' item');

        if (jobCount === 0) {
            $(`.${noResult}`).show();
        } else {
            $(`.${noResult}`).hide();
        }
    });

    $(`.${noResult}`).hide();
}

function convert_csv(my_form) {
    fetch("/convert_csv/", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'form_data': [my_form] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {
        if (Responsedata['message'] != "No Data") {
            window.location.href = `/download_csv/${Responsedata['message']}`;
        } else {
            console.log("RESPONSE:", Responsedata);
        }
    })
}


$(document).ready(function() {

    reduce_work("customer_search", "customer_results", "counter", "no-result_customer");

    reduce_work("destinations_search", "destinations_results", "destinations_counter", "destinations_noresult");

    reduce_work("orders_search", "orders_results", "orders_counter", "orders_noresult");

    reduce_work("records_search", "records_results", "records_counter", "records_noresult");

    reduce_work("agents_search", "agents_results", "agents_counter", "agents_noresult");

    reduce_work("form_search", "form_results", "form_counter", "no-result_form");

    reduce_work("gateways_search", "gateways_results", "gateways_counter", "gateways_noresult");
});