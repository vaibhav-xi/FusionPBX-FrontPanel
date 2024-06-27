var select = document.getElementById("destination-select");

select.addEventListener("change", function() {
    var selectedOption = select.options[select.selectedIndex];
    // var url = selectedOption.value === "Pend" ? "https://example.com/products" : "";
    
    if (selectedOption.value != "EMPTY" && selectedOption.value != "null" && selectedOption.value != null ) {
        window.location.href = `/home/${selectedOption.value}`;
    }

});

show_overlay();


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
      }
  })
}

$('.des_menu').on('click', '.mysearch_item', function(){
  // console.log("CLICKED", $(this)[0].value);
  $('.drop_btn').text($(this)[0].value)
  $(".drop_btn").dropdown('toggle');

  fetch_info($(this)[0].value);
})

$('.empty').hide()

// Modiified Block

// option_select = document.getElementById('destination-select').options;

// if (option_select.length >= 2 ) {
//     console.log("VALUES: ", option_select[0].value, option_select[1].value)

//     if (option_select[1].value === "null" && option_select[0].value != null) {
//         window.location.href = `/home/${option_select[1].value}`;
//     }
// }

///////////////////////////////////////////////////

function convertSecToMin_og(seconds) {
    // Convert the input to an integer if it's a string
    const secondsInt = parseInt(seconds, 10);
  
    // Check if the conversion was successful and if the value is a number
    if (!isNaN(secondsInt) && typeof secondsInt === "number") {
      return secondsInt / 60;
    } else {
      // Return null or handle the invalid input as per your requirement
      return null;
    }
  }

function convertSecToMin(seconds) {

    if (seconds == null){
        return 0;
    }
    // Convert the input to an integer if it's a string
    const secondsInt = parseInt(seconds, 10);

    // Check if the conversion was successful and if the value is a number
    if (!isNaN(secondsInt) && typeof secondsInt === "number") {
        const minutes = Math.floor(secondsInt / 60);
        const remainingSeconds = secondsInt % 60;
        
        // Format the result as "Min:Sec"
        return `${minutes}:${remainingSeconds}`;
        // return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    } else {
        // Return null or handle the invalid input as per your requirement
        return null;
    }
}

function change_chart(chart_type) {

    console.log("SELECTED: ", chart_type);

    show_overlay();

    if (chart_type.toLowerCase().includes('today')) {
        getCurrentMonthDates("today");
    } else if (chart_type.toLowerCase().includes('month')) {
        getCurrentMonthDates("month");
    } else if (chart_type.toLowerCase().includes('year')) {
        getCurrentMonthDates("year");
    } else if (chart_type.toLowerCase().includes('custom')){
        $('#custom_range').modal('show');
        hide_overlay();
    }
    else {
        hide_overlay();
        console.log("INCORRECT VALUE");
    }
}

$('#gen_stats').on('click', function() {
    show_overlay();
    chart_sorted($("#stats_startdate").val(), $("#stats_enddate").val());
    $('#custom_range').modal('hide');
});

function fetch_des_data(des_number) {

    if (des_number != "all_destinations") {
        fetch('/destination_data/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': `49${des_number}` })
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            Responsedata = JSON.parse(Responsedata)

            // console.log("RESPONSE DATA: ", Responsedata, typeof Responsedata);
    
            if (Responsedata[0] == "NO RECORD") {
                console.log("NO RECORD");
            } else {
                console.log("DATA RECEIVED: ", Responsedata);
                $("#tdes_calls").text(Responsedata[0])
                $("#tdes_min").text(convertSecToMin(Responsedata[1]));
                $("#tdes_average").text(convertSecToMin(Responsedata[2]));
                var total_min = parseFloat(Responsedata[1]);
                var total_cost = (parseFloat($("#call_price").val())/60) * parseFloat(total_min)
                var formatted_cost = `${total_cost.toFixed(2).replace('.', ',')} €`;
                $("#tdes_cost").text(formatted_cost);
            }
        })
    }
}

function g_std(number) {
    try {
        // Convert the number to a string for processing
        let numberStr = String(number);

        // Replace commas with an empty string for removing thousands separators
        numberStr = numberStr.replace(/,/g, '.');

        // Replace periods with commas for decimal point conversion
        numberStr = numberStr.replace(/\./g, ',');

        // Replace the last comma with a period for decimal point conversion
        // let parts = numberStr.split(',');
        // if (parts.length > 1) {
        //     parts[parts.length - 1] = parts[parts.length - 1].replace(/,/g, '.');
        // }
        // numberStr = parts.join('.');

        return numberStr;
    } catch (error) {
        console.error("Error: " + error.message);
        return null;
    }
}

function des_sorted(startdate, enddate) {

    if ($("#my_des-number").val() != "all_destinations") {
        fetch('/destination_sorted/', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'details': `49${$("#my_des-number").val()}`,
            "start": startdate, "end": enddate})
        })
        .then((resp) => resp.json())
        .then(function(Responsedata) {

            Responsedata = JSON.parse(Responsedata)

            // console.log("RESPONSE DATA: ", Responsedata, typeof Responsedata);
    
            if (Responsedata[0] == "NO RECORD") {
                console.log(Responsedata[0]);
            } else {
                console.log("DATA RECEIVED: ", Responsedata);
                $("#tdes_calls").text(Responsedata[0])
                $("#tdes_min").text(convertSecToMin(Responsedata[1]));
                $("#tdes_average").text(convertSecToMin(Responsedata[2]));
                var total_min = parseFloat(Responsedata[1]);
                var total_cost = (parseFloat($("#call_price").val().replace(".", "").replace(",", "."))/60) * parseFloat(total_min);
                console.log("TOTAL: ", total_cost);
                var formatted_cost = `${g_std(total_cost.toFixed(2))} €`;
                $("#tdes_cost").text(formatted_cost);
            }
        })
    }
}

// Get the element with class 'destination_cards' and 'products_card'
var destinationCards = document.querySelectorAll('.destination_cards');
var productsCard = document.querySelectorAll('.products_card');

var destinationchart = document.querySelector('.destination_chart');
var productchart = document.querySelector('.product_chart');

destinationchart.style.display = "block";

destinationCards.forEach(function (card) {
    card.style.display = 'block';
});

productsCard.forEach(function (card) {
    card.style.display = 'none';
});

productchart.style.display = "none";

// fetch_des_data($("#my_des-number").val());

// Function to switch the display property
function switchDisplay() {
    fetch_des_data($("#my_des-number").val());

    destinationCards.forEach(function (card) {
        if (card.style.display === 'none') {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });

    productsCard.forEach(function (card) {
        if (card.style.display === 'none') {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });

    if (destinationchart.style.display == 'none') {
        destinationchart.style.display = "block"
        productchart.style.display = "none";

        if (des_chart) {
            des_chart.destroy();
        }

        render_chart2("chart_datad");

        if (chart) {
            chart.destroy();
        }

    } else {
        destinationchart.style.display = "none"
        productchart.style.display = "block";

        if (chart) {
            chart.destroy();
        }

        render_chart1("90_days");

        if (des_chart) {
            des_chart.destroy();
        }
    }
}

option_select = document.getElementById('destination-select').options;

if (option_select.length >= 2 ) {
    console.log("VALUES: ", option_select[0].value, option_select[1].value)
    if (option_select[1].value != "null" && option_select[0].value === "null" && option_select[1].value != "none") {
        window.location.href = `/home/all_destinations`;
    }
}


hide_overlay();

$('.selectpicker').selectpicker();
