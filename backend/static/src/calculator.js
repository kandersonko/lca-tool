
let chart;

const getFilename = (inputFile) => {
  return inputFile.value.split('\\').slice(-1)[0]
}

const getCSVFiles = (className) => {
  console.log("class name: ", className);
  if(className === "uploaded-csv") {
    return getFilesByClassname(className);

  }
  const csvFiles = Array.from(document.getElementsByClassName(className))
                        .map((el, index) => ({file_id: index, filename: getFilename(el), file: el.files[0]}))
                        .filter(el => el.filename !== '');
  return csvFiles;
}

const getFilesByClassname = (className) => {
  return Array.from(document.getElementsByClassName(className))
              .map((el, index) => {
                let filename = el;
                let file = null;
                if(Array.from(el.classList).includes('input-csv')) {
                  file = el.files[0];
                  filename = file ? file.name: '';
                }
                return ({file_id: index, filename: filename, file: file });
              });

}


function calculate(csvFiles, uploadedFiles) {

  let selectionFiles = getFilesByClassname("selection-csv");
  console.log("calculator files: ", selectionFiles);
  const processes = Array.from(document.getElementsByClassName("input-equation"))
                         .map((el, index) => {
                           let kind;
                           const name= el.children[0].value;
                           const equation= el.children[2].value;
                           let filename = el.children[1].value;
                           let file = csvFiles.find(f => f.filename === filename);
                           if(file) {
                             kind = 'file';
                             return ({
                               name: name,
                               filename: filename,
                               file_id: index,
                               file: file.file,
                               equation: equation,
                               kind: kind
                             });
                           }
                           file = uploadedFiles.find(f => f.filename === filename);
                           if(file) {
                             kind = 'csv';
                             return ({
                               name: name,
                               filename: filename,
                               file_id: index,
                               file: file,
                               equation: equation,
                               kind: kind
                             });
                           }
                           return ({});

                         });

  console.log("processes: ", processes, csvFiles, uploadedFiles);
  let files;

  const data = new FormData();
  data.append("processes", JSON.stringify(processes));
  processes.forEach(process => {
    if(process.kind === 'file')
      data.append(process.filename, process.file);
  })
  // data.append("files", JSON.stringify(files));
  // data.append("choice", upload_choice)
  // files.forEach(csv => {
  //   if(csv.filename )
  //   data.append(csv.filename, csv.file);
  // });

  console.log("data", data);

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
      let equations = [];
      let results = [];
      if(response.error) {
        $("#results").html(response.error);
      }
      if(response.processes) {
        response.processes.forEach((process, index) => {
          // Make the equation pretty-printed
          let equation  = process.equation.replaceAll(/\\\mathtt/g, '');
          equation = equation.replaceAll(/\\text/g, '');
          equation = equation.replaceAll(/{|}/g, '');
          equation = equation.replaceAll(/\\/g, '');
          equation = equation.replaceAll(/"/g, '');
          equation = equation.replaceAll(/\ /g, '\\ ');
          equation = equation.replace(/sum/g, "\\sum");

          console.log("equation: ", equation, index);
          // let formula = MathJax.tex2chtml(equation).outerHTML;
          // formula = MathJax.mathml2svg(formula).outerHTML;
          let formula = MathJax.tex2svg(equation).outerHTML;

          // console.log("formula: ", formula);
          const el_id = `equation_img_${index}`;
          const el_svg = `${el_id}_svg`;
          const el_img = `${el_id}_img`;
          output += `
          <div class="calculator-result flex flex-col justify-center items-center mb-3 border-x-4 border-gray-400 p-2">
            <h4 class="mr-2 font-medium">
              ${process.name}: <span class="font-bold">${process.result}</span>
            </h4>
            <div id="${el_svg}" class="output-equation flex justify-center">${formula}</div>
            <img id="${el_img}" class="text-center" alt="" src=""/>
          </div>`;
          results.push({name: process.name, value: process.result});
          const node = document.getElementById("results");
          MathJax.typesetPromise([node]).then(() => {
            $("#results").html(output);
            setTimeout(() => {

            let el = document.getElementById(el_svg);
            let svg = el.children[0].children[0];

            window.toPng({
              width: 16,
              height: 8,
              svg: svg.outerHTML
            }).then((pngUrl) => {
              // const img = document.querySelector('img')
              let img = document.getElementById(el_img)

              img.src = pngUrl
              el.remove();
              console.log("svg: ", svg, pngUrl, img);

            });
            }, 500);
          })
        });
        if(results.length > 0) {
          // const node = document.getElementById("results");
          // MathJax.typesetPromise([node]).then(() => {
          //   $("#results").html(output);
          //   let img_width =

          // });
          if(chartInitialized) {
            updateChart(chart, results);
          } else {
            chart = initializeChart(
              document.getElementById("myChart"),
              results
            )
          }
        }
      }

    },
    error: function(error){
      console.log("error", error);
      $("#results").html(error);
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

  $("#generateReport").click(async function () {

    // This fucntionality should be implemented using a Unit Testing framework
    //updateChart(chart, "Life Exprectancy", 1000000, 3000000);

    //Get the rest of the HTML elemensts here (name, scope, GWP etc.)


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

    // $('input:radio[name="methodCalculation"]:checked').each(function() {
    //   var idVal = $(this).attr("id");
    //   list.push($("label[for='"+idVal+"']").text());
    // });

    //creates image



    // Add the result
    list.push("Results:");

    // list.push($("#Result1").text());
    // list.push($("#Result2").text());
    // $("#results").each((_, el) => {
    //   list.push(el.innerHTML);
    // })

    // list.push($("#phase4Header").text());


    createPDF(list);
  });


  function createPDF(list) {

    // console.log(LifeExpectancyTableImg);

    if(! (Array.isArray(list) && list.length)){
      return null;
    }

    // if(canvasImg == null){
    //   return null;
    // }

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

    });

    // add the equations
    let margin_y = 80;
    let canvas_added = false;
    let alias = 0;
    $(".calculator-result").each(function(index) {
      // const img = document.querySelector('img')
      let title = this.children[0].innerText;
      let img = this.children[1];
      console.log("save pdf", img, margin_y);

      // doc.addSvgAsImage(svg, 1, 1, 100, 100, '', false);
      doc.text(20,margin_y,title);
      doc.addImage(img, 'png', 20, margin_y+3, 24, 8, `alias_${alias}`);
      margin_y += 20;
      alias += 1;
    });

    // Add the chart/plot
        // Get the canvas from the HTML
    let canvas = document.querySelector('#myChart');
    //creates image
    const canvasImg = canvas.toDataURL("image/png", 1.0);
    doc.addImage(canvasImg, 'JPEG', 20, 180, 160, 100, `alias_${alias+1}`);
    canvas_added = true;

    // Add the footer with the link to our tool
    doc.setFontSize(9);
    doc.text("Created using the LCA Tool:", 10, 295);
    doc.textWithLink("https://cycon.nkn.uidaho.edu", 62, 295, {url: "https://cycon.nkn.uidaho.edu"});
    doc.setFontSize(11);

    // doc.addImage(LifeExpectancyTableImg, 'JPEG', 20, 100, 100, 80);

    doc.save('report.pdf');
  }

});

let datatables = [];


function populateTable(dataSet, tableElement, tableId) {
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

    if(datatables[tableId]) {
      datatables[tableId].clear().draw();
      datatables[tableId].rows.add(data); // Add new data
      datatables[tableId].columns.adjust().draw(); // Redraw the DataTable
    } else {

      // We assign the above data and columns and some attributes to display on the table.
      datatables[tableId] =  tableElement.DataTable({
        retrieve: true,
        data: data,
        columns: columns,
        select: {
          style: 'single',
          items: 'row'
        },
      });
    }
    return datatables[tableId];
  }
}



// Method that reads and processes the selected file
function upload(evt, index, choice, filename, files) {
  console.log("upload:", index, choice, filename, files);
  if (!browserSupportFileUpload()) {
    alert('The File APIs are not fully supported in this browser!');
  }
  else {
    let data = null;
    let file;
    if(choice === 'Upload new CSV') {
      file = evt.target.files[0];
      console.log('csv file:', file);
      let reader = new FileReader();
      reader.readAsText(file);


      reader.onload = function (event) {
        var csvData = event.target.result;
        data = $.csv.toArrays(csvData);

        populateTable(data, $('#CSVtable_'+index), index);

      };
      reader.onerror = function () {
        alert('Unable to read ' + file.fileName);
      };
    }
    else {
      if(filename) {
        let csvFile = files.find(f => f.filename === filename)
        file = csvFile;
      } else {
        file = files[0];
      }
      // data = $.csv.toArrays(file.content);
      console.log("found file: ", file, file.content);

      populateTable(file.content, $('#CSVtable_'+index), index);
    }
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
