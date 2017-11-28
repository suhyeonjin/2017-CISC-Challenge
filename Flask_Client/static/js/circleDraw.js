var chart2;

function requestData2() {
    $.ajax({
        url: '/live-count',
        success: function(point) {
            chart2.series[0].setData(point, true);
            setTimeout(requestData2, 5000);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart2 = new Highcharts.chart({
        chart: {
            renderTo: 'container',
            defaultSeriesType: 'pie',
            events: {
                load: requestData2
            }
        },
        title: {
            text: 'packet percentage about Normal, Fuzzy, Dos'
        },

        plotOptions: {
            pie: {
                size: 300
            }
        },

    series: [{
        data: [
            //init value sample
            ['Normal',   44.2],
            ['Dos',       26.6],
            ['Fuzzy',       20],
        ]
    }]
});
});
