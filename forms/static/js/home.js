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

function convertSecToMin(seconds) {
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

function change_chart(chart_type) {

    if (chart_type.includes('today')) {
        console.log("Today")
    } else if (chart_type.includes('monthly')) {
        console.log("Monthly")
    } else if (chart_type.includes('yearly')) {
        console.log("Yearly")
    }
}

function fetch_des_data(des_number) {
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
            $("#tdes_min").text(convertSecToMin(Responsedata[1]).toFixed(2));
            $("#tdes_average").text(convertSecToMin(Responsedata[2]).toFixed(2));
            var total_min = parseFloat(Responsedata[1]);
            var total_cost = (parseFloat($("#call_price").val())/60) * parseFloat(total_min)
            $("#tdes_cost").text(total_cost);
        }
    })
}

// Get the element with class 'destination_cards' and 'products_card'
var destinationCards = document.querySelectorAll('.destination_cards');
var productsCard = document.querySelectorAll('.products_card');

var destinationchart = document.querySelector('.destination_chart');
var productchart = document.querySelector('.product_chart');

destinationchart.style.display = "none";
productchart.style.display = "block";

destinationCards.forEach(function (card) {
    card.style.display = 'none';
});

productsCard.forEach(function (card) {
    card.style.display = 'block';
});


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


hide_overlay();

$('.selectpicker').selectpicker();
