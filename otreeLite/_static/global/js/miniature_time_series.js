// define seq() function as in R
	function* seq( start, end, step = 1 ){
	  if( end === undefined ) [end, start] = [start, 0];
	  for( let n = start; n <= end; n += step ) yield n;
	}

// initiate vars from python
	let num_rounds  = js_vars.num_rounds;
	let stock = js_vars.stock || 0;
	series = stock;

// get categories, i.e. the rounds
	var category = Array.from(seq(1, current_round));
	for(var i=0;i<category.length;i++){
		category[i]="Period #"+category[i];
	}


var chart = Highcharts.chart('container', {
    chart: {
        type: "areaspline",
        backgroundColor: "transparent",
        height: (6 / 16 * 100) + '%', // 16:9 ratio
        margin: [0, 0, 0, 0]
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
		}
    },
    yAxis: {
    	gridLineWidth: 0,
    	labels: {
        		   enabled: false
        		},
        minorGridLineWidth: 0,
        title: {
            text: ""
        }
    },
    tooltip: {
        enabled: false
    },
    credits: {
        enabled: false
    },
    plotOptions: {
    	series: {
    	    fillColor: {
                linearGradient: [0, 0, 0, series[series.length - 1]*1.5],
                stops: [
                    [0, "rgba(13,110,253,0.5)"],
                    [1, "rgba(13,110,253,0.1)"]
                ]
            },
    		color: "#0d6efd",
    		marker: {
                enabled: false
            }
    	},
        areaspline: {
        	stacking: "normal",
        	fillOpacity: 0.33
        },
    },
    series: [{
        name: "Earnings",
        data: series,
        showInLegend: false
    }]
});