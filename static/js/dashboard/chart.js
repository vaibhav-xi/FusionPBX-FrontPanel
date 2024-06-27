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

var csrftoken = getCookie('csrftoken');
var chart;
var des_chart;
var selected = document.getElementById("selected_filter").innerHTML;

if (selected.includes("Month")) {
    var option = "monthly"
} else if (selected.includes("Year")) {
    var option = "yearly"
} else if (selected.includes("Today")) {
    var option = "today"
} else {
    var option = "90_days"
}

function render_chart1(option) {
    fetch("/chart_data/", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [option, $("#destination-select").val()] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log(Responsedata)

        options = {
            series: [{
                name: 'Profit',
                data: Responsedata[0],
            }],
            chart: {
                height: 350,
                type: 'area',
                toolbar: {
                    show: false
                },
            },
            markers: {
                size: 4
            },
            colors: ['#4154f1'],
            fill: {
                type: "gradient",
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.3,
                    opacityTo: 0.4,
                    stops: [0, 90, 100]
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth',
                width: 2
            },
            xaxis: {
                type: 'datetime',
                categories: Responsedata[1]
            },
            tooltip: {
                x: {
                    format: 'dd/MM/yy HH:mm'
                },
            }
        }

        // var existingChart = ApexCharts.getChartById('reportsChart');
        // if (existingChart) {
        //     existingChart.destroy();
        // }

        chart = new ApexCharts(document.querySelector("#reportsChart"), options)

        chart.render();
    })
}

function getCurrentMonthDates(selected_date) {
    var currentDate = new Date();

    // Set the date to the first day of the current month
    var startMonthDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);

    // Set the date to the last day of the current month
    var endMonthDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);

    // Format the month dates as "DD/MM/YYYY"
    var startMonthDateString = formatDate(startMonthDate);
    var endMonthDateString = formatDate(endMonthDate);

    // Set the date to the first day of the current year
    var startYearDate = new Date(currentDate.getFullYear(), 0, 1);

    // Set the date to the last day of the current year
    var endYearDate = new Date(currentDate.getFullYear(), 11, 31);

    // Format the year dates as "DD/MM/YYYY"
    var startYearDateString = formatDate(startYearDate);
    var endYearDateString = formatDate(endYearDate);

    // Format Today's Date
    var todays_date = formatDate(currentDate);

    console.log("SELECTED DATE: ", selected_date);

    if (selected_date == "month") {
        des_sorted(startMonthDateString, endMonthDateString)
        chart_sorted(startMonthDateString,endMonthDateString)
    } else if (selected_date == "year") {
        des_sorted(startYearDateString, endYearDateString)
        chart_sorted(startYearDateString,endYearDateString)
    } else if (selected_date == "today") {
        des_sorted(todays_date, todays_date)
        chart_sorted(todays_date, todays_date)
    }

}

function formatDate(date) {
    var day = date.getDate();
    var month = date.getMonth() + 1; // Months are zero-based
    var year = date.getFullYear();

    // Ensure two digits for day and month
    day = day < 10 ? '0' + day : day;
    month = month < 10 ? '0' + month : month;

    return month + '/' + day + '/' + year;
}

function render_chart2() {

    if ($("#my_des-number").val() == 'all_destinations') {
        sending_data = ["all_destinations", [myDestinations]]
    } else {
        sending_data = ["chart_datad", `49${$("#my_des-number").val()}`]
    }

    console.log("SENDING: ", sending_data);
    
    fetch("/destination_chart/", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': sending_data })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log("DATA: ", Responsedata)

        Responsedata = JSON.parse(Responsedata)

        console.log("CHART 2: ", Responsedata, typeof Responsedata)

        options = {
            series: [{
                name: 'Calls',
                data: Responsedata[1],
            }],
            chart: {
                height: 350,
                type: 'area',
                toolbar: {
                    show: false
                },
            },
            markers: {
                size: 4
            },
            colors: ['#4154f1'],
            fill: {
                type: "gradient",
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.3,
                    opacityTo: 0.4,
                    stops: [0, 90, 100]
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth',
                width: 2
            },
            xaxis: {
                type: 'date',
                categories: Responsedata[0]
            },
            tooltip: {
                x: {
                    format: 'yy/MM/dd'
                },
            }
        }

        // var existingChart = ApexCharts.getChartById('reportsChart');
        // if (existingChart) {
        //     existingChart.destroy();
        // }

        des_chart = new ApexCharts(document.querySelector("#destinationChart"), options)

        des_chart.render();

        hide_overlay();
    })
}

function chart_sorted(start_date, end_date) {

    if ($("#my_des-number").val() == 'all_destinations') {
        sending_data = ["all_sorted", [myDestinations], start_date, end_date]
    } else {
        sending_data = ["chart_sorted", `49${$("#my_des-number").val()}`, start_date, end_date]
    }

    console.log("SENDING: ", sending_data);
    
    fetch("/destination_chart/", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': sending_data })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

        console.log("DATA: ", Responsedata)

        Responsedata = JSON.parse(Responsedata)

        console.log("CHART 2: ", Responsedata, typeof Responsedata)

        options = {
            series: [{
                name: 'Calls',
                data: Responsedata[1],
            }],
            chart: {
                height: 350,
                type: 'area',
                toolbar: {
                    show: false
                },
            },
            markers: {
                size: 4
            },
            colors: ['#4154f1'],
            fill: {
                type: "gradient",
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.3,
                    opacityTo: 0.4,
                    stops: [0, 90, 100]
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth',
                width: 2
            },
            xaxis: {
                type: 'date',
                categories: Responsedata[0]
            },
            tooltip: {
                x: {
                    format: 'yy/MM/dd'
                },
            }
        }

        // var existingChart = ApexCharts.getChartById('reportsChart');
        // if (existingChart) {
        //     existingChart.destroy();
        // }

        if (des_chart){
            des_chart.destroy()
        }

        des_chart = new ApexCharts(document.querySelector("#destinationChart"), options)

        des_chart.render();

        hide_overlay();
    })
}

// document.querySelector("#reportsChart").style = "";
// document.querySelector("#destinationChart").style = "";
// // Set the style property of the chart to display block
// document.querySelector("#reportsChart").style.display = "block";

if ($("#my_des-number").val().length > 2) {

    // render_chart1(option);
    render_chart2();

    }