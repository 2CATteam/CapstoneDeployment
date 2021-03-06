var data = null
var measures = null
var toShow = null
var quarters = null

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
	color [index] = 'rgb(221, 61, 63)';
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
		console.log(measuresIn)
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
						    </div>
					   </div>

						<p>${measures[i].description ? measures[i].description : ""}</p>
						<div class="canvasContainers">
							<div class="canvasInnerContainer"><canvas class="canvas1"></canvas></div>
							<div class="canvasInnerContainer"><canvas class="canvas2"></canvas></div>
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
				quarters = []
				for (var j in data) {
					if (data[j] && j.match(/\d+Q\d+/i)) {
						quarters.push(j)
					}
				}
				quarters.sort()
				//console.log(quarters)

				let quartersParent = dom.find(".dropdown-content")

				for (var j in quarters) {
					if (data[quarters[j]].num_records > 20) {
						toShow = quarters[j]
					}
					quartersParent.append(`<a href="javascript:void(0)" onclick="setQuarter('${quarters[j]}')">${quarters[j]}</a>`)
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
				var plot1 = BuildLine(quarters, roundList(indivData, 3), roundList(allData, 3), dom.find(".canvas1"))
				dom.find(".canvas1").data("graph", plot1)
				var plot2 = BuildBar(roundList(data[toShow][i.toLowerCase()], 3), "Hospitals", dom.find(".canvas2"), measures[i].yLabel, 8)
				dom.find(".canvas2").data("graph", plot2)
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

function setQuarter(toSet) {
	toShow = toSet
	rebuildGraphs()
}

function rebuildGraphs() {
	let l = 0
	for (var i in measures) {
		l++
		let indivData = []
		let allData = []
		for (var j in quarters) {
			indivData.push(data[quarters[j]][i.toLowerCase()][8])
		}
		for (var j in quarters) {
			//Holy duct tape, Batman!
			allData.push(data[quarters[j]].total[parseInt(i.match(/(\d+)$/)[1])-1])
		}
		let el = $(`#buttonParent .panel:nth-child(${l * 2})`)
		el.find(".canvas2").data("graph").destroy()
		let newPlot = BuildBar(roundList(data[toShow][i.toLowerCase()], 3), "Hospitals", el.find(".canvas2"), measures[i].yLabel, 8)
		el.find(".canvas2").data("graph", newPlot)
	}
}

function roundList(list, places) {
	for (var i in list) {
		list[i] = Math.round(list[i] * Math.pow(10, places)) / Math.pow(10, places)
	}
	return list
}

//https://css-tricks.com/snippets/jquery/make-jquery-contains-case-insensitive/
$.expr[":"].contains = $.expr.createPseudo(function(arg) {
    return function( elem ) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
})

$(document).ready(() => {
	createButtons();
	createAdminTable();
	updateMyAccount();
	$("#search").keydown(search).change(search).keypress(search)
})

function search() {
	$("#buttonParent").children().removeClass("hidden")
	$(`#buttonParent > :not(:contains('${$(this).val()}'))`).addClass("hidden")
	$("#buttonParent > button:visible").next().removeClass("hidden")
	$("#buttonParent > div:visible").prev().removeClass("hidden")
}

function createAdminTable() {
	if (getCookie("admin") !== "True") {
		return
	}
	let toMove = $("#Account .centerChild .accountCard").detach()
	$("#Account .centerChild").addClass("hidden")
	$("#Account .flexColumnFull").removeClass("hidden")
	$("#Account .flexColumnFull").prepend(toMove)

	$.post("/adminInfo", (data, textStatus, xhr) => {
		if (xhr.status == 200) {
			let select = $("#userHospitalSelect")
			data.hospitals = data.hospitals.sort((a, b) => a.hospital_name.localeCompare(b.hospital_name))
			for (var i in data.hospitals) {
				select.append($(`<option value="${data.hospitals[i].hospital_id}">${data.hospitals[i].hospital_name}</option>`))
			}
			let table = $("#Users")
			console.log(data)
			data.users = data.users.sort((a, b) => a.email.localeCompare(b.email))
			for (var i in data.users) {
				let hName = "None"
				for (var j in data.hospitals) {
					if (data.hospitals[j].hospital_id == data.users[i].hospital_id) {
						hName = data.hospitals[j].hospital_name
						break
					}
				}
				table.append($(`<tr>
					<td>${data.users[i].username}</td>
					<td>${data.users[i].email}</td>
					<td>${data.users[i].admin == "True" ? "Yes" : "No"}</td>
					<td>${hName}</td>
					<td>
						<button class="tableButton" onclick="deleteAccount('${data.users[i].username}')">
							Remove Account
						</button>
					</td>
				</tr>`))
			}
		} else {
			console.log(xhr)
			console.log(data)
			alert("Authentication failed when setting up the account view")
		}
	})
}

function updateMyAccount() {
	let username = getCookie("username")
	if (username) {
		$("#accountUsername").text(username)
	} else {
		$("#accountUsername").text("Unknown")
	}
	let email = getCookie("email")
	if (email) {
		$("#accountEmail").text(email)
	} else {
		$("#accountEmail").text("Unknown")
	}
	let hospital_name = getCookie("hospital_name")
	if (hospital_name) {
		$("#accountHospital").text(hospital_name)
	} else {
		$("#accountHospital").text("Unknown")
	}
}

function createUser() {
	let path = "/createUser"
	if ($("#adminAdding:checked").length > 0) {
		path = "/createAdmin"
	}
	$.post(path, {email: $("#emailAdding").val(), username: $("#usernameAdding").val(), hospital: $("#userHospitalSelect").val()}, (data, statusText, xhr) => {
		if (xhr.status == 200) {
			alert("User created! The user will receive an email shortly with the invite.")
			$("#usernameAdding").val("")
			$("#emailAdding").val("")
		}
	})
}

function deleteAccount(user) {
	if (!user) {
		if (confirm("This action will delete your own account. This cannot be undone.")) {
			user = getCookie("username")
		} else {
			return
		}
	} else {
		if (!confirm(`You are about to delete the following account:

${user}

This action cannot be undone. Are you sure?`)) {
			return
		}
	}
	$.post("/deleteUser", {username: user}, (data, textStatus, xhr) => {
		if (xhr.status == 200) {
			alert("User deleted")
			$(`#Users tr:contains('${user}')`).remove()
			if (user == getCookie("username")) {
				location.reload()
			}
		} else {
			alert(xhr.responseText)
		}
	})
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
