let processCount = 0;

let chart;

function calculate(e) {

  const inputEquations = document.getElementsByClassName("input-equation");
  const equations = Array.from(inputEquations)
                         .filter(x => x.children[1].value !== '')
                         .map(x => ({"equation": x.children[1].value, "name": x.children[0].value}));
  console.log("equations: ", equations, inputEquations);
  const csvFile = $("#txtFileUpload_1")[0].files[0];
  console.log("csv: ", csvFile)
  const data = new FormData();
  data.append("csv_file", csvFile);
  data.append("equations", JSON.stringify(equations));
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
      const name = response.name;
      let output = "";
      let results = [];
      for (const [name, equation] of Object.entries(response.results)) {
        output += `<div class="calculator-result" class="flex flex-row mb-2"><h4 class="mr-2 font-medium"><h4>${name}: <span class="font-bold">${equation}</span></h4> </div/>`;
        results.push({name: name, value: equation})
      }
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


function addEquation() {
  const equationPlaceholder = document.getElementById("lca_equation");
  const equation = `
            <div class="input-equation flex items-center mb-2">
                <input type="text" name="label" class="py-1 px-2 border border-gray-400 rounded-lg" value="Process ${processCount}" placeholder="Rename Process 1" style="margin-right: .5rem;">
                <textarea class="py-1 px-2 border border-gray-400 rounded-lg" rows="1" cols="30" value="" placeholder="Enter the equation" style="margin-right: .5rem"></textarea> <br />
            </div>
    `
  $(equation).insertBefore(equationPlaceholder);
}

function  addNewProcessCSV() {
  if(processCount < 4){
    processCount = processCount + 1;
    const output = `
            <label id="processCount2_1"> Processes: ${processCount}/4 </label>
        `
    $("#processCount2_1").replaceWith(output)

    addEquation()
  }
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
    doc.textWithLink("https://cycon.nkn.uidaho.edu", 62, 295, {url: "https://cycon.nkn.uidaho.edu"});
    doc.setFontSize(11);

    // doc.addImage(LifeExpectancyTableImg, 'JPEG', 20, 100, 100, 80);

    doc.save('report.pdf');
  }
})
