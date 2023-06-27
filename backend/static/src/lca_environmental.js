// Maybe we need this to be an array if we have multiple results for Life Excpectancy, Health etc.
var resultProcess1 = 0;
var resultProcess2 = 0;

// 1, 2, 3 represent the differnt types of calculation (Pup,Pmid,Pdown)
function checkCSVHeader(data,type){ 
  
  if(data.length == 0){
    return false;
  }

  if(type == 1 &&  data[0].length != 3 && (data[0][0] !== "Indicator" || data[0][1] !== "Mass" || data[0][2] !== "Emission Factor Up")){  
    return false; 
  }
  
  if(type == 2 && data[0].length != 3 && (data[0][0] !== "Indicator" || data[0][1] !== "Mass" || data[0][2] !== "Emission Factor Mid")){  
    return false; 
  }

  if(type == 3 && data[0].length != 4 && (data[0][0] !== "Indicator" || data[0][1] !== "Mass" || data[0][2] !== "Emission Factor Down" || data[0][3] !== "Distance")){  
    return false; 
  }
  
  return true;
  
}

function initializeChart(ctx) {
  var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
      labels: ['Case Study Result', 'Proposed Study Result'],
      datasets: []
    },

    // Configuration options go here
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
            //max: 3000,
            stepSize: 500000
          }
        }]
      },
      "animation": {
        "duration": 1,
        "onComplete": function() {
          var chartInstance = this.chart,
            ctx = chartInstance.ctx;
  
          ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
          ctx.textAlign = 'center';
          ctx.textBaseline = 'bottom';
  
          this.data.datasets.forEach(function(dataset, i) {
            var meta = chartInstance.controller.getDatasetMeta(i);
            meta.data.forEach(function(bar, index) {
              var data = dataset.data[index];
              ctx.fillText(data, bar._model.x, bar._model.y - 5);
            });
          });
        }
      }
    }
  });
  return chart;
}
// 1, 2, 3 represent the differnt types of calculation (Pup,Pmid,Pdown)
function createResultsFromCSVTable(table,type) {

  if (table == null) {
    return null;
  }

  var rowsData = table.rows().data();
  var rows_results = []; var wrong_length = false;
  var wrong_type = false;
  
  Array.from(rowsData).forEach((function (row,index){

    if(type == 1 || type == 2){
      if(row.length != 3){
        wrong_length = true;
      }

      if(isNaN(parseFloat(row[1])) || isNaN(parseFloat(row[2]))){
        wrong_type = true
      }

      rows_results.push(parseFloat(row[2]) * parseFloat(row[2]));
    }

    if(type == 3){
      if(row.length != 4){
        wrong_length = true;
      }

      if(isNaN(parseFloat(row[1])) || isNaN(parseFloat(row[2])) || isNaN(parseFloat(row[3]) )){
        wrong_type = true
      }

      rows_results.push(parseFloat(row[1]) * parseFloat(row[2]) * parseFloat(row[3]));
    }
    
  }));

  // TODO: Possibly change the boolean variable with different error statusses
  if(wrong_length|| wrong_type){
    return null;
  }

  //Some ES6 magic to find the sum in one line (no for loops)
  var sum = (array) => array.reduce((a, b) => a + b, 0) 
  var result = sum(rows_results);

  // Round result to 2 decimal points
  result = Math.round((result + Number.EPSILON) * 100) / 100;

  return result;
  
}

function createResultsFromCustomTable(masses, emFactors, distances) {

  // console.log(metrics, countries, score, totalScore);

  var rows_results = [];
  var w_xmis = [];
  var wrong_type = false;
  
  if(masses == null || emFactors == null ){
    return null;
  }


  if(masses.length == 0 || emFactors.length == 0){
    return null;
  }


  if(distances != null && distances.length != 0){
    masses.forEach(function (mass, index) {
      if(isNaN(parseFloat(mass)) || isNaN(parseFloat(emFactors[index])) || isNaN(parseFloat(distances[index]) )){
        wrong_type = true
      }

      var rows_result = mass*emFactors[index]*distances[index];
      rows_results.push(rows_result);
    });
  }
  else{
    masses.forEach(function (mass, index) {
      if(isNaN(parseFloat(mass)) || isNaN(parseFloat(emFactors[index]))){
        wrong_type = true
      }

      var rows_result = mass*emFactors[index];
      rows_results.push(rows_result);
    });
  }

  if(wrong_type){
    return null;
  }

  //Some ES6 magic to find the average in one line (no for loops)
  var sum = (array) => array.reduce((a, b) => a + b, 0) 
  var result = sum(rows_results);

  // Round result to 2 decimal points
  result = Math.round((result + Number.EPSILON) * 100) / 100

  return result;

}

function updateChart(chart, indicators, resultsPup, resultsPMid, resultsPDown) {
  var dataset = [
    {
      label: indicators[0],
      backgroundColor: 'rgb(0, 128, 255)',
      borderColor: 'rgb(0, 128, 255)',
      data: [resultsPup.result1, resultsPup.result2]
    },
    {
      label: indicators[1],
      backgroundColor: 'rgb(0, 255, 0)',
      borderColor: 'rgb(0, 255, 0)',
      data: [resultsPMid.result1, resultsPMid.result2]
    },
    {
      label: indicators[2],
      backgroundColor: 'rgb(255,0,0)',
      borderColor: 'rgb(255,0,0)',
      data: [resultsPDown.result1, resultsPDown.result2]
    },
  ];
  chart.data.datasets = dataset;
  chart.update();
}

function createPDF(canvasImg, LifeExpectancyTableImg, equation, list) {
  
  // console.log(LifeExpectancyTableImg);

  if(! (Array.isArray(list) && list.length)){
    return null;
  }

  if(canvasImg == null || equation == null){
    return null;
  }

  // creates PDF from the img that the chart is converted to
  var doc = new jspdf.jsPDF();
  doc.setFontSize(11);

  var lMargin=15; //left margin in mm
  var rMargin=15; //right margin in mm
  var pdfInMM=210;  // width of A4 in mm

  var text = []
  for (var i in list) {
    
    // if(list[i] === "Name of the project, Name and Email:" || list[i] === "Phase 1. Goal and scope definition:" 
    // || list[i] === "Phase 2. Life cycle inventory (LCI):" || list[i] === "Phase 3. Life cycle impact assessment (LCIA):"){
    //   const textWidth = doc.getTextWidth(list[i]);
    //   text.push(doc.line(lMargin, 20, lMargin + textWidth, 20));
    // }
    text.push(list[i]);
  }

  // Wrap the text in the page's margnins defined above
  var lines = doc.splitTextToSize(text, (pdfInMM-lMargin-rMargin));
  // console.log('++++'+lines);
  var y_margin = 20;

  lines.forEach(line => {
    if(line === "Name of the project, Name and Email:" || line === "Phase 1. Goal and scope definition:" 
    || line === "Phase 2. Life cycle inventory (LCI):" || line === "Phase 3. Life cycle impact assessment (LCIA):"
    || line === "Results:" || line ==="Phase 4: Interpretation:"){
      var textWidth = doc.getTextWidth(line);
      doc.line(lMargin, y_margin+1, lMargin + textWidth, y_margin+1);
    }
    
    doc.text(lMargin,y_margin,line);
    y_margin+=10;

    if(line === "Phase 3. Life cycle impact assessment (LCIA):"){
      
      if(equation.length != 0){
        doc.text(equation, lMargin, y_margin+1);
        y_margin+=30;
      } 
    }
  });
  // doc.text(lMargin,20,lines);

  // Add the chart/plot      
  doc.addImage(canvasImg, 'JPEG', 20, 180, 160, 100, 'NONE');

  // Add the footer with the link to our tool
  doc.setFontSize(9);
  doc.text("Created using the IDeaL LCA Tool:", 10, 295);
  doc.textWithLink("https://webpages.uidaho.edu/ideal/lca.html", 62, 295, {url: "https://webpages.uidaho.edu/ideal/lca.html"});
  doc.setFontSize(11);
   
  // doc.addImage(LifeExpectancyTableImg, 'JPEG', 20, 100, 100, 80);

  doc.save('report.pdf');
}