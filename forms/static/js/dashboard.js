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

    var selected_form = ""

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

var diss_action = '';

function sv(m) {
    diss_action=m;
}

function create_diss() {

    myname = document.getElementById("message_name").value;
    // message = document.getElementById("message").value;
    mydate = document.getElementById("date-fr").value;

    message = document.getElementsByClassName("message")[0].querySelector(".ck-editor__editable").innerHTML;

    switch (diss_action){
        case 'edit':
            var url = '/edit_diss/';
            data = [myname, message, mydate, $("#dropdown_coins").val(), $("#diss_id").val()];
            break;
        case 'new':
            var url = '/create_diss/';
            data = [myname, message, mydate, $("#dropdown_coins").val()]
            break;
        default:
            alert("Invalid Action");
    }

    // var url = '/create_diss/'

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

            // console.log("BACK!", Responsedata)

            window.location.href = "";
        })

}

function general_info() {
    var url = '/general_info/'
    
    // welcome_text = document.getElementById("welcome_text").value;
    // imp_info = document.getElementById("important_text").value;

    welcome_text = document.getElementsByClassName("welcome_text")[0].querySelector(".ck-editor__editable").innerHTML;
    imp_info = document.getElementsByClassName("important_text")[0].querySelector(".ck-editor__editable").innerHTML;

    // const ckEditorEditableDiv = welcomeTextDiv.querySelector(".ck-editor__editable");
    // const innerHTML = ckEditorEditableDiv.innerHTML;

    data = [welcome_text, imp_info, $("#dropdown_coins").val()]

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

            // console.log("BACK!", Responsedata)

            window.location.href = "";
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
    contact_destination = $('#dropdown_coins').val();

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

        window.location.href = "";
    })
}

function create_product() {
    product_name = document.getElementById("productname").value;
    product_number = document.getElementById("itemnumber").value;
    product_sp = document.getElementById("sales_price").value;
    product_pp = document.getElementById("purchase_price").value;
    product_shipping = document.getElementById("item_shipping").value;
    product_tax = document.getElementById("item_tax").value;
    product_others = document.getElementById("other_price").value;
    product_destination = $('#dropdown_coins').val();

    fetch('/create_product/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [product_name, product_number, 
            product_sp, product_pp, product_destination,
            product_tax, product_shipping, product_others] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log("PRODUCT CREATED !", Responsedata);

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

$(document).ready(function() {
    reduce_work("contacts_search", "contact_results", "contacts_counter", "contact_noresult");
    reduce_work("product_search", "product_results", "product_counter", "products_noresult");
    reduce_work("diss_search", "diss_results", "diss_counter", "diss_noresult");
    reduce_work("mforms_search", "mform_results", "mform_counter", "mform_noresult");
    reduce_work("emails_search", "emails_results", "emails_counter", "emails_noresult");
});

function assign_form() {
    product_destination = $('#dropdown_coins').val();

    fetch('/assign_form/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [selected_form, product_destination] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log(Responsedata);

        window.location.href = "";
    })
}

function createnew_email(){

    form_name = $('#selected_eform').text();
    form_username = $('#form_username').val();
    form_useremail = $('#form_useremail').val();

    console.log("DETAILS:", form_name, form_useremail, form_username)

    fetch('/add_emails/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [form_name, form_useremail, form_username] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log(Responsedata);

        window.location.href = "";
    })
}

function delete_form(form_id) {
    fetch('/delete_form/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [form_id] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log(Responsedata);

        window.location.href = "";
    })
}

function delete_this(my_email) {

    my_form = $('#selected_form').text().trim()

    if (my_form !== '' && my_form !== 'Forms') {
        fetch('/delete_email/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': [my_email, my_form] })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {
    
            console.log(Responsedata);
    
            window.location.href = "";
        })
      } else {
        alert('Not Proceeding');
    }
}

var selectedFormEdit = "";

function edit_this(username, user_emails) {

    $("#selectedform_edit").val(selectedFormEdit);
    $("#editform_user").val(username);
    $("#editform_email").val(user_emails);

    $("#edit_details").modal('show');
}

$('#EditFormDetails').on('click', function() {
    fetch('/edit_formdetails/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [
        $("#selectedform_edit").val(),
        $("#editform_user").val(),
        $("#editform_email").val()] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log(Responsedata);

        window.location.href = "";
    })
});

$('#create_diss').on('click', function() {
    create_diss();
});

$('#general_info').on('click', function() {
    general_info();
});

$('#assign_form-destination').on('click', function() {
    assign_form();
});

$('#createcontact').on('click', function() {
    create_contact();
});

$('#create_product').on('click', function() {
    create_product();
});

$('#createnew_email').on('click', function() {
    createnew_email();
});

var select = document.getElementById("destination-select");

select.addEventListener("change", function() {
var selectedOption = select.options[select.selectedIndex];
// var url = selectedOption.value === "Pend" ? "https://example.com/products" : "";

if (selectedOption.value != "EMPTY" && selectedOption.value != "null" && selectedOption.value != null ) {
    window.location.href = `/dashboard/${selectedOption.value}`;
}

});

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


let searchFields = document.querySelectorAll(".des_drop");


searchFields.forEach(function(search) {
    search.addEventListener('input', function () {
        if (search.value) { 
            // console.log("VALUE", search.value); 
            filter(search.value.trim().toLowerCase());
        }
    });
});

function fetch_info(my_des) {
    fetch('/diss_info/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [my_des] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        if (Responsedata[0] == "NO RECORD") {
            console.log("NO RECORD");
        } else {
            $("#diss_name").val(Responsedata[0]);
            $("#diss_datetime").val(Responsedata[1]);
            $("#diss_message").val(Responsedata[2]);
            $("#diss_id").val(Responsedata[3]);
        }
    })
}

function change_productstatus(product_id) {

    console.log("INSIDE THE FUNCTION");

    fetch('/change_pstatus/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': product_id })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        // console.log(Responsedata)

        window.location.href = '';
    })
}


function fetch_emails(my_fname) {

    selectedFormEdit = my_fname;

    fetch('/send_emails/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [my_fname] })
    })
    .then((resp) => resp.json())
    .then(function(data) {

        console.log("FORM DATA: ", data)

        const tbody = document.querySelector('#form_emails tbody');

        // Clear existing table rows
        tbody.innerHTML = '';

        // Iterate over object key-value pairs
        for (const [name, email] of Object.entries(data)) {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        const emailCell = document.createElement('td');
        const delCell = document.createElement('td');
        const edtCell = document.createElement('td');
        
        nameCell.textContent = name;
        emailCell.textContent = email;
        delCell.innerHTML = `<a id='${email}' onClick="delete_this(this.id)">Delete</a>`;
        edtCell.innerHTML = `<a onClick="edit_this('${name}', '${email}')">Edit</a>`;
        
        row.appendChild(nameCell);
        row.appendChild(emailCell);
        row.appendChild(delCell);
        row.appendChild(edtCell);
        
        tbody.appendChild(row);
        }

        // Show "No result" message if the data object is empty
        if (Object.keys(data).length === 0) {
        const noResultRow = document.createElement('tr');
        const noResultCell = document.createElement('td');
        
        noResultCell.setAttribute('colspan', '2');
        noResultCell.innerHTML = '<i class="fa fa-warning"></i> No result';
        
        noResultRow.appendChild(noResultCell);
        tbody.appendChild(noResultRow);
        }
    })
}

$('.des_menu').on('click', '.mysearch_item', function(){
    // console.log("CLICKED", $(this)[0].value);
    $('.drop_btn').text($(this)[0].value)
    $(".drop_btn").dropdown('toggle');

    fetch_info($(this)[0].value);
})

$('#diss_del').on('click', function(){

    if ($('#diss_id').val() == 'none') {
        alert("No Message Selected");
    } else {
        fetch('/delete_diss/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': [$('#diss_id').val()] })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {
    
            window.location.href = '';
        })
    }
})

$('.des_menu').on('click', '.mysearch_item', function(){
    // console.log("CLICKED", $(this)[0].value);
    $('.drop_btn').text($(this)[0].value)
    $(".drop_btn").dropdown('toggle');

    fetch_info($(this)[0].value);
})

$('.emails_fetch').on('click', '.mysearch_item', function(){
    // console.log("CLICKED", $(this)[0].value);
    $('.edrop_btn').text($(this)[0].value)
    $(".edrop_btn").dropdown('toggle');

    fetch_emails($(this)[0].value);
})

$('.emails_set').on('click', '.mysearch_item', function(){
    // console.log("CLICKED", $(this)[0].value);
    $('.eset_btn').text($(this)[0].value)
    $(".eset_btn").dropdown('toggle');
})

$('.empty').hide()

option_select = document.getElementById('destination-select').options;

if (option_select.length >= 2 ) {
    console.log("VALUES: ", option_select[0].value, option_select[1].value)
    if (option_select[1].value != "null" && option_select[0].value === "null" && option_select[1].value != "none") {
        window.location.href = `/dashboard/${option_select[1].value}`;
    }
}

function initializeCKEditorForTextarea(textareaId) {
    const editorConfigs = {
      toolbar: {
        items: [
          'heading',
          '|',
          'bold',
          'italic',
          'link',
          'bulletedList',
          'numberedList',
          '|',
          'alignment',
          'undo',
          'redo'
        ]
      }
    };

    ClassicEditor
      .create(document.getElementById(textareaId), editorConfigs)
      .then(editor => {
        // CKEditor is initialized for the specific textarea with ID 'textareaId'.
        // You can perform any additional logic here if needed.
        console.log(`CKEditor initialized for textarea with ID: ${textareaId}`);
      })
      .catch(error => {
        console.error(`Error initializing CKEditor for textarea with ID '${textareaId}':`, error);
      });
  }

  document.addEventListener("DOMContentLoaded", function() {
    // Call the function for each textarea with a specific ID
    initializeCKEditorForTextarea('welcome_text');
    initializeCKEditorForTextarea('important_text');
    initializeCKEditorForTextarea('message');

  });

  document.addEventListener("DOMContentLoaded", function() {

    const ckEditorDivs = document.querySelectorAll('.ck-editor__main');
    // const ckEditorDivs = document.querySelectorAll('.ck-editor__editable');

    console.log("EDITORS: ", ckEditorDivs)

    // Create CKEditor instances for each ck-editor__editable div
    ckEditorDivs.forEach((editorDiv) => {
        const formGroupDiv = editorDiv.closest('.form-group');
        const textarea = formGroupDiv.querySelector('textarea');
        const textareaId = textarea.getAttribute('id');
        console.log(editorDiv, textarea, textareaId)

        // Add textareaId as a class to the ckEditorDiv
        editorDiv.classList.add(textareaId);

    });
  });


hide_overlay();
