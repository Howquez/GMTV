// define seq() function as in R
	function* seq( start, end, step = 1 ){
	  if( end === undefined ) [end, start] = [start, 0];
	  for( let n = start; n <= end; n += step ) yield n;
	}

// initiate vars from python
	let template = js_vars.template;
	let current_round  = js_vars.current_round;
	let endowments = js_vars.endowments;
	let stock = js_vars.stock || 0;
	console.log(stock);

// get categories, i.e. the rounds
	var category = Array.from(seq(1, current_round));

	for(var i=0;i<category.length;i++){
		category[i]="Runde #"+category[i];
	}

// determine which series to be displayed
	var series = endowments;
	var suffix = " Punkte";
	plot_line_label = "Anfangsausstattung";

	if (template == "results"){
		series = stock;
		suffix = " Euro";
		plot_line_label = "Grundbetrag";

	}

	// console.log(current_round);
	// console.log(endowments);
	// console.log(category);


var chart = Highcharts.chart('container', {
    chart: {
        type: 'areaspline',
        backgroundColor: "transparent",
        height: (4 / 16 * 100) + '%' // 16:9 ratio
    },
    title: {
        text: ""
    },
    exporting: {
				enabled: false
	},
    
    xAxis: {
        categories: category,
        labels: {
		   enabled: false
		},
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
                width: 1,
                label: {
                    text: ""//plot_line_label
                },
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
    		color: "#00C851"
    	},
        areaspline: {
            fillOpacity: 0.33
        }
    },
    series: [{
        name: "Kontostand",
        data: series,
        showInLegend: false
    }]
});