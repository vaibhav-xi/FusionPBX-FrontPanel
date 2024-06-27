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

function render_chart2(option) {

    console.log("SENDING: ", [option, `49${$("#my_des-number").val()}`]);
    
    fetch("/destination_chart/", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [option, `49${$("#my_des-number").val()}`] })
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
    })
}

function chart2_sorted(option, range) {

    fetch("/destination_chart/", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'details': [option, `49${$("#my_des-number").val()}`, range] })
    })
    .then((resp) => resp.json())
    .then(function(Responsedata) {

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
    })
}
// document.querySelector("#reportsChart").style = "";
// document.querySelector("#destinationChart").style = "";
// // Set the style property of the chart to display block
// document.querySelector("#reportsChart").style.display = "block";

if ($("#my_des-number").val().length > 2) {

    render_chart1(option);
    render_chart2("chart_datad");

    }