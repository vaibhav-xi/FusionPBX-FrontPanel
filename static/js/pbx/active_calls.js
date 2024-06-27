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

function active_calls(){
    fetch('/activecalls/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify('Hoi')
    })
    .then((resp) => resp.json())
    .then(response => {
        
        total_active_calls = JSON.parse(response)
        console.log(total_active_calls);

        if (total_active_calls != "No Queues") {
            for (const dict_key in total_active_calls) {
                // console.log(dict_key);
                var room = dict_key.split('@')[0];
                callers = total_active_calls[dict_key]['caller_names']
                callers.forEach(element => {
                    console.log(element);
                    const container = document.getElementById(room);
                    const myDiv = container.querySelector(`#${element}`);
    
                    if (myDiv) {
                        // pass
                    }
                    else {
                        var div = document.createElement('div');
    
                        div.classList.add('room-banner', 'noselect', 'draggable_banner');
    
                        div.setAttribute('id', `${element}`);
    
                        var dn = element;
    
                        d = document.createTextNode(`${dn}`);
    
                        div.appendChild(d);
    
                        document.getElementById(room).appendChild(div);
                    }
                });
            }
        } else {
            for (const my_container in total_container) {
                while (my_container.firstChild) {
                    if(my_container.firstChild.tagName === 'DIV'){
                        my_container.removeChild(my_container.firstChild);
                    }
                    else{
                        my_container.firstChild.remove();
                    }
                }
            }
        }
    });
}

setInterval(function(){
    active_calls();
  }, 5000);