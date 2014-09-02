openerp.polling = function(instance)  {
    
    var _t = instance.web._t,
		_lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    
    instance.polling={};
    
    instance.polling.charts=instance.web.Widget.extend({
    	template:"demo",
    	start:function(){
    	var self=this;
    	
    	var assid_cont = document.getElementById("assid_cont");
    	

//*****demo1_div start*****
	$(function funcdemo1(){
			var demo1_width = document.getElementById("demo1_div").offsetWidth;
			var demo1_height = document.getElementById("demo1_div").offsetHeight;
						
			var container, stats;
			var camera, scene, projector, raycaster,projectorclick,raycasterclick, renderer;
			
			var object1,object2;

			var mouse = new THREE.Vector2(), INTERSECTED;
			var mouseclick = new THREE.Vector2(), INTERSECTEDCLICK;
			var radius = 100, theta = 0;
			
			var mesh;
			
			info_top=0;
			info_left=0;
			
			init();
			animate();

			function init() {

				container = document.createElement( 'div' );
				container.id="container";
				document.getElementById("demo1_div").appendChild( container );
				
				var opts = {
				lines: 12, // The number of lines to draw
				length: 10, // The length of each line
				width: 5, // The line thickness
				radius: 10, // The radius of the inner circle
				color: '#000', // #rbg or #rrggbb
				speed: 1, // Rounds per second
				trail: 100, // Afterglow percentage
				shadow: true // Whether to render a shadow
				};

				var container = document.getElementById( 'container' );
				var target = document.createElement( 'div' );
				target.id="target";
				target.style.width = '100%';
				target.style.height = '100%';				
				container.appendChild(target);

				var target1 = document.getElementById('target');
				var spinner = new Spinner(opts).spin(target1);

				camera = new THREE.PerspectiveCamera( 700, demo1_width / demo1_height, 1, 10000 );
		
				scene = new THREE.Scene();

				var light = new THREE.DirectionalLight( 0xffffff, 2 );
				light.position.set( 1, 1, 1 ).normalize();
				scene.add( light );

				var light = new THREE.DirectionalLight( 0xffffff );
				light.position.set( -1, -1, -1 ).normalize();
				scene.add( light );



				object1 = new THREE.Mesh( new THREE.CubeGeometry(5,5,5), new THREE.MeshLambertMaterial( { color: Math.random() * 0xffffff } ) );

				object1.position.set(0,18,0);
				

				object2 = new THREE.Mesh( new THREE.CubeGeometry(5,5,5), new THREE.MeshLambertMaterial( { color: Math.random() * 0xffffff } ) );

				object2.position.set(0,-18,0);

				
				var loader = new THREE.OBJMTLLoader();

			
                loader.addEventListener('load', function(event) {
					var obj2=event.content;
                    mesh = obj2;
                    obj2.position.set(0,0,0);
                    
					scene.add(object1);
					scene.add(object2);	
					scene.add(mesh);

					var container=document.getElementById("container");
					var target=document.getElementById("target");

					if (target)
					{
						container.removeChild(target);
					}					
					
                });                
				loader.load('/polling/static/src/obj/plane.obj');
				
				projector = new THREE.Projector();
				raycaster = new THREE.Raycaster();
				projectorclick = new THREE.Projector();
				raycasterclick = new THREE.Raycaster();

				renderer = new THREE.WebGLRenderer();
				renderer.setClearColor( 0xf0f0f0 );
				renderer.setSize( demo1_width , demo1_height );
				renderer.sortObjects = false;
				container.appendChild(renderer.domElement);

				camera.position.set(100,100,100); 
				camera.lookAt( scene.position );
				
				controls = new THREE.OrbitControls(camera, renderer.domElement); //重新为相机加载控制器 
				camera.updateProjectionMatrix(); //更新相机
				
				
				stats = new Stats();
				stats.domElement.style.position = 'absolute';
				stats.domElement.style.top = '0%';
				container.appendChild( stats.domElement );
				


				document.getElementById("demo1_div").addEventListener( 'mousemove', onDocumentMouseMove, false );
				document.getElementById("demo1_div").addEventListener( 'click', onDocumentMouseClick, false );
//				window.addEventListener( 'resize', onWindowResize, false );

			}

			function onWindowResize() {

				camera.aspect = demo1_width / demo1_height;
				camera.updateProjectionMatrix();

				renderer.setSize( demo1_width , demo1_height );

			}

			function onDocumentMouseClick( event ){
				event.preventDefault();

				mouseclick.x = ( (event.clientX-250) / demo1_width ) * 2 - 1;
				mouseclick.y = - ( (event.clientY-30) / demo1_height ) * 2 + 1;				
			}
			
			
			function onDocumentMouseMove( event ) {

				event.preventDefault();

				mouse.x = ( (event.clientX-250) / demo1_width ) * 2 - 1;
				mouse.y = - ( (event.clientY-30) / demo1_height ) * 2 + 1;
				
				info_top=event.clientY;
				info_left=event.clientX-250;

			}


			function animate() {

				requestAnimationFrame( animate );

				render();
				render_click();
				stats.update();

			}

			function render_click(){
				var vector = new THREE.Vector3( mouseclick.x, mouseclick.y, 1 );
				projectorclick.unprojectVector( vector, camera );

				raycasterclick.set( camera.position, vector.sub( camera.position ).normalize() );

				var intersects = raycasterclick.intersectObjects( scene.children );

				if ( intersects.length > 0 ) {

					if ( INTERSECTEDCLICK != intersects[ 0 ].object ) {

						if ( INTERSECTEDCLICK ) 
						{
				//			INTERSECTEDCLICK.material.emissive.setHex( INTERSECTEDCLICK.currentHex );
				//			alert("1");
							
						}
						INTERSECTEDCLICK = intersects[ 0 ].object;
				//		INTERSECTEDCLICK.currentHex = INTERSECTEDCLICK.material.emissive.getHex();
		//				INTERSECTEDCLICK.material.emissive.setHex( 0xff00ff );
						
						if (INTERSECTEDCLICK ==  object1)
						{
							contdemo2("4,BY0002");
							contdemo3("4,BY0002");
						}
						if (INTERSECTEDCLICK ==  object2)
						{
							contdemo2("ZK_001,总控统计电");
							contdemo3("ZK_001,总控统计电");							
						}

					}

				} else {

					if ( INTERSECTEDCLICK ) 
					{

	//					INTERSECTEDCLICK.material.emissive.setHex( INTERSECTEDCLICK.currentHex );
					}
					INTERSECTEDCLICK = null;
		
				}

				renderer.render( scene, camera );
	
			}

			function render() {
				// find intersections

				var vector = new THREE.Vector3( mouse.x, mouse.y, 1 );
				projector.unprojectVector( vector, camera );

				raycaster.set( camera.position, vector.sub( camera.position ).normalize() );

				var intersects = raycaster.intersectObjects( scene.children );

				if ( intersects.length > 0 ) {


					if ( INTERSECTED != intersects[ 0 ].object ) {

						if ( INTERSECTED ) 
						{
							INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
				//			alert("1");
							
						}
						INTERSECTED = intersects[ 0 ].object;
						INTERSECTED.currentHex = INTERSECTED.material.emissive.getHex();
						INTERSECTED.material.emissive.setHex( 0xff0000 );
						
						

						var container = document.getElementById( 'container' );
						var info = document.createElement( 'div' );
						info.id="info";
						info.style.position = 'absolute';				
						container.appendChild( info );				
						

						var info = document.getElementById("info");
						info.style.left = info_left+"px";
						info.style.top = info_top+"px";
						
						if (INTERSECTED ==object1)
						{
							info.innerHTML = "BY0002";
						}
						
						if (INTERSECTED ==object2)
						{
							info.innerHTML = "2,light";
						}
					}


					

				} else {

					if ( INTERSECTED ) 
					{

						INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
					}
					INTERSECTED = null;
					var container=document.getElementById("container");
					var info=document.getElementById("info");

					if (info)
					{
						container.removeChild(info);
					}
		
				}

				renderer.render( scene, camera );

			}

		
	});

//**********************************************************

//*****#demo2_div start*****
 
	var demo2_div = document.getElementById( 'demo2_div' );
	demo2_div.innerHTML = "please choose an asset!!!";
		 
	function contdemo2(require_data){
		
			if (require_data != undefined)
			{
				assid_cont.value= require_data;
				var opts = {
					lines: 10, // The number of lines to draw
					length: 8, // The length of each line
					width: 4, // The line thickness
					radius: 8, // The radius of the inner circle
					color: '#000', // #rbg or #rrggbb
					speed: 2, // Rounds per second
					trail: 100, // Afterglow percentage
					shadow: true, // Whether to render a shadow
					position:'relative'
				};

				var container = document.getElementById( 'demo2_div' );
				container.innerHTML = "";				
				var target = document.createElement( 'div' );
				target.id="target";
				target.style.width = '100%';
				target.style.height = '100%';				
				container.appendChild(target);

				var target1 = document.getElementById('target');
				var spinner = new Spinner(opts).spin(target1);
				funcdemo2();				
			}

	}
 

 
	function funcdemo2(){
		var model= new instance.web.Model("polling.asset.collect.record");

		var req_result = assid_cont.value;
		
		if (req_result != "CALLING_ARGS_ERROR")
		{
			require = req_result;
		}
		else
		{
			require = undefined;
		}
		
		model.query(["asset_id","asset_attr_id","asset_attr_high","asset_attr_low","collect_value","collect_time"]).limit(5000).all().then(function(result){
		mytitle1="The history of asset_id \""+require+"\"";
		
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
			if (result[i].asset_id !=undefined && result[i].asset_id==require)
			{		
			resultdatatemp = [];
		//highstock datatime
			datetemp1=result[i].collect_time.split("-");
			datetemp2=datetemp1[2].split(" ");
			datetemp3=datetemp2[1].split(":");
			datetemp=Date.UTC(datetemp1[0],datetemp1[1]-1,datetemp2[0],datetemp3[0],datetemp3[1],datetemp3[2]);
			resultdatatemp.push(datetemp);		

		//highstock data

			maxdata = result[i].asset_attr_high;
			mindata = result[i].asset_attr_low;	
		
			if ((maxdata ==false )&& (mindata !=false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". ["+result[i].asset_attr_low+",null]--";				
			}

			if ((maxdata != false)&&(mindata ==false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". [null,"+result[i].asset_attr_high+"]--";				
			}
						
			if ((maxdata == false)&&(mindata == false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". [null,null]--";
				
			}
				
			if ((maxdata !=false)&&(mindata !=false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". ["+result[i].asset_attr_low+","+result[i].asset_attr_high+"]--";				
			}
	
			mydata = result[i].collect_value;
			
			if ((maxdata ==false )&& (mindata !=false))
			{
				datatemp = (mydata - mindata)/Math.abs(mydata)*100;
				if (datatemp>61.8)
				{
					datatemp = 61.8;
				}
				if (datatemp<0)
				{
					datatemp = datatemp*Math.abs(mydata)/Math.abs(mindata);
				}

			}

			if ((maxdata != false)&&(mindata ==false))
			{
				datatemp = (maxdata - mydata)/Math.abs(maxdata)*100;
				if (datatemp <0)
				{
					datatemp = 100 - datatemp;	
				}
				else
				{				
					if (datatemp<61.8)
					{
						datatemp=61.8;
					}
				}	
			}
						
			if ((maxdata == false)&&(mindata == false))
			{
				datatemp = 61.8;	
			}
				
			if ((maxdata !=false)&&(mindata !=false))
			{
				datatemp = (mydata - mindata)/(maxdata - mindata)*100;
			}
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
			
		var container = document.getElementById( 'demo2_div' );
		var target = document.getElementById( 'target' );
		if (target)
		{
			container.removeChild(target);
		}				
		createChart();

//highstock start


		function createChart() {

			$('#demo2_div').highcharts('StockChart', {
				chart: {
				},

				rangeSelector: {
					buttons: [{
						count:'30',
						type: 'second',
						text: '30s'
						},{
						count: 1,
						type: 'minute',
						text: '1m'
						}, {
						count: 1,
						type: 'hour',
						text: '1h'
						},{
						count:1,
						type: 'day',
						text: '1d'
						},{
						count:1,
						type: 'week',
						text: '1w'
						},{
						type: 'all',
						text: 'All'
						}],
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



	
    	});
 

	}

//**********************************************************

//*****#demo3_div start*****

	var demo3_div = document.getElementById( 'demo3_div' );
	demo3_div.innerHTML = "please choose an asset!!!";

	function contdemo3(require_data){
		var model= new instance.web.Model("polling.asset.collect.finalrecord");
		
		var req_result = assid_cont.value;

			if (req_result != undefined)
			{

				funcdemo3();
				funcdemo3_addseries();
				$(function() {

					// set up the updating of the chart each second

					 var funcdemo3_addpoint = setInterval(function () {


						
//-------------------------------------

		var model= new instance.web.Model("polling.asset.collect.finalrecord");

		if (req_result != "CALLING_ARGS_ERROR")
		{
			require = req_result;
		}
		else
		{
			require = undefined;
		}
		model.query(["asset_id","asset_attr_id","asset_attr_high","asset_attr_low","collect_value","collect_time"]).all().then(function(result){
		mytitle1="The history of asset_id \""+require+"\"";
		
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
			if (result[i].asset_id !=undefined && result[i].asset_id==require)
			{		
			resultdatatemp = [];
		//highstock datatime
			datetemp1=result[i].collect_time.split("-");
			datetemp2=datetemp1[2].split(" ");
			datetemp3=datetemp2[1].split(":");
			datetemp=Date.UTC(datetemp1[0],datetemp1[1]-1,datetemp2[0],datetemp3[0],datetemp3[1],datetemp3[2]);
			resultdatatemp.push(datetemp);		

		//highstock data

			maxdata = result[i].asset_attr_high;
			mindata = result[i].asset_attr_low;	
		
			if ((maxdata ==false )&& (mindata !=false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". ["+result[i].asset_attr_low+",null]--";				
			}

			if ((maxdata != false)&&(mindata ==false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". [null,"+result[i].asset_attr_high+"]--";				
			}
						
			if ((maxdata == false)&&(mindata == false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". [null,null]--";
				
			}
				
			if ((maxdata !=false)&&(mindata !=false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". ["+result[i].asset_attr_low+","+result[i].asset_attr_high+"]--";				
			}
	
			mydata = result[i].collect_value;
			
			if ((maxdata ==false )&& (mindata !=false))
			{
				datatemp = (mydata - mindata)/Math.abs(mydata)*100;
				if (datatemp>61.8)
				{
					datatemp = 61.8;
				}
				if (datatemp<0)
				{
					datatemp = datatemp*Math.abs(mydata)/Math.abs(mindata);
				}

			}

			if ((maxdata != false)&&(mindata ==false))
			{
				datatemp = (maxdata - mydata)/Math.abs(maxdata)*100;
				if (datatemp <0)
				{
					datatemp = 100 - datatemp;	
				}
				else
				{				
					if (datatemp<61.8)
					{
						datatemp=61.8;
					}
				}	
			}
						
			if ((maxdata == false)&&(mindata == false))
			{
				datatemp = 61.8;	
			}
				
			if ((maxdata !=false)&&(mindata !=false))
			{
				datatemp = (mydata - mindata)/(maxdata - mindata)*100;
			}
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
			if ($('#demo3_div').highcharts() == null)
				{					
					clearInterval(funcdemo3_addpoint);
					break;
					
				}	
			for (n=0;n<markname.length+1;n++)
			{
					if ($('#demo3_div').highcharts().series[n] !=undefined && $('#demo3_div').highcharts().series[n].name == markname[m])
					{
						$('#demo3_div').highcharts().series[n].addPoint(markdata[m][0]);

						break;	
					}
			}
				
		
		}

	
		});								


					}, 1000);
				});
			
			
								
			}
	
	}
 
	function funcdemo3_addseries() {


						
//-------------------------------------

		var model= new instance.web.Model("polling.asset.collect.finalrecord");
		var req_result = assid_cont.value;

		if (req_result != "CALLING_ARGS_ERROR")
		{
			require = req_result;
		}
		else
		{
			require = undefined;
		}
		model.query(["asset_id","asset_attr_id","asset_attr_high","asset_attr_low","collect_value","collect_time"]).all().then(function(result){
		mytitle1="The history of asset_id \""+require+"\"";
		
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
			if (result[i].asset_id !=undefined && result[i].asset_id==require)
			{		
			resultdatatemp = [];
		//highstock datatime
			datetemp1=result[i].collect_time.split("-");
			datetemp2=datetemp1[2].split(" ");
			datetemp3=datetemp2[1].split(":");
			datetemp=Date.UTC(datetemp1[0],datetemp1[1]-1,datetemp2[0],datetemp3[0],datetemp3[1],datetemp3[2]);
			resultdatatemp.push(datetemp);		

		//highstock data

			maxdata = result[i].asset_attr_high;
			mindata = result[i].asset_attr_low;	
		
			if ((maxdata ==false )&& (mindata !=false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". ["+result[i].asset_attr_low+",null]--";				
			}

			if ((maxdata != false)&&(mindata ==false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". [null,"+result[i].asset_attr_high+"]--";				
			}
						
			if ((maxdata == false)&&(mindata == false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". [null,null]--";
				
			}
				
			if ((maxdata !=false)&&(mindata !=false))
			{
				myname = "Attribute \""+result[i].asset_attr_id+"\". ["+result[i].asset_attr_low+","+result[i].asset_attr_high+"]--";				
			}
	
			mydata = result[i].collect_value;
			
			if ((maxdata ==false )&& (mindata !=false))
			{
				datatemp = (mydata - mindata)/Math.abs(mydata)*100;
				if (datatemp>61.8)
				{
					datatemp = 61.8;
				}
				if (datatemp<0)
				{
					datatemp = datatemp*Math.abs(mydata)/Math.abs(mindata);
				}

			}

			if ((maxdata != false)&&(mindata ==false))
			{
				datatemp = (maxdata - mydata)/Math.abs(maxdata)*100;
				if (datatemp <0)
				{
					datatemp = 100 - datatemp;	
				}
				else
				{				
					if (datatemp<61.8)
					{
						datatemp=61.8;
					}
				}	
			}
						
			if ((maxdata == false)&&(mindata == false))
			{
				datatemp = 61.8;	
			}
				
			if ((maxdata !=false)&&(mindata !=false))
			{
				datatemp = (mydata - mindata)/(maxdata - mindata)*100;
			}
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
		$('#demo3_div').highcharts().addSeries(valuetmp);				

		}
//		alert($('#demo3_div').highcharts().series[2].name);		


	
		});								


	}
		


		function funcdemo3() {

			$('#demo3_div').highcharts('StockChart', {
				chart: {
				},

				rangeSelector: {
					buttons: [{
						count:'10',
						type: 'second',
						text: '10s'
						},{
						count:'30',
						type: 'second',
						text: '30s'
						},{
						count: 1,
						type: 'minute',
						text: '1m'
						}, {
						count: 1,
						type: 'hour',
						text: '1h'
						},{
						type: 'all',
						text: 'All'
						}],
					selected: 0
				},
				title: {
					text:"The live data"
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
		    
				series: []

			});
			}


//**********************************************************

/*	
	var tmp2 = 0;
	var model3= new instance.web.Model("polling.asset.collect.record");
	tmp = model3.call("chart_require",["2*#GET"," "],{context:new instance.web.CompoundContext()});
	tmp.done(function(result){tmp2 = result});

	alert(tmp2);
*/





		},    	
    });
    	
  	instance.web.client_actions.add('polling.charts', 'instance.polling.charts');  
 }
    
