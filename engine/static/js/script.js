var $ = jQuery.noConflict();

$(document).ready(function () {
    $("#form-link").submit(function (event) {
        event.preventDefault();

        $.ajax({
            url: tokens.ajax_short_url,
            type: 'POST',
            data: {
                link: $('#original-link').val(),
                csrfmiddlewaretoken: tokens.csrf_token,
            },
            success: function (data) {
                window.prompt("Copy to clipboard: Ctrl+C, Enter", data);
            },
            statusCode: {
                400: function() {
                  alert( "Please, input correct url (ex: https://google.com)" );
                }
            },
        });
    });

    if (document.getElementById("click_statistics")) {
        console.log(1);
        var data = tokens.graph_data;
        var labels_data = [];
        var clicks_data = [];

        for (var i in data) {
            labels_data.push(i);
            clicks_data.push(data[i]);
        }

        var ctx = document.getElementById("click_statistics").getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels_data,
                datasets: [{
                    label: 'Clicks per day',
                    data: clicks_data,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }
});