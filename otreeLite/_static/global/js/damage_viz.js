Highcharts.chart('container', {
    chart: {
        type: 'area'
    },
    xAxis: {
        categories: [0,10,20,30,40,50,60,70,80,90,100],
        title: {
        		text : "Share of Total Endowments Contributed"
        },
    },

    yAxis: {
        title: {
        		text : "Possible Damage"
        },
    },

    legend: {
    		enabled: false
    },

    plotOptions: {
        series: {
            fillColor: {
                linearGradient: [0, 0, 0, 300],
                stops: [
                    [0, "rgba(217, 83, 79, 0.5)"],
                    [1, "rgba(217, 83, 79, 0.05)"]
                ]
            },
            color: "#d9534f",
            marker: {
                enabled: false
            }
        }
    },

    series: [{
        name: 'Possible Damage',
        data: [50,45,40,35,30,25,20,15,10,5,0]
    }]
});