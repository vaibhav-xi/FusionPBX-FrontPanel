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
                    if (my_id != "call_price") {

                        console.log("KEYS: ", my_id);

                        var my_val = settings_data[key] ? "on" : "off";

                        $('#' + my_id).bootstrapToggle(my_val);
                    } else {
                        $('#call_price').val(settings_data[key])
                    }
                }
            }
        })
}

function generate_invoice(m) {
    var url = '/create_invoice/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': m })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {
            console.log(Responsedata);
        })
}

$('#client_details').on('click', function() {

    data = [selected,
        $("#daily_stats").prop("checked"),
        $("#weekly_stats").prop("checked"),
        $("#monthly_stats").prop("checked"),
        $("#invoice_creation").prop("checked"),
        $("#form_function").prop("checked"),
        $("#call_price").val(),
        $("#imp_sw").prop("checked"),
        $("#diss_sw").prop("checked"),
        $("#sales_sw").prop("checked")
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

    data = [$("#selected_desname").val(),
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

$('#edit_userdetails').on('click', function() {

    data = [$("#edit_username").val(),
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
        body: JSON.stringify({ 'details': ['destinations'] })
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

$('.cus_menu').on('click', '.mysearch_item', function() {
    // console.log("CLICKED", $(this)[0].value);
    $('.drop_btn1').text($(this)[0].value)
    $(".drop_btn1").dropdown('toggle');
})

$('.empty').hide()
$('.empty1').hide()


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



$(document).ready(function() {

    reduce_work("customer_search", "customer_results", "counter", "no-result_customer");

    reduce_work("destinations_search", "destinations_results", "destinations_counter", "destinations_noresult");

    reduce_work("orders_search", "orders_results", "orders_counter", "orders_noresult");

    reduce_work("records_search", "records_results", "records_counter", "records_noresult");
});