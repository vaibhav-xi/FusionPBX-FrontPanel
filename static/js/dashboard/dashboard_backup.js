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

(function(i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] || function() {
        (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date();
    a = s.createElement(o),
        m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m)
})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-60343429-1', 'auto');
ga('send', 'pageview');

$(document).ready(function()
{

    // Get the current date and time
    var currentDate = new Date();

    // Get the individual components of the date and time
    var day = currentDate.getDate();
    var month = currentDate.getMonth() + 1; // January is 0, so we add 1
    var year = currentDate.getFullYear();
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();

    // Format the components as two digits if needed
    day = (day < 10) ? '0' + day : day;
    month = (month < 10) ? '0' + month : month;
    hours = (hours < 10) ? '0' + hours : hours;
    minutes = (minutes < 10) ? '0' + minutes : minutes;

    // Create the formatted date-time string
    var formattedDateTime = day + '/' + month + '/' + year + ' ' + hours + ':' + minutes;

    document.getElementById('date-fr').value = formattedDateTime;


    $('#date').bootstrapMaterialDatePicker
    ({
        time: false,
        clearButton: true
    });

    $('#time').bootstrapMaterialDatePicker
    ({
        date: false,
        shortTime: false,
        format: 'HH:mm'
    });

    $('#date-format').bootstrapMaterialDatePicker
    ({
        format: 'dddd DD MMMM YYYY - HH:mm'
    });
    $('#date-fr').bootstrapMaterialDatePicker
    ({
        format: 'DD/MM/YYYY HH:mm',
        lang: 'en',
        weekStart: 1, 
        cancelText : 'Cancel',
        nowButton : true,
        switchOnClick : true
    });

    $('#date-end').bootstrapMaterialDatePicker
    ({
        weekStart: 0, format: 'DD/MM/YYYY HH:mm'
    });
    $('#date-start').bootstrapMaterialDatePicker
    ({
        weekStart: 0, format: 'DD/MM/YYYY HH:mm', shortTime : true
    }).on('change', function(e, date)
    {
        $('#date-end').bootstrapMaterialDatePicker('setMinDate', date);
    });

    $('#min-date').bootstrapMaterialDatePicker({ format : 'DD/MM/YYYY HH:mm', minDate : new Date() });

    // $.material.init()
});


function create_diss() {
    var url = '/create_diss/'

    myname = document.getElementById("message_name").value;
    message = document.getElementById("message").value;
    mydate = document.getElementById("date-fr").value;

    data = [myname, message, mydate]

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': data })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            console.log("BACK!", Responsedata)
        })

}

function fetch_diss(d_name) {
    fetch('/fetch_diss/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': d_name })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        document.getElementById("diss_name").value = Responsedata[0];
        document.getElementById("diss_datetime").value = Responsedata[1];
        document.getElementById("diss_message").value = Responsedata[2];

        console.log("BACK!!!", Responsedata);
    })
}

function create_contact() {
    contact_name = document.getElementById("username").value;
    contact_email = document.getElementById("useremail").value;
    contact_number = document.getElementById("userphone").value;
    contact_destination = $('#dropdown_coins').text();

    fetch('/create_contact/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [contact_name, contact_email, contact_number, contact_destination] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log("CONTACT CREATED !", Responsedata);
    })
}

function create_product() {
    product_name = document.getElementById("productname").value;
    product_number = document.getElementById("itemnumber").value;
    product_sp = document.getElementById("sales_price").value;
    product_pp = document.getElementById("purchase_price").value;
    product_destination = $('#dropdown_coins3').text();

    fetch('/create_product/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [product_name, product_number, product_sp, product_pp, product_destination] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log("PRODUCT CREATED !", Responsedata);
    })
}


$(document).ready(function() {
    $(".search").keyup(function () {
      var searchTerm = $(".search").val();
      var listItem = $('.results tbody').children('tr');
      var searchSplit = searchTerm.replace(/ /g, "'):containsi('")
      
    $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
          return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
      }
    });
      
    $(".results tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
      $(this).attr('visible','false');
    });
  
    $(".results tbody tr:containsi('" + searchSplit + "')").each(function(e){
      $(this).attr('visible','true');
    });
  
    var jobCount = $('.results tbody tr[visible="true"]').length;
      $('.counter').text(jobCount + ' item');
  
    if(jobCount == '0') {$('.no-result').show();}
      else {$('.no-result').hide();}
            });
  });


$('#create_diss').on('click', function() {
    create_diss();
});

$('#createcontact').on('click', function() {
    create_contact();
});

$('#create_product').on('click', function() {
    create_product();
});

$(document).ready(function() {

    //Find the input search box

    let searchFields = document.querySelectorAll(".des_drop");

    searchFields.forEach(function(search) {
        search.addEventListener('input', function () {
            if (search.value) { 
                // console.log("VALUE", search.value); 
                filter(search.value.trim().toLowerCase());
            }
        });
    });
    
    //Find every item inside the dropdown
    
    // function buildDropDown(values) {
    //     let contents = []
    //     for (let name of values) {
    //     contents.push('<input type="button" class="dropdown-item mysearch_item" type="button" value="' + name + '"/>')
    //     }
    //     $('#menuItems').append(contents.join(""))

    //     //Hide the row that shows no items were found
    //     $('#empty').hide()
    // }

    //For every word entered by the user, check if the symbol starts with that word
    //If it does show the symbol, else hide it
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
                }
                else {
                    // console.log("HIDING: ", items[i])
                    $(items[i]).hide()
                    hidden++
                }
            }
        }

        //If all items are hidden, show the empty view
        if (hidden === length) {
        $('.empty').show()
        }
        else {
        $('.empty').hide()
        }
    }

    //If the user clicks on any item, set the title of the button as the text of the item

    $('.des_menu').on('click', '.mysearch_item', function(){
        // console.log("CLICKED", $(this)[0].value);
        $('.drop_btn').text($(this)[0].value)
        $(".drop_btn").dropdown('toggle');
    })


    $('.empty').hide()
})