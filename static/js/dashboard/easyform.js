var currentStep = 1;
var updateProgressBar;

function displayStep(stepNumber) {
  if (stepNumber >= 1 && stepNumber <= 5) {
    $(".step-" + currentStep).hide();
    $(".step-" + stepNumber).show();
    currentStep = stepNumber;
    updateProgressBar();
  }
}

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

function get_destinations(my_value) {

  if (my_value != 'select_gateway') {

    start = my_value.split('.')[0];
    end = my_value.split('.')[1];

    fetch('/get_numbers/', {
      method: 'POST',
      headers: {
          'Content-type': 'application/json',
          'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ 'details': ['available_destinations', start, end] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {
  
        values = JSON.parse(Responsedata)
  
        let contents = []
        for (let name of values) {
            contents.push('<input type="button" class="dropdown-item mysearch_item" type="button" value="' + name + '"/>')
        }

        $('#menuItems').append(contents.join(""))

        let searchFields = document.querySelectorAll(".des_drop");

        searchFields.forEach(function(search) {
          search.addEventListener('input', function() {
            filter(search.value.trim().toLowerCase());
              
          });
        });

        $('.mysearch_item').click(function() {
          var selectedText = $(this).val();
    
          updateButtonText(selectedText);
        });
    });
    
  }
}

function filter(word) {
  let items = document.getElementsByClassName("mysearch_item");
  let length = items.length;
  let hidden = 0;

  if (word.length === 0) {
      // If the length of the word is 0, show all items
      Array.from(items).forEach(function(item) {
          $(item).show();
      });
      $('.empty').hide();
  } else {
      // If the length of the word is not 0, filter items based on the word
      Array.from(items).forEach(function(item) {
          if (item.value.toLowerCase().startsWith(word.toLowerCase())) {
              $(item).show();
          } else {
              $(item).hide();
              hidden++;
          }
      });

      if (hidden === length) {
          $('.empty').show();
      } else {
          $('.empty').hide();
      }
  }
}

function nextstep() {

  if (currentStep < 5) {
    $(".step-" + currentStep).addClass("animate__animated animate__fadeOutLeft");
    currentStep++;
    setTimeout(function() {
      $(".step").removeClass("animate__animated animate__fadeOutLeft").hide();
      $(".step-" + currentStep).show().addClass("animate__animated animate__fadeInRight");
      updateProgressBar();
    }, 500);
  }
}

function music_options() {
  fetch('/get_mohsounds/', {
    method: 'POST',
    headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': getCookie("csrftoken"),
    },
    body: JSON.stringify({ 'details': "" })
  })
  .then((resp) => resp.json())
  .then(function(Responsedata) {

    var selectElement = document.getElementById('selected_moh');

    Responsedata.forEach(function(option) {
        // Create a new option element
        var newOption = document.createElement('option');

        // Set the value and text of the option
        newOption.value = option.option_value;
        newOption.text = option.option_text;

        // Append the option to the select element
        selectElement.appendChild(newOption);
    });

  })
}

function get_destination_data() {
  fetch('/get_destination_data/', {
    method: 'POST',
    headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': getCookie("csrftoken"),
    },
    body: JSON.stringify({ 'details': "" })
  })
  .then((resp) => resp.json())
  .then(function(Responsedata) {

    var des_action = document.getElementById('selected_action');
    var des_domain = document.getElementById('selected_domain');

    Responsedata.domains.forEach(function(domain) {
      var option = document.createElement('option');
      option.value = domain.option_value;
      option.textContent = domain.option_text;
      des_domain.appendChild(option);
    });

    // Add destination options
    Responsedata.destination_options.forEach(function(option) {
      var optgroupLabel;
      if (option.optgroup_label === "Call Center") {
          optgroupLabel = "Queues";
      } else {
          optgroupLabel = option.optgroup_label;
      }
      
      var optgroup = des_action.querySelector('optgroup[label="' + optgroupLabel + '"]');
      if (!optgroup) {
          optgroup = document.createElement('optgroup');
          optgroup.label = optgroupLabel;
          des_action.appendChild(optgroup);
      }
      
      var optionElem = document.createElement('option');
      optionElem.value = option.option_value;
      optionElem.textContent = option.option_text;
      optgroup.appendChild(optionElem);
    });

  })
}

$("#upload_music").click(function(event) {
  event.preventDefault();
  
  show_overlay();

  var formData = new FormData(document.getElementById('upload_music_form'));

  fetch('/upload_music/', {
      method: 'POST',
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      body: formData,
  })
  .then(response => response.json())
  .then(data => {
    hide_overlay();
    console.log("RESPONSE: ", data);
      if (data.status == 'success') {
          nextstep();
      } else {
          console.error('File upload failed:', data.error);
      }
  })
  .catch(error => {
      hide_overlay();
      console.error('Error submitting form:', error);
  });

});

function updateButtonText(text) {
  
  document.getElementById('dropdown_coins').textContent = text;
  $('#destinationnumber').val(text);
}

  $(document).ready(function() {
    $('#multi-step-form').find('.step').slice(1).hide();
  
    $(".next-step").click(function() {
      nextstep();
    });

    music_options();
    get_destination_data();

    $(".prev-step").click(function() {
      if (currentStep > 1) {
        $(".step-" + currentStep).addClass("animate__animated animate__fadeOutRight");
        currentStep--;
        setTimeout(function() {
          $(".step").removeClass("animate__animated animate__fadeOutRight").hide();
          $(".step-" + currentStep).show().addClass("animate__animated animate__fadeInLeft");
          updateProgressBar();
        }, 500);
      }
    });

    updateProgressBar = function() {
      var progressPercentage = ((currentStep - 1) / 4) * 100;
      $(".progress-bar").css("width", progressPercentage + "%");
    }

    function displayErrorMessage(errorMessage) {
      var errorDiv = $('#error-message');
      errorDiv.empty(); // Clear any previous error messages
      errorDiv.show(); // Show the error message div
  
      var displayedErrors = {}; // Object to track displayed errors
  
      // Iterate over each error and append it to the error message div if it's not already displayed
      $.each(errorMessage.errors, function(field, errors) {
          $.each(errors, function(index, error) {
              if (!displayedErrors.hasOwnProperty(error)) {
                  errorDiv.append('<p>' + error + '</p>');
                  displayedErrors[error] = true; // Mark error as displayed
              }
          });
      });
  }

    // Create Client

    $("#create_client").click(function(e) {
      e.preventDefault(); // Prevent default form submission
      show_overlay();
      
      // Serialize form data
      var formData = $("#client_form").serialize();

      $.ajax({
        type: 'POST',
        url: '/create_client/',
        data: formData,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function(response) {
            hide_overlay();
            nextstep();
        },
        error: function(xhr, textStatus, errorThrown) {
            hide_overlay();

            // Handle error response here
            var errorMessage = JSON.parse(xhr.responseText);
            displayErrorMessage(errorMessage);
        }
      });
    });

    // Create Queue

    document.getElementById('createqueue').addEventListener('click', function(event) {
      // Prevent the default form submission behavior
      event.preventDefault();

      show_overlay();

      // Get form data
      var formData = new FormData(document.getElementById('create_queue'));

      // Make a POST request to your Django view
      fetch('/create_queue/', {
          method: 'POST',
          body: formData,
          headers: { "X-CSRFToken": getCookie("csrftoken") },
      })
      .then(response => {
          hide_overlay();
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          // Handle the response from the Django view
          console.log("QUEUE Response", data);

          if (data['message'].includes("successfully")) {
            hide_overlay();
            nextstep();
          }
      })
      .catch(error => {
          hide_overlay();
          console.error('There was an error with the fetch request:', error);
      });
    });

    document.getElementById('skip_last').addEventListener('click', function(event) {
      // Prevent the default form submission behavior
      event.preventDefault();

      show_overlay();

      window.location.href = "/admin_dashboard";
    });

    // Create Conference

    document.getElementById('createconf').addEventListener('click', function(event) {
      // Prevent the default form submission behavior
      event.preventDefault();

      show_overlay();

      // Get form data
      var formData = new FormData(document.getElementById('create_conf'));

      // Make a POST request to your Django view
      fetch('/create_conference/', {
          method: 'POST',
          body: formData,
          headers: { "X-CSRFToken": getCookie("csrftoken") },
      })
      .then(response => {
          hide_overlay();
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          // Handle the response from the Django view
          console.log("CONF Response", data);

          if (data['message'].includes("successfully")) {
            hide_overlay();
            nextstep();
          }
      })
      .catch(error => {
          hide_overlay();
          console.error('There was an error with the fetch request:', error);
      });
    });

    // Create Destination
    document.getElementById('createdes').addEventListener('click', function(event) {
      // Prevent the default form submission behavior
      event.preventDefault();

      show_overlay();

      // Get form data
      var formData = new FormData(document.getElementById('create_des'));

      // Make a POST request to your Django view
      fetch('/create_destination/', {
          method: 'POST',
          body: formData,
          headers: { "X-CSRFToken": getCookie("csrftoken") },
      })
      .then(response => {
          hide_overlay();
          if (!response.ok) {
              console.log(response);
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          // Handle the response from the Django view
          console.log("DESTINATION Response", data);

          if (data["message"].includes("successfully")) {
            hide_overlay();
            window.location.href = "/admin_dashboard";
          }
      })
      .catch(error => {
          hide_overlay();
          console.error('There was an error with the fetch request:', error);
      });
    });

  });