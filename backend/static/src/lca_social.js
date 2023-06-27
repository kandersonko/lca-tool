// Maybe we need this to be an array if we have multiple results for Life Excpectancy, Health etc.
var resultProcess1 = 0;
var resultProcess2 = 0;


function checkCSVHeaderSocial(data){ 
  
  if(data.length == 0){
    return false;
  }

  if(data[0].length != 5){
    return false;
  }

  if(data[0][0] !== "Indicator" || data[0][1] !== "Metric" || data[0][2] !== "Location" || data[0][3] !== "Score" || data[0][4] !== "Total Score"){  
    return false;
  }
  
  return true;
  
}

function checkCSVHeaderEconomic(data,type){ 
  
  if(data.length == 0){
    return false;
  }

  if(data[0].length != 5){
    return false;
  }

  if(type == 1 && (data[0][0] !== "Indicator" || data[0][1] !== "Metric" || data[0][2] !== "Location" || data[0][3] !== "Mass" || data[0][4] !== "Cost")){  
    return false;
  }
  
  // if(type == 2 && (data[0][0] !== "Indicator" || data[0][1] !== "Raw Material Mass" || data[0][2] !== "Production Cost")){  
  //   return false;
  // }

  // if(type == 3 && (data[0][0] !== "Indicator" || data[0][1] !== "Final Product Mass" || data[0][2] !== "Distribution Cost")){  
  //   return false;
  // }
  
  return true;
  
}

function checkCSVHeaderEnvironmental(data,type){ 
  
  if(data.length == 0){
    return false;
  }

  if(type == 1 &&  data[0].length != 3 && (data[0][0] !== "Indicator" || data[0][1] !== "Metric" || data[0][2] !== "Location" || data[0][3] !== "Mass" || data[0][4] !== "Emission Factor")){  
    return false; 
  }
  
  if(type == 2 && data[0].length != 3 && (data[0][0] !== "Indicator" || data[0][1] !== "Metric" || data[0][2] !== "Location" || data[0][3] !== "Mass" || data[0][4] !== "Emission Factor")){  
    return false; 
  }

  if(type == 3 && data[0].length != 4 && (data[0][0] !== "Indicator"  || data[0][1] !== "Metric" || data[0][2] !== "Location" || data[0][3] !== "Mass" || data[0][4] !== "Emission Factor" || data[0][5] !== "Distance")){  
    return false; 
  }
  
  return true;
  
}
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = initializeChart(ctx);

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

function updateChart(chart, results) {
  
  
  var dataset = [];

  var colors = ['rgb(0,128,255)', 'rgb(0,255,0)', 'rgb(255,0,0)', 'rgb(255,255,0)', 'rgb(255,51,153)', 
                'rgb(0,0,153)', 'rgb(0,102,51)', 'rgb(51,0,25)', 'rgb(225,128,0)', 'rgb(0,0,0)'];
  results.forEach(function (result, index){
    var obj = {
      label: result.indicator,
      backgroundColor: colors[index],
      borderColor: colors[index],
      data: [result.result1, result.result2]
    };
    dataset.push(obj);
  });

  chart.data.datasets = dataset;
  chart.update();
}

function createResultsFromCSVTableSocial(table) {

  if (table == null) {
    return null;
  }

  var rowsData = table.rows().data();
  var w_xmis = []; 
  var wrong_length = false;
  var wrong_type = false;

  var indicator = "";
  
  Array.from(rowsData).forEach((function (row,index){
    // if we find the indicator we assign it and return it
       
    if(row[0] !== ""){
      indicator = row[0];
    }

    if(row.length != 5){
      wrong_length = true;
    }

    if(isNaN(parseFloat(row[3])) || isNaN(parseFloat(row[4]))){
      wrong_type = true;
    }

    w_xmis.push((parseFloat(row[3])/parseFloat(row[4]))*parseFloat(row[3]));
  }));

  // TODO: Possibly change the boolean variable with different error statusses
  if(wrong_length|| wrong_type){
    return null;
  }

  //Some ES6 magic to find the average in one line (no for loops) to get: Sum of number of metrics * sum of number of locations * weight_i(x_mi)/number_of_metrics
  var average = (array) => array.reduce((a, b) => a + b) / w_xmis.length; 
  var result = average(w_xmis);

  // Round result to 2 decimal points
  result = Math.round((result + Number.EPSILON) * 100) / 100;

  return {indicator, result};
  
}

function createResultsFromCSVTableEconomic(table) {

  if (table == null) {
    return null;
  }

  //TODO: Change this to the original file
  var rowsData = table.rows().data();

  var rows_results = []; 
  var wrong_length = false;
  var wrong_type = false;

  var indicator= "";
  
  Array.from(rowsData).forEach((function (row,index){

    if(row[0] !== ""){
      indicator = row[0];
    }

    if(row.length != 5){
      wrong_length = true;
    }

    if(isNaN(parseFloat(row[3])) || isNaN(parseFloat(row[4]))){
      wrong_type = true;
    }

    rows_results.push((parseFloat(row[3]) * parseFloat(row[4])));
  }));

  // TODO: Possibly change the boolean variable with different error statusses
  if(wrong_length|| wrong_type){
    return null;
  }

  //Some ES6 magic to find the sum in one line 
  var sum = (array) => array.reduce((a, b) => a + b, 0) 
  var result = sum(rows_results);

  // Round result to 2 decimal points
  result = Math.round((result + Number.EPSILON) * 100) / 100;

  return {indicator, result};
  
}

function createResultsFromCSVTableEnvironmental(table,type) {

  if (table == null) {
    return null;
  }

  //TODO: Change this to the original file
  var rowsData = table.rows().data();

  // var rowsData = table.rows().data();
  var rows_results = []; 
  var wrong_length = false;
  var wrong_type = false;

  var indicator = "";
  
  Array.from(rowsData).forEach((function (row,index){

    if(row[0] !== ""){
      indicator = row[0];
    }

    if(type == 1 || type == 2){
      if(row.length != 5){
        wrong_length = true;
      }

      if(isNaN(parseFloat(row[3])) || isNaN(parseFloat(row[4]))){
        wrong_type = true;
      }

      rows_results.push(parseFloat(row[3]) * parseFloat(row[4]));
    }

    if(type == 3){      
      if(row.length != 6){
        wrong_length = true;
      }

      if(isNaN(parseFloat(row[3])) || isNaN(parseFloat(row[4])) || isNaN(parseFloat(row[5]) )){
        wrong_type = true;
      }

      rows_results.push(parseFloat(row[3]) * parseFloat(row[4]) * parseFloat(row[5]));      
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

  return {indicator, result};
  
}

function createResultsFromCustomTableSocial(metrics, countries, score, totalScore) {

  // console.log(metrics, countries, score, totalScore);

  var weights = [];
  var w_xmis = [];
  
  if(metrics == null || score == null || totalScore == null){
    return null;
  }

  if(metrics == 0 || score.length == 0 || totalScore.length == 0){
    return null;
  }

  for (var index=0 ; index<metrics; index++){

    if(isNaN(score[index]) || isNaN(totalScore[index])){
      return null;
    }

    var weight = score[index]/totalScore[index];
    weights.push(weight);
  }

  weights.forEach(function (weight, index) {
    var w_xmi = weights[index]*score[index];
    w_xmis.push(w_xmi);
  });

  //Some ES6 magic to find the average in one line (no for loops)
  var average = (array) => array.reduce((a, b) => a + b) / w_xmis.length; 
  var result = average(w_xmis);

  // Round result to 2 decimal points
  result = Math.round((result + Number.EPSILON) * 100) / 100

  return result;

}

function createResultsFromCustomTableEconomic(masses, costs) {

  // console.log(metrics, countries, score, totalScore);

  var rows_results = [];
  var w_xmis = [];
  var wrong_type = false;
  
  if(masses == null || costs == null ){
    return null;
  }

  if(masses.length == 0 || costs.length == 0){
    return null;
  } 
 
  masses.forEach(function (mass, index) {

    if(isNaN(parseFloat(mass)) || isNaN(parseFloat(costs[index]))){
      wrong_type = true
    }

    var rows_result = mass*costs[index];
    rows_results.push(rows_result);
  });

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

function createResultsFromCustomTableEnvironmental(masses, emFactors, distances) {

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
 
  if(distances != null && distances.length != 0 && distances.every(i => (i !== ""))){
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

function createPDF(canvasImg, LifeExpectancyTableImg, equation, list) {
  
  // console.log(LifeExpectancyTableImg);

  if(! (Array.isArray(list) && list.length)){
    return null;
  }

  if(canvasImg == null){
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

    // if(line === "Phase 3. Life cycle impact assessment (LCIA):"){
      
    //   if(equation_image!=null){
    //     doc.addImage(equation_image, 'JPEG', lMargin, y_margin+1, 40, 22);
    //     y_margin+=30;
    //   } 
    // }
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
