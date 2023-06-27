
$(document).ready(function () {

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

  var tableLifeExpectancy = null;
  var tableHealth = null;
  var tableEducation = null;
  var tableSafety = null;

  var tables = [];

  var selectedMethodId = null;

  var customTables = [];

  var customTable_1 = $('#customTable_1').dataTable();
  customTables.push(customTable_1);


  var ctx = document.getElementById('myChart').getContext('2d');
  var chart = initializeChart(ctx);

  //Initialize an array with same objects but differnt id
  var results = new Array(10).fill().map((_, i) => ({ id: i, indicator:"",
                                                     result1 : 0,
                                                     result2 : 0,
                                                     error : null })
                                        );

  var resultsLifeExpectancy = {
    result1 : 0,
    result2 : 0,
    error : null
  };
  var resultsEducation = {
    result1 : 0,
    result2 : 0,
    error : null
  };
  var resultsHealth = {
    result1 : 0,
    result2 : 0,
    error : null
  };
  var resultsSafety = {
    result1 : 0,
    result2 : 0,
    error : null
  };

  var readyTablesCounter = 1;
  $("#addCSVUpload").on('click', function () {

    // If the previous table element is empty clone it and add it
    if(readyTablesCounter != 10 && ($("#CSVtable_" + readyTablesCounter+" tr").length == 0)){

      var el = $("#readyTableDiv_"+readyTablesCounter).clone().attr('id', 'readyTableDiv_' + ++readyTablesCounter).appendTo("#readyTables");
      // Fing all child elements and change their ID
      el.find("[id]").add(el).each(function() {
        // Remove the trailing one and replace it with the counter
        this.id = this.id.slice(0, -1) + readyTablesCounter;
      });

      $("#legend_"+readyTablesCounter).text("Upload your CSV File for indicator "+readyTablesCounter);

      // Add the required event to populate the table
      $('#txtFileUpload_'+readyTablesCounter).on('change', upload);

      $("#addNewProcessButton2_"+readyTablesCounter).on('click', addNewProcessCSV);
      // console.log(results);
      // Add a new table variable for each new CSV table

    }
  });

  $("#addCustomTable").on("click", function() {
    if($('input:radio[name="method"]:checked').val() == "socialMethod" && (methodLocked !=2 || methodLocked !=3)){
      $('#csvTableErrorMessage_2').text("");
      createNewTable("socialMethod");
    }
    else if ($('input:radio[name="method"]:checked').val() == "economicMethod" && (methodLocked !=1 || methodLocked !=3)){
      $('#csvTableErrorMessage_2').text("");
      createNewTable("economicMethod");
    }
    else if ($('input:radio[name="method"]:checked').val() == "environmentalMethod" && (methodLocked !=1 || methodLocked !=2)){
      $('#csvTableErrorMessage_2').text("");
      createNewTable("environmentalMethod");
    }
    else{
      $('#csvTableErrorMessage_2').text("You must select an objective in Phase 1 first");
    }
  });

  $('input:radio[name="databaseMethod"]').click(
    function () {

      if (this.value == 'createDatabase') {
        $("#customTables").css("display", "block");

        $("#readyTables").css("display", "none");

        resultsLifeExpectancy.result1 = 0;
        resultsLifeExpectancy.result2 = 0;
        resultsLifeExpectancy.error = null;

        resultsEducation.result1 = 0;
        resultsEducation.result2 = 0;
        resultsEducation.error = null;

        resultsHealth .result1 = 0;
        resultsHealth.result2 = 0;
        resultsHealth.error = null;

        resultsSafety.result1 = 0;
        resultsSafety.result2 = 0;
        resultsSafety.error = null;

      }
      if (this.value == 'importDatabase') {
        $("#readyTables").css("display", "block");

        $("#customTables").css("display", "none");

        resultsLifeExpectancy.result1 = 0;
        resultsLifeExpectancy.result2 = 0;
        resultsLifeExpectancy.error = null;

        resultsEducation.result1 = 0;
        resultsEducation.result2 = 0;
        resultsEducation.error = null;

        resultsHealth .result1 = 0;
        resultsHealth.result2 = 0;
        resultsHealth.error = null;

        resultsSafety.result1 = 0;
        resultsSafety.result2 = 0;
        resultsSafety.error = null;
      }
    }
  );

  $('input:radio[name="methodCalculation"]').click (
    function(){
      var selectedMethod = $('input:radio[name="method"]:checked').next('label:first').text();

      var finalString1 = "<p id='Result1'>Case Study Result for "+selectedMethod+" method: <br>";
      var finalString2 = "<p id='Result2'>Proposed Study Result for "+selectedMethod+" method: <br>";

      results.forEach(function (result, index){

        // Add only the results that are not zero and have an indicator
        if(result.indicator && result.result1 !== 0 && result.result1 !== 1){
          finalString1 += result.indicator+": <i> "+ result.result1 + " </i>";
          finalString2 += result.indicator+": <i> "+ result.result2 + " </i>";
        }

        if(index == 9){
          finalString1 += "</i></p>";
          finalString2 += "</i></p>";
        }

      });

      $('#Result1').replaceWith(finalString1);
      $('#Result2').replaceWith(finalString2);

      let indicators = results.map(result => result.indicator);

      // updateChart(chart, label, results.result1, results.result2);
      updateChart(chart, results);
    }
  );

  $('input:radio[name="method"]').click(
    function () {
      if (this.value == "socialMethod" && customTablesCounter == 1 && (methodLocked !=2 || methodLocked !=3)){
        methodLocked = 1;
        createNewTable("socialMethod");
      }
      else if (this.value == "economicMethod" && customTablesCounter == 1 && (methodLocked !=1 || methodLocked !=3)){
        methodLocked = 2;
        createNewTable("economicMethod");
      }
      else if (this.value == "environmentalMethod" && customTablesCounter == 1 && (methodLocked !=1 || methodLocked !=2)){
        methodLocked = 3;
        createNewTable("environmentalMethod");
      }
    }
  );


  var customTablesCounter = 1;
  var methodLocked = 0;
  function createNewTable(method){
    // Here we do not need to have the previous elements empty, we can clone them anyways, it speeds up the creation of new tables
    if(customTablesCounter != 10){

      addTable(customTablesCounter, method);

      // $('#customTable_'+customTablesCounter).destroy();
      var newCustomTable = $('#customTable_'+customTablesCounter).dataTable();
      customTables.push(newCustomTable);

      $("#addButton_"+customTablesCounter).on('click', function() {
        addRows(newCustomTable,method);
      });

      $("#addNewProcessButton1_"+customTablesCounter).on('click', addNewProcessCustomTable);

      customTablesCounter++;
    }
  }

  // Here based on the button click we perform the corresponding calculation and store the values
  function addNewProcessCSV(evt) {

    var buttonId = this.id;

    var el_number = buttonId.slice(buttonId.length - 1);
    // selectedMethodId = $(this).attr("id");

    $("#csvTableErrorMessage").text("");


    //Make these functions more generic (have all the checks etc and before and call only the function based on the user's selection)
    if($('input:radio[name="method"]:checked').val() == "socialMethod"){

      if (tables[el_number-1] != null && typeof tables[el_number-1] !== 'undefined') {
        if (results[el_number-1].result1 == 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = createResultsFromCSVTableSocial(tables[el_number-1]);
          results[objIndex].indicator = values.indicator;
          results[objIndex].result1 = values.result;

          $("#processCount2_"+el_number).replaceWith("<label id='processCount2_"+el_number+"''> Processes: 1/2 </label>");
          return;
        }

        if (results[el_number-1].result1 != 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = createResultsFromCSVTableSocial(tables[el_number-1]);
          results[objIndex].indicator = values.indicator;
          results[objIndex].result2 = values.result;

          $("#processCount2_"+el_number).replaceWith("<label id='processCount2_"+el_number+"''> Processes: 2/2 </label>");
          return;
        }


      }
    }
    if($('input:radio[name="method"]:checked').val() == "economicMethod"){

      if (tables[el_number-1] != null && typeof tables[el_number-1] !== 'undefined') {
        if (results[el_number-1].result1 == 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = createResultsFromCSVTableEconomic(tables[el_number-1]);
          results[objIndex].indicator = values.indicator;
          results[objIndex].result1 = values.result;

          $("#processCount2_"+el_number).replaceWith("<label id='processCount2_"+el_number+"''> Processes: 1/2 </label>");
          return;
        }

        if (results[el_number-1].result1 != 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = createResultsFromCSVTableEconomic(tables[el_number-1]);
          results[objIndex].indicator = values.indicator;
          results[objIndex].result2 = values.result;

          $("#processCount2_"+el_number).replaceWith("<label id='processCount2_"+el_number+"''> Processes: 2/2 </label>");
          return;
        }



      }
    }
    else if($('input:radio[name="method"]:checked').val() == "environmentalMethod"){

      if (tables[el_number-1] != null && typeof tables[el_number-1] !== 'undefined') {
        if (results[el_number-1].result1 == 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var type = 1;
          var tempTable = tables[el_number-1];

          if(tempTable.columns().nodes().length == 6 && $(tempTable.column(5).header()).html() === "Distance"){
            type = 3;
          }

          var values = createResultsFromCSVTableEnvironmental(tables[el_number-1], type);
          results[objIndex].indicator = values.indicator;
          results[objIndex].result1 = values.result;

          $("#processCount2_"+el_number).replaceWith("<label id='processCount2_"+el_number+"''> Processes: 1/2 </label>");
          return;
        }

        if (results[el_number-1].result1 != 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var type = 1;
          var tempTable = tables[el_number-1];
          if(tempTable.columns().nodes().length == 6 && $(tempTable.column(5).header()).html() === "Distance"){
            type = 3;
          }

          var values = createResultsFromCSVTableEnvironmental(tables[el_number-1], type);
          results[objIndex].indicator = values.indicator;
          results[objIndex].result2 = values.result;

          $("#processCount2_"+el_number).replaceWith("<label id='processCount2_"+el_number+"''> Processes: 2/2 </label>");
          return;
        }


      }
    }

  }

  // This function should be for the manually populated table
  function addNewProcessCustomTable (evt) {
    var buttonId = this.id;

    var el_number = buttonId.slice(buttonId.length - 1);

    if($('input:radio[name="method"]:checked').val() == "socialMethod"){
      // if ($(this).attr("id") === 'addNewProcessButton1LifeExpectancy' && customTableLifeExpectancy != null) {
      var metric_elements =$('#customTable_'+el_number+' tbody .metric');
      var location_elements =$('#customTable_'+el_number+' tbody .location');
      var score_elements = $('#customTable_'+el_number+' tbody .score');
      var totalScore_elements = $('#customTable_'+el_number+' tbody .totalScore');

      var elements = [metric_elements, location_elements, score_elements, totalScore_elements];

      var indicator = $('#customTableDiv_'+el_number+' .indicator')[0].value;

      if (customTables[el_number-1] != null && typeof customTables[el_number-1] !== 'undefined') {

        if (results[el_number-1].result1 == 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = getResultsSocial(location_elements, metric_elements, score_elements, totalScore_elements);
          results[objIndex].indicator = indicator;
          results[objIndex].result1 = values;

          $("#processCount_"+el_number).replaceWith("<label id='processCount_"+el_number+"''> Processes: 1/2 </label>");

          exportTableToCSV(results[objIndex].indicator, results[objIndex].indicator+'_Process1.csv',
                           el_number, 1, elements);
          return;
        }

        if (results[el_number-1].result1 != 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = getResultsSocial(location_elements, metric_elements, score_elements, totalScore_elements);
          results[objIndex].indicator = indicator;
          results[objIndex].result2 = values;

          $("#processCount_"+el_number).replaceWith("<label id='processCount_"+el_number+"''> Processes: 2/2 </label>");

          $("#exportDatabase_"+el_number).click(function(){exportTableToCSV(results[objIndex].indicator, results[objIndex].indicator+'_Process2.csv',
                                                                            el_number, 2, elements)});
          $("#exportDatabase_"+el_number).css("display", "block");
          return;
        }


      }
    }

    if($('input:radio[name="method"]:checked').val() == "economicMethod"){

      var metric_elements =$('#customTable_'+el_number+' tbody .metric');
      var location_elements =$('#customTable_'+el_number+' tbody .location');
      var mass_elements =$('#customTable_'+el_number+' tbody .mass');
      var cost_elements =$('#customTable_'+el_number+' tbody .cost');

      var elements = [metric_elements, location_elements, mass_elements, cost_elements];

      var indicator = $('#customTableDiv_'+el_number+' .indicator')[0].value;

      if (customTables[el_number-1] != null && typeof customTables[el_number-1] !== 'undefined') {

        if (results[el_number-1].result1 == 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = getResultsEconomic(mass_elements, cost_elements);
          results[objIndex].indicator = indicator;
          results[objIndex].result1 = values;

          $("#processCount_"+el_number).replaceWith("<label id='processCount_"+el_number+"''> Processes: 1/2 </label>");

          exportTableToCSVEconomic(results[objIndex].indicator, results[objIndex].indicator+'_Process1.csv',
                                   el_number, 1, elements);
          return;
        }

        if (results[el_number-1].result1 != 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = getResultsEconomic(mass_elements, cost_elements);
          results[objIndex].indicator = indicator;
          results[objIndex].result2 = values;

          $("#processCount_"+el_number).replaceWith("<label id='processCount_"+el_number+"''> Processes: 2/2 </label>");

          $("#exportDatabase_"+el_number).click(function(){exportTableToCSVEconomic(results[objIndex].indicator, results[objIndex].indicator+'_Process2.csv',
                                                                                    el_number, 2, elements)});
          $("#exportDatabase_"+el_number).css("display", "block");
          return;
        }
      }
    }

    if($('input:radio[name="method"]:checked').val() == "environmentalMethod"){

      var metric_elements =$('#customTable_'+el_number+' tbody .metric');
      var location_elements =$('#customTable_'+el_number+' tbody .location');
      var mass_elements =$('#customTable_'+el_number+' tbody .mass');
      var emFactor_elements =$('#customTable_'+el_number+' tbody .emissionFactor');
      var distance_elements =$('#customTable_'+el_number+' tbody .distance');

      var indicator = $('#customTableDiv_'+el_number+' .indicator')[0].value;

      var elements = [metric_elements, location_elements, mass_elements, emFactor_elements, distance_elements];

      if (customTables[el_number-1] != null && typeof customTables[el_number-1] !== 'undefined') {

        if (results[el_number-1].result1 == 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = getResultsEnvironmental(mass_elements, emFactor_elements, distance_elements);
          results[objIndex].indicator = indicator;
          results[objIndex].result1 = values;

          // console.log(distance_elements);
          var type = 1;
          distance_elements.each(function () {
            if($(this).val() !== null){
              type = 3;
            }
          });

          $("#processCount_"+el_number).replaceWith("<label id='processCount_"+el_number+"''> Processes: 1/2 </label>");

          exportTableToCSVEnvironmental(results[objIndex].indicator, results[objIndex].indicator+'_Process1.csv',
                                        el_number, 1, type, elements);
          return;
        }

        if (results[el_number-1].result1 != 0 && results[el_number-1].result2 == 0) {

          var objIndex = results.findIndex((obj => obj.id == el_number-1));

          var values = getResultsEnvironmental(mass_elements, emFactor_elements, distance_elements);
          results[objIndex].indicator = indicator;
          results[objIndex].result2 = values;

          var type = 1;
          distance_elements.each(function () {
            if($(this).val() !== null){
              type = 3;
            }
          });

          $("#processCount_"+el_number).replaceWith("<label id='processCount_"+el_number+"''> Processes: 2/2 </label>");

          $("#exportDatabase_"+el_number).click(function(){exportTableToCSVEnvironmental(results[objIndex].indicator, results[objIndex].indicator+'_Process2.csv',
                                                                                         el_number, 2, type, elements)});
          $("#exportDatabase_"+el_number).css("display", "block");
          return;
        }
      }
    }
  }

  function getResultsSocial(location_elements, metric_elements, score_elements, totalScore_elements){
    // selectedMethodId = "Social Analysis Method";

    var metrics = 0;
    metric_elements.each(function () {
      metrics++;
    });

    var location = [];
    location_elements.each(function () {
      location.push($(this).val());
    });

    var score = [];
    score_elements.each(function () {
      score.push($(this).val());
    });

    var totalScore = [];
    totalScore_elements.each(function () {
      totalScore.push($(this).val());
    });

    return createResultsFromCustomTableSocial(metrics, location, score, totalScore);
  }

  function getResultsEconomic(mass_elements, cost_elements){
    var masses = [];

    mass_elements.each(function () {
      masses.push($(this).val());
    });

    var costElements = [];
    cost_elements.each(function () {
      costElements.push($(this).val());
    });

    return createResultsFromCustomTableEconomic(masses, costElements);
  }

  function getResultsEnvironmental(mass_elements, emFactor_elements, distance_elements){
    var masses = [];
    mass_elements.each(function () {
      masses.push($(this).val());
    });

    var emFactors = [];
    emFactor_elements.each(function () {
      emFactors.push($(this).val());
    });

    var distances = [];
    if(distance_elements != null){
      distance_elements.each(function () {
        distances.push($(this).val());
      });
    }

    return createResultsFromCustomTableEnvironmental(masses, emFactors, distances);
  }

  // The event listener for the file uploads
  document.getElementById('txtFileUpload_1').addEventListener('change', upload, false);
  document.getElementById('addNewProcessButton2_1').addEventListener('click', addNewProcessCSV, false);

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

  function addRows(customTable, method){
    if (method == 'socialMethod') {
      customTable.dataTable().fnAddData([
        "",
        "<input id='metric' type='text' name='metric' placeholder='Metric' class='metric' />",
        "<input id='location' type='text' name='location' placeholder='Location' class='location' />",
        "<input id='score' type='text' name='score' placeholder='Score' class='score' />",
        "<input id='totalScore' type='text' name='totalScore' placeholder='Total Score' class='totalScore' />"
      ]);
    }
    else if (method == 'economicMethod') {
      customTable.dataTable().fnAddData([
        "",
        "<input id='metric' type='text' name='metric' placeholder='Metric' class='metric' />",
        "<input id='location' tpe='text' name='location' placeholder='Location' class='location' />",
        "<input id='mass' type='text' name='mass' placeholder='Mass' class='mass'/>",
        "<input id='cost' type='text' name='cost' placeholder='Cost' class='cost' />"
      ]);
    }
    else if (method == 'environmentalMethod') {
      customTable.dataTable().fnAddData([
        "",
        "<input id='metric' type='text' name='metric' placeholder='Metric' class='metric' />",
        "<input id='location' tpe='text' name='location' placeholder='Location' class='location' />",
        "<input id='mass' type='text' name='mass' placeholder='Mass' class='mass'/>",
        "<input id='emissionFactor' type='text' name='emissionFactor' placeholder='Emission Factor' class='emissionFactor' />",
        "<input id='distance' type='text' name='distance' placeholder='Distance' class='distance' />"
      ]);
    }
  }

  function addTable(number, method){
    var newTable =  document.createElement('div');
    if (method == 'socialMethod') {

      // TODO: Must remove all the previous tables first and reset the counter
      newTable.innerHTML =
        '<div id="customTableDiv_'+number+'" style="display: block;">'+
        '<table id="customTable_'+number+'" style="table-layout:fixed; width: 100%;">'+
        '<thead>'+
        '<tr>'+
        '<th>Indicator</th>'+
        '<th>Metric</th>'+
        '<th>Location</th>'+
        '<th>Score</th>'+
        '<th>Total Score</th>'+
        '</tr>'+
        '<thead>'+
        '<tbody>'+
        '<tr>'+
        '<td>'+
        '<input id="indicator" type="text" name="indicator" placeholder="Indicator" class="indicator"/>'+
        '</td>'+
        '<td><input id="metric" type="text" name="metric" placeholder="Metric" class="metric"/></td>'+
        '<td><input id="location" type="text" name="location" placeholder="Location" class="location" /></td>'+
        '<td><input id="score" type="text" name="score" placeholder="score" class="score" /></td>'+
        '<td><input id="totalScore" type="text" name="totalScore" placeholder="Total Score" class="totalScore" /></td> '+
        '</tr>'+
        '</tbody>'+
        '</table>'+
        '<input id="addButton_'+number+'" type="button" value="Add new record" class="addButton"/>'+
        '<input id="addNewProcessButton1_'+number+'" type="button" value="Add new process" class="addNewProcessButton1"/>'+
        '<label id="processCount_'+number+'"> Processes: 0/2 </label>'+
        '<label id="customTableErrorMessage_'+number+'" value="" style="color:red"></label>'+
        '<br>'+
        '<input id="exportDatabase_'+number+'" value="Export as CSV" type="button" style="display: none;">'+

      '</div>';

    }

    else if (method == 'economicMethod') {

      // TODO: Must remove all the previous tables first and reset the counter

      newTable.innerHTML =
        '<div id="customTableDiv_'+number+'" style="display: block;">'+
        '<table id="customTable_'+number+'" style="table-layout:fixed; width: 100%;">'+
        '<thead>'+
        '<tr>'+
        '<th>Indicator</th>'+
        '<th>Metric</th>'+
        '<th>Location</th>'+
        '<th>Mass</th>'+
        '<th>Cost</th>'+
        '</tr>'+
        '<thead>'+
        '<tbody>'+
        '<tr>'+
        '<td>'+
        '<input id="indicator" type="text" name="indicator" placeholder="Indicator" class="indicator"/>'+
        '</td>'+
        '<td><input id="metric" type="text" name="metric" placeholder="Metric" class="metric"/></td>'+
        '<td><input id="location" type="text" name="location" placeholder="Location" class="location" /></td>'+
        '<td><input id="mass" type="text" name="mass" placeholder="Mass" class="mass"/></td>'+
        '<td><input id="cost" type="text" name="cost" placeholder="Cost" class="cost" /></td>'+
        '</tr>'+
        '</tbody>'+
        '</table>'+
        '<input id="addButton_'+number+'" type="button" value="Add new record" class="addButton"/>'+
        '<input id="addNewProcessButton1_'+number+'" type="button" value="Add new process" class="addNewProcessButton1"/>'+
        '<label id="processCount_'+number+'"> Processes: 0/2 </label>'+
        '<label id="customTableErrorMessage_'+number+'" value="" style="color:red"></label>'+
        '<br>'+
        '<input id="exportDatabase_'+number+'" value="Export as CSV" type="button" style="display: none;">'+

      '</div>';
    }

    else if (method == 'environmentalMethod') {
      newTable.innerHTML =
        '<div id="customTableDiv_'+number+'" style="display: block;">'+
        '<table id="customTable_'+number+'" style="table-layout:fixed; width: 100%;">'+
        '<thead>'+
        '<tr>'+
        '<th>Indicator</th>'+
        '<th>Metric</th>'+
        '<th>Location</th>'+
        '<th>Mass</th>'+
        '<th>Emission Factor</th>'+
        '<th>Distance</th>'+
        '</tr>'+
        '<thead>'+
        '<tbody>'+
        '<tr>'+
        '<td>'+
        '<input id="indicator" type="text" name="indicator" placeholder="Indicator" class="indicator"/>'+
        '</td>'+
        '<td><input id="metric" type="text" name="metric" placeholder="Metric" class="metric"/></td>'+
        '<td><input id="location" type="text" name="location" placeholder="Location" class="location" /></td>'+
        '<td><input id="mass" type="text" name="mass" placeholder="Mass" class="mass"/></td>'+
        '<td><input id="emissionFactor" type="text" name="emissionFactor" placeholder="Emission Factor" class="emissionFactor" /></td>'+
        '<td><input id="distance" type="text" name="distance" placeholder="Distance" class="distance" /></td>'+
        '</tr>'+
        '</tbody>'+
        '</table>'+
        '<input id="addButton_'+number+'" type="button" value="Add new record" class="addButton"/>'+
        '<input id="addNewProcessButton1_'+number+'" type="button" value="Add new process" class="addNewProcessButton1"/>'+
        '<label id="processCount_'+number+'"> Processes: 0/2 </label>'+
        '<label id="customTableErrorMessage_'+number+'" value="" style="color:red"></label>'+
        '<br>'+
        '<input id="exportDatabase_'+number+'" value="Export as CSV" type="button" style="display: none;">'+

      '</div>';
    }

    document.getElementById("customTables").appendChild(newTable);

    // var newCustomTable = $('#customTable_'+number).dataTable();
    // customTables.push(newCustomTable);
    // console.log(customTables);
  }


  // Method that reads and processes the selected file
  function upload(evt) {
    if (!browserSupportFileUpload()) {
      alert('The File APIs are not fully supported in this browser!');
    }
    else {
      var data = null;
      var file = evt.target.files[0];
      var reader = new FileReader();
      reader.readAsText(file);

      var uploadId = this.id;

      reader.onload = function (event) {
        var csvData = event.target.result;
        data = $.csv.toArrays(csvData);

        // if(uploadId === 'txtFileUpload_1'){

        // We get the number of the selected upload field and we use it to populate the table and store the data to the 'tables' array
        var el_number= uploadId.slice(uploadId.length - 1);
        // We clear the table from previous data
        if (tables[el_number-1] != null &&  typeof tables[el_number-1] !== 'undefined') {
          tables[el_number-1].destroy();
          $('#CSVtable_'+el_number).empty();
        }

        if($('input:radio[name="method"]:checked').val() == "socialMethod"){
          if(checkCSVHeaderSocial(data) == false){
            $("#csvTableErrorMessage_"+el_number).text("Dataset must have five columns and have the header of 'Indicator,Metric,Location,Score,Total Score'");
            return;
          }
          $("#csvTableErrorMessage_"+el_number).text("");
        }
        else if ($('input:radio[name="method"]:checked').val() == "economicMethod"){
          if(checkCSVHeaderEconomic(data) == false){
            $("#csvTableErrorMessage_"+el_number).text("Dataset must have five columns and have the header of 'Indicator,Metric,Location,Mass,Cost (Colection/Transportation, Production, Distribution)'");
            return;
          }
          $("#csvTableErrorMessage_"+el_number).text("");

        }
        else if ($('input:radio[name="method"]:checked').val() == "environmentalMethod"){

          var type = 1;
          if(data[0][5] === "Distance"){
            type = 3;
          }
          if(checkCSVHeaderEnvironmental(data,type) == false){
            $("#csvTableErrorMessage_"+el_number).text("Dataset must have five or six columns and have the header of 'Indicator,Metric,Location,Mass,Emission Factor,(Distance)'");
            return;
          }
          $("#csvTableErrorMessage_"+el_number).text("");

        }


        tables[el_number-1] = populateTable(data, $('#CSVtable_'+el_number));

      };
      reader.onerror = function () {
        alert('Unable to read ' + file.fileName);
      };
    }
  }

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

    list.push($("#Result1").text());
    list.push($("#Result2").text());

    list.push($("#phase4Header").text());


    createPDF(canvasImg, null, equation_image, list);
  });
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
