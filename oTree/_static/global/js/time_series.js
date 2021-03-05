// define seq() function as in R
	function* seq( start, end, step = 1 ){
	  if( end === undefined ) [end, start] = [start, 0];
	  for( let n = start; n <= end; n += step ) yield n;
	}

// initiate vars from python
	let flat_fee = js_vars.flat_fee || 0;
	let exchange_rate = js_vars.exchange_rate;
	// let template = js_vars.template; declared in basics
	// let current_round  = js_vars.current_round;
	let num_rounds  = js_vars.num_rounds;
	//let endowments = js_vars.endowments;
	let stock = js_vars.stock || 0;
	let euros = js_vars.euros || 0;

	var plot_height = 4;

// create dummy data for instructions
    if (template == "instructions"){
        current_round = 4;
        endowments = [20, 21, 27, 35]
    }

// get categories, i.e. the rounds
	var category = Array.from(seq(1, current_round));

	for(var i=0;i<category.length;i++){
		category[i]="Runde #"+category[i];
	}

// create participation fee series
	var flat = Array(current_round).fill(flat_fee)


// determine which series to be displayed
	var series = endowments;
	var suffix = " Punkte";
	var plot_line_width = 1;
	var show_in_legend = false;
	var max = num_rounds;

	if (template == "results"){
	    series = stock;
		plot_line_width = 1;
		plot_height = 4;
		max = num_rounds - 1;
	}

	if (template == "final"){
		series = euros;
		suffix = " Euro";
		plot_line_width = 0;
		show_in_legend = true;
		plot_height = 6;
		max = num_rounds - 1;
	}

	// console.log(current_round);
	// console.log(endowments);
	// console.log(category);


var chart = Highcharts.chart('container', {
    chart: {
        type: "areaspline",
        backgroundColor: "transparent",
        height: (plot_height / 16 * 100) + '%' // 16:9 ratio
    },
    title: {
        text: ""
    },
    exporting: {
				enabled: false
	},
    
    xAxis: {
        max: max,
        categories: category,
        labels: {
		   enabled: true,
		   formatter: function () {
                return "Ende"
            }
		},
		tickPositions: [max],
		plotLines: [{
        	zIndex: 5,
                value: max,
                color: 'grey',
                //dashStyle: 'shortdash',
                width: plot_line_width,
        }]
    },
    yAxis: {
    	gridLineWidth: 0,
        minorGridLineWidth: 0,
        title: {
            text: ""
        },
        plotLines: [{
        	zIndex: 5,
                value: series[0],
                color: 'grey',
                dashStyle: 'shortdash',
                width: plot_line_width,
        }]
    },
    tooltip: {
        shared: true,
        valueSuffix: suffix
    },
    credits: {
        enabled: false
    },
    plotOptions: {
    	series: {
    	    fillColor: {
                linearGradient: [0, 0, 0, series[series.length - 1]*1.5],
                stops: [
                    [0, "rgba(62,56,242,0.5)"],
                    [1, "rgba(62,56,242,0.1)"]
                ]
            },
    		color: "#3E38F2",
    		marker: {
                enabled: false
            }
    	},
        areaspline: {
        	stacking: "normal",
        	//fillOpacity: 0.33
        },
    },
    series: [{
        name: "Kontostand",
        data: series,
        showInLegend: show_in_legend
    },{
        name: "Grundbetrag",
        data: flat,
        color: "#00fad1",
        showInLegend: show_in_legend,
        visible: template == "final"
    }]
});

if (template != "decision"){
    chart.tooltip.refresh([chart.series[0].points[current_round - 1]]);
}