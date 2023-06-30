let chart;

const getFilename = (inputFile) => {
  return inputFile.value.split('\\').slice(-1)[0]
}

const getCSVFiles = (className) => {
  const csvFiles = Array.from(document.getElementsByClassName(className))
                        .map(el => ({filename: getFilename(el), file: el.files[0]}));
  return csvFiles;
}

function calculate(e) {

  const csvFiles = getCSVFiles("input-csv")
  console.log("csv files: ", csvFiles);
  const processes = Array.from(document.getElementsByClassName("input-equation"))
                         .map(el => {
                           return ({
                             name: el.children[0].value,
                             filename: el.children[1].value,
                             equation: el.children[2].value
                           });
                         });
  console.log("processes", processes);

  const data = new FormData();
  data.append("processes", JSON.stringify(processes));
  csvFiles.forEach(csv => {
    data.append(csv.filename, csv.file);
  })
  console.log("data", data)

  $.ajax({
    url: "/experiments/calculate",
    data: data,
    type: 'POST',
    dataType: 'json',
    processData: false, // important
    contentType: false, // important
    success: function(response){
      console.log("response", response);
      let output = "";
      let results = [];
      response.processes.forEach(process => {
        output += `
          <div class="calculator-result" class="flex flex-row mb-3">
            <h4 class="mr-2 font-medium">
              ${process.name}: <span class="font-bold">${process.result}</span>
              <span>| Formula: ${process.equation}</span>
            </h4>
          </div/>`;
        results.push({name: process.name, value: process.result});
      });
      if(results.length > 0) {
        $("#results").html(output);
        if(chartInitialized) {
          updateChart(chart, results);
        } else {
          chart = initializeChart(
            document.getElementById("myChart"),
            results
          )
        }
      }

    },
    error: function(error){
      console.log("error", error);
      $("#results").html("There is an error in your entries!");
    }
  });
}


const colors = ['rgb(0,128,255)', 'rgb(0,255,0)', 'rgb(255,0,0)', 'rgb(255,255,0)', 'rgb(255,51,153)',
                'rgb(0,0,153)', 'rgb(0,102,51)', 'rgb(51,0,25)', 'rgb(225,128,0)', 'rgb(0,0,0)'];

// convert results to datasets for chartjs
const convertToChartData = (results) => {
  return ({
    labels: results.map(row => row.name),
    datasets: [
      {
        data: results.map(row => row.value),
        backgroundColor: colors,
        borderColor: colors,
      }
    ]
  });
}

let chartInitialized = false;

const chartOptions = {
  scales: {
    yAxes: [{
      ticks: {
        beginAtZero: true,
        min: 0
      }
    }]
  },
  legend: {
    display: false //This will do the task
  }
};

function initializeChart(ctx, results) {

  chartInitialized = true;
  let newChart = new Chart(
    ctx,
    {
      type: 'bar',
      data: convertToChartData(results),
      options: chartOptions,
      // options: chartOptions,
    }
  );
  // newChart.options = chartOptions;
  // newChart.update();
  return newChart;
}

function updateChart(chart, results) {

  const data = convertToChartData(results);

  chart.data = data;
  chart.update();
}

$(document).ready(function () {

  let customTable_1 = $('#customTable_1').dataTable();

  $("#generateReport").click(async function () {

    // This fucntionality should be implemented using a Unit Testing framework
    //updateChart(chart, "Life Exprectancy", 1000000, 3000000);

    //Get the rest of the HTML elemensts here (name, scope, GWP etc.)

    // Get the canvas from the HTML
    var canvas = document.querySelector('#myChart');
    //creates image
    var canvasImg = canvas.toDataURL("image/png", 1.0);

    // We add all the info into one list in order to put them into the pdf
    var list = [];
    // Add the info
    list.push($("#infoHeader").text());
    list.push($("#projectName").val());


    // Add the description
    list.push($("#scopeHeader").text());

    list.push($("textarea#phase1Text").val());



    // Add the selected equation
    list.push($("#methodHeader").text());
    //list.push($('input:radio[name="methodCalculation"]:checked').text());

    $('input:radio[name="methodCalculation"]:checked').each(function() {
      var idVal = $(this).attr("id");
      list.push($("label[for='"+idVal+"']").text());
    });

    var equation_image = null;


    // Add the result
    list.push("Results:");

    // list.push($("#Result1").text());
    // list.push($("#Result2").text());
    $(".calculator-result").each((_, el) => {
      list.push(el.innerText);
    })

    list.push($("#phase4Header").text());


    createPDF(canvasImg, null, equation_image, list);
  });


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
      if(line === "Name of the project" || line === "Goal and scope"
         || line === "Life cycle impact assessment (LCIA)" || line === "Results:"){
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
    doc.textWithLink("https://cycon.nkn.uidaho.edu", 62, 295, {url: "https://cycon.nkn.uidaho.edu"});
    doc.setFontSize(11);

    // doc.addImage(LifeExpectancyTableImg, 'JPEG', 20, 100, 100, 80);

    doc.save('report.pdf');
  }
})



function populateTable(dataSet, tableElement) {
  if (typeof (dataSet[0]) === 'undefined') {
    return null;
  }
  else {
    var columns = [];
    var data = [];
    $.each(dataSet, function (index, row) {

      // The first row of the csv data is going to be represent each column in our HTML table
      if (index == 0) {
        $.each(row, function (index, colData) {
          columns.push({ title: colData });
        });
      } // Then we just have the rest of the data
      else {
        data.push(row);
      }

    });


    // We assign the above data and columns and some attributes to display on the table.
    return tableElement.DataTable({
      data: data,
      columns: columns,
      select: {
        style: 'single',
        items: 'row'
      },
    });
  }
}



// Method that reads and processes the selected file
function upload(evt, index) {
  if (!browserSupportFileUpload()) {
    alert('The File APIs are not fully supported in this browser!');
  }
  else {
    var data = null;
    var file = evt.target.files[0];
    var reader = new FileReader();
    reader.readAsText(file);

    var uploadId = index;

    reader.onload = function (event) {
      var csvData = event.target.result;
      data = $.csv.toArrays(csvData);

      populateTable(data, $('#CSVtable_'+index));

    };
    reader.onerror = function () {
      alert('Unable to read ' + file.fileName);
    };
  }
}

// TODO: Add the rest of the events here, pass the ID of the csv somehow (see this.id) and then convert the addNewProcessButton2
// to have the appropriate button ID and to call the same fucntion based on the if statements

// Method that checks that the browser supports the HTML5 File API
function browserSupportFileUpload() {
  var isCompatible = false;
  if (window.File && window.FileReader && window.FileList && window.Blob) {
    isCompatible = true;
  }
  return isCompatible;
}
