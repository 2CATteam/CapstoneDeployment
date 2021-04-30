var data = null
var measures = null
var toShow = null

//Percent of women with OUD during pregnancy who received MAT
//Build the line graph showing yourself vs other hospitals
function BuildLine(months, yourPercent, allPercent, canvas) { //Can use any other arguments for this
	var data = {
	labels: months, //Array of strings
	datasets: [{
		label: "You", // Name the series
		fill: false,
		data: yourPercent, //Array of percentages
		backgroundColor: ['rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
        'rgb(54, 162, 235)',
      ],
		 pointBackgroundColor: "rgb(0,0,0)",
		 pointBorderColor: "rgb(221,61,63)",
		 borderColor: "rgb(255,50,50)",
		 borderWidth: 3
	}, {
		label: "All", // Name the series
		data: allPercent,
		fill: false,
		backgroundColor: ['rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		'rgb(54, 162, 235)',
		], pointBackgroundColor: "rgb(0, 0, 0)",
		pointBorderColor: "rgb(237,199,134)",
		  borderColor: "rgb(75,192,192)",
		 backgroundColor: 'rgba(0, 0, 0, 1)',
		 borderWidth: 3,

	}],
	};

	var p1Line = new Chart(canvas, {
	type: 'line',
	data: data,
	options: {
		responsive: true, // Instruct chart js to respond nicely.
		//maintainAspectRatio: false, // Add to prevent default behavior of full-width/height 
		scales: {
		xAxes: [{
			scaleLabel: {
			display: true,
			labelString: 'Month'
			}
		}],
		yAxes: [{
			ticks: {
			beginAtZero: true
		},
			scaleLabel: {
			display: true,
			labelString: 'yLabel'
			}
		}]
		},
	}
	});

	return p1Line;
}

function BuildBar(yValues, chartTitle, canvas, yLabel="Value (units)",yourHospital) {
	var data = {
	xLabels: generateXAxis(yourHospital),
	datasets: [{
		label: chartTitle, // Name the series
		data: yValues,
		backgroundColor: generateColor(yourHospital),
	}],
	};

	var p1Bar = new Chart(canvas, {
		type: 'bar',
		data: data,
		options: {
			responsive: true, // Instruct chart js to respond nicely.
			//maintainAspectRatio: false, // Add to prevent default behavior of full-width/height
			scales: {
				xAxes: [{
					scaleLabel: {
					display: true,
					labelString: 'Hospital'
					}
				}],
				yAxes: [{
					ticks: {
						beginAtZero: true
					},
					scaleLabel: {
						display: true,
						labelString: yLabel
					}
				}]
			}
		}
	});

	return p1Bar;
	
}

/*
//Function to build 2 lines within the same graph
function BuildMultiple(xLabels, yValues1,yValues2, chartTitle1,chartTitle2) { //X label, y values for each graph, title for each line (will show up as a legend)
	var data = {
		xLabels: xLabels,
		datasets: [{
		label: chartTitle1, // Name the series
		fill: false,
		data: yValues1,
		backgroundColor: ['rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
		], pointBackgroundColor: "rgb(0,0,0)",
			 pointBorderColor: "rgb(237,199,134)",
			 borderColor: "rgb(75,192,192)",
			 borderWidth: 3
		}, {		label: chartTitle2, // Name the series
		data: yValues2,
		fill: false,
		backgroundColor: ['rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
		], pointBackgroundColor: "rgb(0, 0, 0)",
			 pointBorderColor: "rgb(221, 61, 63)",
			 borderColor: "rgb(255,50,50)",
			 backgroundColor: 'rgba(0, 0, 0, 1)',
			 borderWidth: 3,
	
		}],
	};
	
	var ctx = document.getElementById("myChart").getContext('2d');
	var myChart = new Chart(ctx, {
		type: 'line',
		data: data,
		options: {
		responsive: true, // Instruct chart js to respond nicely.
		maintainAspectRatio: false, // Add to prevent default behavior of full-width/height 
		scales: {
			xAxes: [{
			scaleLabel: {
				display: true,
				labelString: 'Month'
			}
			}],
			yAxes: [{
			scaleLabel: {
				display: true,
				labelString: 'Percent'
			}
			}]
		},
		}
	});
	
	return myChart;
	}
	
	//Function to build a single bar chart 
	function BuildSingle(xLabels, yValues, chartTitle) { //X axis labels, y axis values, legend
	var data = {
		xLabels: xLabels,
		datasets: [{
		label: chartTitle, // Name the series
		data: yValues,
		backgroundColor: ['rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
			'rgb(54, 162, 235)',
		],
		}],
	};
	
	var ctx = document.getElementById("myChart").getContext('2d');
	var myChart = new Chart(ctx, {
		type: 'bar',
		data: data,
		options: {
		responsive: true, // Instruct chart js to respond nicely.
		//maintainAspectRatio: false, // Add to prevent default behavior of full-width/height 
		scales: {
			xAxes: [{
			scaleLabel: {
				display: true,
				labelString: 'Date'
			}
			}],
			yAxes: [{
			ticks: {
				max: 100,
				min: 0,
				stepSize: 10,
				beginAtZero: true
			},
			scaleLabel: {
				display: true,
				labelString: 'Produced Count',
			 
			}
			}]
		},
		}
	});

	return myChart;
	}
*/


function generateXAxis(index)
{
var you = [];
	for (i = 0; i < 13; i++)
	{
		you[i] = "";
		you[index] = "You"
	}

	return you;
}

function generateColor(index)
{
	var color = [];
	for (i = 0; i < 13; i++) {
		color.push('rgb(54, 162, 235)');
	}
	color [index] =  'rgb(221, 61, 63)';
    return color;
}

function generateRange(base, start, end) {
	var toReturn = []

	for (var i = start; i <= end; i++) {
		var toAdd = base
		toAdd += i
		toReturn.push(toAdd)
	}

	return toReturn
}

function createButtons() {
	$.get("/static/measures.json").done((measuresIn) => {
		console.log(measures)
		measures = measuresIn
		$.get("/data", (dataIn) => {
			data = JSON.parse(dataIn)
			for (var i in measures) {
				let element = `
<button class="accordion">
	${measures[i].title}
</button>
<div class="panel">
   <div class="dropdown">
     <button class="dropbtn">Quarter</button>
     <div class="dropdown-content">
       <a onclick="generateQ3()"href="#">Q3</a>
       <a href="#">Q4</a>
     </div>
  </div>
  
	<p>${measures[i].description ? measures[i].description : ""}</p>
	<div class="canvasContainers">
		<canvas class="canvas1"></canvas>
		<canvas class="canvas2"></canvas>
	</div>
</div>`
				let dom = $(element)
				$("#buttonParent").append(dom)
				//TODO: Add each thing's canvas and update it
				//let plot1 = BuildLine()
				//dom.find(".canvas1")
				//TODO: Fix this
				for (var j in data[i.toLowerCase()]) {
					if (!data[i.toLowerCase()][j]) {
						data[i.toLowerCase()][j] = 0
					}
				}
				//console.log(data)
				//console.log(i)
				//console.log(data[i.toLowerCase()])

				//Choose which quarters to use and which one to graph
				//If you're having issues with choosing data, look here for bugs! This was not well-coded
				let quarters = []
				for (var j in data) {
					if (data[j] && j.match(/\d+Q\d+/i)) {
						quarters.push(j)
					}
				}
				quarters.sort()
				//console.log(quarters)

				let toShow = null
				for (var j in quarters) {
					if (data[quarters[j]].num_records > 20) {
						toShow = quarters[j]
					}
				}
				//console.log(toShow)

				let indivData = []
				let allData = []
				for (var j in quarters) {
					indivData.push(data[quarters[j]][i.toLowerCase()][8])
				}
				for (var j in quarters) {
					//Holy duct tape, Batman!
					allData.push(data[quarters[j]].total[parseInt(i.match(/(\d+)$/)[1])-1])
				}

				//console.log(indivData)
				//console.log(allData)

				//TODO: Include index for user's hospital ID
				let plot1 = BuildLine(quarters, roundList(indivData, 3), roundList(allData, 3), dom.find(".canvas1"))

				let plot2 = BuildBar(roundList(data[toShow][i.toLowerCase()], 3), "Hospitals", dom.find(".canvas2"), measures[i].yLabel, 8)
			}

			//JS Code for Tab Navigation
			var acc = document.getElementsByClassName("accordion");
			var i;

			for (i = 0; i < acc.length; i++) {
				acc[i].addEventListener("click", function() {
					this.classList.toggle("activeAccordion");
					var panel = this.nextElementSibling;
					if (panel.style.maxHeight) {
						panel.style.maxHeight = null;
					} else {
						panel.style.maxHeight = panel.scrollHeight + "px";
					}
				});
			}
		})
	}).fail(() => {
		alert("Error getting data from server. Is your token valid?")
	})
}


function roundList(list, places) {
	for (var i in list) {
		list[i] = Math.round(list[i] * Math.pow(10, places)) / Math.pow(10, places)
	}
	return list
}

$(document).ready(async () => {
	createButtons();
	createAdminTable();
})

function createAdminTable() {
	if (getCookie("admin") !== "True") {
		return
	}
	let toMove = $("#Account .centerChild .accountCard").detach()
	$("#Account .centerChild").addClass("hidden")
	$("#Account .flexColumn").removeClass("hidden")
	$("#Account .flexColumn").prepend(toMove)

	
}

function logout() {
	document.cookie = "token="
	location.reload()
}

function changePassword() {
	window.location.href = `/resetPassword?token=${getCookie("token")}${getCookie("admin") == "True" ? "&admin=True" : ""}`
}

function getCookie(key) {
	obj = {}
	list = document.cookie.split(";")
	for (x in list) {
		if (list[x]) {
			pair = list[x].split("=", 2)
			obj[pair[0].trim()] = pair[1].trim()
		}
	}
	return obj[key]
}

function setCookie(key, value) {
	document.cookie = `${key}=${value}`
}
