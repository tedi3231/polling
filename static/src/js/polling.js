openerp.polling = function(instance)  {
    
    var _t = instance.web._t,
    _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    
    instance.polling={};
    
    instance.polling.charts=instance.web.Widget.extend({
    		template:"demo",
    		start:function(){
    		var self=this;

 //#demo2_div highstock:  
		var model= new instance.web.Model("polling.asset.collect.record");
		model.query(["asset_id","asset_attr_id","asset_attr_high","asset_attr_low","collect_value","collect_time"]).all().then(function(result){
		var mytitle1;
		mytitle1="The history of asset_id \""+result[0].asset_id+"\"";
		
		var datetemp;
		var datetemp1;
		var datetemp2;
		var datetemp3;
		var mydate;
		
		var mydata;
		var maxdata;
		var mindata;
		var datatemp;
		var resultdata;
		
		var myname;
		var mynamecat;
		
		var markname=[];
		var markdata=[];
		var valuetemp={};
		var resultvalue=[];		 



		for (i=0;i<result.length;i++)
		{	
			if (result[i].asset_id !=undefined)
			{		
			resultdatatemp = [];
		//highstock datatime
			datetemp1=result[i].collect_time.split("-");
			datetemp2=datetemp1[2].split(" ");
			datetemp3=datetemp2[1].split(":");
			datetemp=Date.UTC(datetemp1[0],datetemp1[1]-1,datetemp2[0],datetemp3[0],datetemp3[1],datetemp3[2]);
			resultdatatemp.push(datetemp);		

		//highstock data
			myname = "Attribute \""+result[i].asset_attr_id+"\". ["+result[i].asset_attr_low+","+result[i].asset_attr_high+"]--";
				

			maxdata = result[i].asset_attr_high;
			mindata = result[i].asset_attr_low;
			mydata = result[i].collect_value;
			datatemp = (mydata - mindata)/(maxdata - mindata)*100;
			resultdatatemp.push(datatemp);
			

		//highstock data to category
			var k=0;
			if (markname.length ==0 )
			{
				markname[0]=myname;
				markdata[0]=[];
				markdata[0].push(resultdatatemp);	
			}
			else
			{	
				for (k=0;k<markname.length;k++)
				{
					if (myname == markname[k])
						break;	
				}
				if (k == markname.length)
				{				
					markname.push(myname);
					markdata.push([]);
					markdata[k].push(resultdatatemp);
				}
				else
				{
					markdata[k].push(resultdatatemp);
				}
			}

			}		
		}
			
		for (m=0;m<markname.length;m++)
		{			
			valuetmp = {
					name:markname[m],
					data:markdata[m]				
				};
			resultvalue.push(valuetmp);			
		}			

		var seriesOptions=[],
			yAxisOptions=[],
			seriesCounter=0,
			colors = Highcharts.getOptions().colors;
		
		createChart();

//highstock start


		function createChart() {

			$('#demo2').highcharts('StockChart', {
				chart: {
				},

				rangeSelector: {
					selected: 4
				},
				title: {
					text:mytitle1
				},
				yAxis: {
					labels: {
						formatter: function() {
							return (this.value > 0 ? '+' : '') + this.value + '%';
						}
					},
					plotLines: [{
						value: 0,
						width: 2,
						color: 'silver'
					}]
				},
		    
				plotOptions: {
//			    	series: {
//			    		compare: 'value'
//			    	}
				},
		    
				tooltip: {
					pointFormat: '<span style="color:{series.color}">{series.name}</span> <b>  states:{point.y}%</b><br/>',
					valueDecimals: 2
				},
		    
				series: resultvalue

			});
		}

//#demo2_div highstock finish

//#demo3_div highstock start

﻿$(function() {
	
	Highcharts.setOptions({
		global : {
			useUTC : false
		}
	});
	
	// Create the chart
	$('#demo3').highcharts('StockChart', {
		chart : {
			events : {
				load : function() {

					// set up the updating of the chart each second
					var series = this.series[0];
					setInterval(function() {
						var x = (new Date()).getTime(), // current time
						y = Math.round(Math.random() * 100);
						series.addPoint([x, y], true, true);
					}, 1000);
				}
			}
		},
		
		rangeSelector: {
			buttons: [{
				count: 1,
				type: 'minute',
				text: '1M'
			}, {
				count: 5,
				type: 'minute',
				text: '5M'
			}, {
				type: 'all',
				text: 'All'
			}],
			inputEnabled: false,
			selected: 0
		},
		
		title : {
			text : 'Live random data'
		},
		
		exporting: {
			enabled: false
		},
		
		series : [{
			name : 'Random data',
			data : (function() {
				// generate an array of random data
				var data = [], time = (new Date()).getTime(), i;

				for( i = -999; i <= 0; i++) {
					data.push([
						time + i * 1000,
						Math.round(Math.random() * 100)
					]);
				}
				return data;
			})()
		}]
	});

});	

//#demo3_div highstock stop

	
    			});
    	
		},

    	
    	});
    	
  	instance.web.client_actions.add('polling.charts', 'instance.polling.charts');  
 }
    
