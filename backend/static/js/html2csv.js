// Adopted from https://www.codexworld.com/export-html-table-data-to-csv-using-javascript/

var CSVCup  = {
    csv1 : [],
    csv2 : [],
    filename1 : "",
    filename2 : ""
}

var CSVCmid  = {
    csv1 : [],
    csv2 : [],
    filename1 : "",
    filename2 : ""
}

var CSVCdown  = {
    csv1 : [],
    csv2 : [],
    filename1 : "",
    filename2 : ""
}

function exportTableToCSV(indicator, filename, el_number, count, elements) {

    var tempCSV = [];

    var metric_elements = elements[0];
    var location_elements = elements[1];
    var score_elements = elements[2];
    var totalScore_elements = elements[3];

    var metrics = [];
    metric_elements.each(function () {
        metrics.push($(this).val());
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
    
    var header = ['Indicator','Metric','Location','Score','Total Score']
    var row = [];

    tempCSV.push(header.join(","));

    metrics.forEach(function(metric, index){
        if(index ==0){
            row.push(indicator)
        }
        else{
            row.push("");
        }
        row.push(metric, location[index], score[index], totalScore[index])
        tempCSV.push(row.join(","));
        row = [];
    });

    if(count == 1){
        CSVCup.csv1 = tempCSV;
        CSVCup.filename1 = filename;    
    }

    if(count == 2){
        CSVCup.csv2 = tempCSV;
        CSVCup.filename2 = filename;        

        // Download CSV files
        downloadCSV(CSVCup.csv1.join("\n"), CSVCup.filename1);
        downloadCSV(CSVCup.csv2.join("\n"),CSVCup.filename2);
    }

    
}

// Type 1 for Pup, type 2 for Pmid, type 3 for Pdown
function exportTableToCSVEnvironmental(indicator, filename, el_number, count, type, elements) {

    var tempCSV = [];

    var metric_elements = elements[0];
    var location_elements = elements[1];
        

    if(type == 1 || type == 2){
        var mass_elements = elements[2];
        var emFactor_elements = elements[3];    

        header = ['Indicator','Metric','Location','Mass','Emission Factor'];        
    }   

    if(type == 3){
        var mass_elements = elements[2];
        var emFactor_elements = elements[3];
        var distance_elements = elements[4];    
        
        header = ['Indicator','Metric','Location','Mass','Emission Factor', 'Distance'];
    }

    var metrics = [];
    metric_elements.each(function () {
        metrics.push($(this).val());
    });

    var location = [];
    location_elements.each(function () {
        location.push($(this).val());
    });

    var masses = [];
    mass_elements.each(function () {
        masses.push($(this).val());
    });

    var emFactors = [];
    emFactor_elements.each(function () {
        emFactors.push($(this).val());
    });
    
    var distances = [];
    if(distance_elements !=null){
        distance_elements.each(function () {              
            distances.push($(this).val());
        });
    }
    
    var row = [];

    tempCSV.push(header.join(","));

    masses.forEach(function(mass, index){
        if(index ==0){
            row.push(indicator)
        }
        else{
            row.push("");
        }

        if(distances.length != 0){
            row.push(metrics[index], location[index], mass, emFactors[index], distances[index]);
        }
        else{
            row.push(metrics[index], location[index], mass, emFactors[index])
        }
        tempCSV.push(row.join(","));
        row = [];
    });

    if(type == 1){
        assignValues(count, CSVCup, filename, tempCSV); 
    }

    if(type == 2){
        assignValues(count, CSVCmid, filename, tempCSV); 
    }

    if(type == 3){
        assignValues(count, CSVCdown, filename, tempCSV);   
    }    
}

function assignValues(count, CSVObj, filename, tempCSV){
    if(count == 1){
        CSVObj.csv1 = tempCSV;
        CSVObj.filename1 = filename;
    }

    if(count == 2){
        CSVObj.csv2 = tempCSV;
        CSVObj.filename2 = filename;

        // Download CSV files
        downloadCSV(CSVObj.csv1.join("\n"), CSVObj.filename1);
        downloadCSV(CSVObj.csv2.join("\n"), CSVObj.filename2);
    }
}

function exportTableToCSVEconomic(indicator, filename, el_number, count, elements) {

    var tempCSV = [];

    var header = ['Indicator','Metric','Location','Mass','Cost'];

    var metric_elements = elements[0];
    var location_elements = elements[1];
    var mass_elements = elements[2];
    var cost_elements = elements[3];
                           
    var metrics = [];
    metric_elements.each(function () {
        metrics.push($(this).val());
    });

    var location = [];
    location_elements.each(function () {
        location.push($(this).val());
    });

    var masses = [];
    mass_elements.each(function () {
        masses.push($(this).val());
    });

    var costs = [];
    cost_elements.each(function () {
        costs.push($(this).val());
    });   
    
    var row = [];

    tempCSV.push(header.join(","));

    masses.forEach(function(mass, index){
        if(index ==0){
            row.push(indicator)
        }
        else{
            row.push("");
        }

        row.push(metrics[index], location[index], mass, costs[index]);
        
        tempCSV.push(row.join(","));
        row = [];
    });

    if(count == 1){
        CSVCup.csv1 = tempCSV;
        CSVCup.filename1 = filename;
    }

    if(count == 2){
        CSVCup.csv2 = tempCSV;
        CSVCup.filename2 = filename;

        // Download CSV files
        downloadCSV(CSVCup.csv1.join("\n"), CSVCup.filename1);
        downloadCSV(CSVCup.csv2.join("\n"), CSVCup.filename2);
    }
    
}

function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;

    csvFile = new Blob([csv], {type: "text/csv"});

    downloadLink = document.createElement("a");

    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    downloadLink.click();
}