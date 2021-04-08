


//Percent of women with OUD during pregnancy who received MAT
//Build the line graph showing yourself vs other hospitals
function BuildP1Line(months, yourPercent,allPercent, yourHospital,allHospitals) { //Can use any other arguments for this
  var data = {
    labels: months, //Array of strings
    datasets: [{
      label: yourHospital, // Name the series
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
      ], pointBackgroundColor: "rgb(0,0,0)",
         pointBorderColor: "rgb(237,199,134)",
         borderColor: "rgb(75,192,192)",
         borderWidth: 3
    }, {      label: allHospitals, // Name the series
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
         pointBorderColor: "rgb(221, 61, 63)",
         borderColor: "rgb(255,50,50)",
         backgroundColor: 'rgba(0, 0, 0, 1)',
         borderWidth: 3,

    }],
  };

  var ctx = document.getElementById("p1Line").getContext('2d');
  var p1Line = new Chart(ctx, {
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
            max: 100,
            min: 0,
            stepSize: 10,
            beginAtZero: true
        },
          scaleLabel: {
            display: true,
            labelString: 'Percent'
          }
        }]
      },
    }
  });

  return p1Line;
}

function BuildP1Bar(xLabels, yValues, chartTitle) {
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

  var ctx = document.getElementById("p1Bar").getContext('2d');
  var p1Bar = new Chart(ctx, {
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
            max: 100,
            min: 0,
            stepSize: 10,
            beginAtZero: true
        },
          scaleLabel: {
            display: true,
            labelString: 'Percent %',
           
          }
        }]
      },
    }
  });

  return p1Bar;
  
}


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
      }, {      label: chartTitle2, // Name the series
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