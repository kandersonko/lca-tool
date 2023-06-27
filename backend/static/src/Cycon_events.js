var preoptCounter = 0;
var columnTitles = [];

$(document).ready(function () {
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
                var el_number = uploadId.slice(uploadId.length - 1);
                // We clear the table from previous data
                if (tables[el_number - 1] != null && typeof tables[el_number - 1] !== 'undefined') {
                    tables[el_number - 1].destroy();
                    $('#CSVtable_' + el_number).empty();
                }

                if ($('input:radio[name="method"]:checked').val() == "socialMethod") {
                    if (checkCSVHeaderSocial(data) == false) {
                        $("#csvTableErrorMessage_" + el_number).text("Dataset must have five columns and have the header of 'Indicator,Metric,Location,Score,Total Score'");
                        return;
                    }
                    $("#csvTableErrorMessage_" + el_number).text("");
                }
                else if ($('input:radio[name="method"]:checked').val() == "economicMethod") {
                    if (checkCSVHeaderEconomic(data) == false) {
                        $("#csvTableErrorMessage_" + el_number).text("Dataset must have five columns and have the header of 'Indicator,Metric,Location,Mass,Cost (Colection/Transportation, Production, Distribution)'");
                        return;
                    }
                    $("#csvTableErrorMessage_" + el_number).text("");

                }
                else if ($('input:radio[name="method"]:checked').val() == "environmentalMethod") {

                    var type = 1;
                    if (data[0][5] === "Distance") {
                        type = 3;
                    }
                    if (checkCSVHeaderEnvironmental(data, type) == false) {
                        $("#csvTableErrorMessage_" + el_number).text("Dataset must have five or six columns and have the header of 'Indicator,Metric,Location,Mass,Emission Factor,(Distance)'");
                        return;
                    }
                    $("#csvTableErrorMessage_" + el_number).text("");

                }


                tables[el_number - 1] = populateTable(data, $('#CSVtable_' + el_number));

            };
            reader.onerror = function () {
                alert('Unable to read ' + file.fileName);
            };
        }
    }
 });

function changePreoptCategory(category, ID_Preopts) {
    var category_selection = document.getElementById(category)
    var category_name = category_selection.value

    dict_values = { Category: category_name };

    const sent_data = JSON.stringify(dict_values)

    $.ajax({
        url: "/experiments/getCategoryPreopts",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (data) {
            select = document.getElementById(ID_Preopts);
            select.options.length = 0;
            // Remove existing options in the selection
            var len = select.length;
            for (var i = 0; i < len; i++) {
                select.remove(0);
            }

            // For each preoptimization in the category, create a selection possibility.
            for (var Preopt in data) {
                var Preopt_Name = data[Preopt]["Name"];
                var Preopt_Display_Name = data[Preopt]["Display_Name"];

                if (data.hasOwnProperty(Preopt)) {
                    newOption = document.createElement('option');
                    optionText = document.createTextNode(Preopt_Display_Name);

                    newOption.appendChild(optionText);
                    newOption.setAttribute('value', Preopt_Name);

                    select.appendChild(newOption);
                }
            }
        }
    });
}



function changeAlgorithm(algorithms, ID_Parameters) {
    var algorithms_selection = document.getElementById(algorithms)
    var algorithm_name = algorithms_selection.value
    //document.getElementById("Results").innerHTML = method_name

    dict_values = { Algorithm: algorithm_name };

    const sent_data = JSON.stringify(dict_values)

    $.ajax({
        url: "/experiments/getAlgorithmParameters",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (data) {
            //document.getElementById("Results").innerHTML = "";
            var html_section = document.getElementById(ID_Parameters);
            html_section.innerHTML = "";

            // create the field box for the new preopt option.
            var field = document.createElement('fieldset');
            // create title for the field.
            var legend = document.createElement('legend');
            legend_text = document.createTextNode(algorithm_name);
            legend.appendChild(legend_text);
            field.appendChild(legend);

            for (var Parameter in data) {
                //document.getElementById("Results").innerHTML += data[Parameter]["Name"] + " ";
                var Parameter_Name = data[Parameter]["Name"];

                if (data.hasOwnProperty(Parameter)) {
                    // Create a label, which will be the parameter Name followed by the default value.
                    var name_label = Parameter_Name + " (Default: " + data[Parameter]["Default"] + ") ";
                    var label = document.createElement('label');
                    label.htmlFor = name_label;
                    label.appendChild(document.createTextNode(name_label));
                    let id_info = data[Parameter]["Name"] + "_Info";

                    field.appendChild(label);

                    // Create popup information.
                    let newDiv = document.createElement("div");
                    newDiv.className = "popup";
                    newDiv.onclick = function () { popupInformation(id_info); };

                    let newImage = document.createElement("img");
                    newImage.src = "../../static/Images/information_icon.png";
                    newImage.width = "20";
                    newImage.height = "20";

                    newDiv.appendChild(newImage);

                    let newSpan = document.createElement("span");
                    newSpan.style = "white-space: pre-wrap";
                    newSpan.className = "popuptext";
                    newSpan.id = id_info;
                    newSpan.textContent = data[Parameter]["Definition"];

                    newDiv.appendChild(newSpan);

                    field.appendChild(newDiv);

                    // Create choices and options to edit the parameter

                    fillSection(field, data, Parameter, ID_Parameters, 0, )
                }
            }

            html_section.appendChild(field)
        }
    });
}

function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

function getData(form) {
    // Copy over information from element outside of form to the copy inside form
    document.getElementById("projectName_copy").value = document.getElementById("projectName").value;
    document.getElementById("phase1Text_copy").value = document.getElementById("phase1Text").value;
    document.getElementById("csvFile_copy").value = document.getElementById("csvFile").value;

    // Collect all form data instances
    var formData = new FormData(form);

    var dict_data = {};

    const csvFileName = document.getElementById("csvFile").files[0].name;
    formData.append("csvFileName", csvFileName);

    var checkbox = $("#cyconForm").find("input[type=checkbox]");
    $.each(checkbox, function (key, val) {
        formData.append($(val).attr('name') + "_checked", $(this).is(':checked'));
    });

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json
    dict_values = { "form": dict_data };

    const sent_data = JSON.stringify(dict_values)

    $.ajax({
        url: "/experiments/run_experiment",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (Results) {
            if (Results[0] == "worked") {

                Results = Results[2]

                var writeData = {
                    paragraph: ''
                }

                // Experiment info
                // Phase 1
                // Name of Experiment
                writeData.paragraph += "Experiment Information".bold().italics().big() + "<br\>"
                writeData.paragraph += "Name of Experiment: ".bold().italics() + "<br\>" + dict_data["projectName"] + "<br\><br\>"
                // Goal and Scope
                writeData.paragraph += "Goal and Scope: ".bold().italics() + "<br\>" + dict_data["phase1Text"] + "<br\><br\>"
                // Phase 2
                // Name of Dataset
                writeData.paragraph += "Dataset Information".bold().italics().big() + "<br\>"
                writeData.paragraph += "Dataset File: ".bold().italics() + "<br\>" + dict_data["csvFileName"] + "<br\><br\>"
                // Preoptimization
                writeData.paragraph += "Preoptimization: ".bold().italics() + "<br\>" + dict_data["preoptimization"] + "<br\><br\>"
                // Phase 3
                // Name of Methology
                writeData.paragraph += "Methodology Information".bold().italics().big() + "<br\>"
                writeData.paragraph += "Name of Methodology: ".bold().italics() + "<br\>" + dict_data["methodology"] + "<br\><br\>"
                // Name of Method
                writeData.paragraph += "Method: ".bold().italics() + "<br\>" + dict_data["MLalgorithm"] + "<br\><br\>"
                // Algorithm parameters
                writeData.paragraph += "Method Parameters".bold().italics() + "<br\>"
                for (let i = 0; i < Results["Parameter_Length"]; i++) {
                    writeData.paragraph += Results["Parameter_" + i + "_Name"].bold() + ": ".bold() + Results["Parameter_" + i] + "<br\>"
                }

                writeData.paragraph += "<br\>"

                // Validation
                writeData.paragraph += "Validation".bold().italics() + "<br\>"
                writeData.paragraph += "Method: ".bold() + dict_data["validation"] + "<br\>"
                writeData.paragraph += "Random State: ".bold() + Results["Val_Random_State"] + "<br\>"
                writeData.paragraph += "Shuffle: ".bold() + Results["Val_Shuffle"] + "<br\>"

                writeData.paragraph += "<br\>"


                if (Results['Validation'] == "Split") {
                    // obtain the Metrics
                    Accuracy = Results["Accuracy"]
                    F1 = Results["F1"]
                    F1_micro = Results["F1_micro"]
                    F1_macro = Results["F1_macro"]
                    Precision = Results["Precision"]
                    Precision_micro = Results["Precision_micro"]
                    Precision_macro = Results["Precision_macro"]
                    Conf_Matrix = Results["cm_overall"]


                    // display the metrics
                    var img = new Image();

                    img.src = "data:image/png;base64," + Results["cm_overall"];


                    writeData.paragraph += '=========================Results=========================<br\>'
                    writeData.paragraph += Results["Accuracy_Intro"].bold() + Results["Accuracy"] + '<br\>'
                    writeData.paragraph += Results["Precision_Intro"].bold() + Results["Precision"] + "<br\>"
                    writeData.paragraph += Results["Precision_micro_Intro"].bold() + Results["Precision_micro"] + "<br\>"
                    writeData.paragraph += Results["Precision_macro_Intro"].bold() + Results["Precision_macro"] + "<br\>"
                    writeData.paragraph += Results["F1_Intro"].bold() + Results["F1"] + "<br\>"
                    writeData.paragraph += Results["F1_micro_Intro"].bold() + Results["F1_micro"] + "<br\>"
                    writeData.paragraph += Results["F1_macro_Intro"].bold() + Results["F1_macro"] + "<br\>"
                    writeData.paragraph += `${img.outerHTML}`


                    //$('#Results').html(data.paragraph);
                    document.getElementById("Results").innerHTML = writeData.paragraph;
                }

                else if (Results['Validation'] == "K-Fold") {


                    for (let i = 0; i < Results["acc_list"].length; i++) {
                        writeData.paragraph += '=========================Results for Fold ' + i + '=========================<br\>'
                        writeData.paragraph += Results["Accuracy_Intro"].bold() + Results["acc_list"][i] + '<br\>'
                        writeData.paragraph += Results["Precision_Intro"].bold() + Results["prec_list"][i] + '<br\>'
                        writeData.paragraph += Results["Precision_micro_Intro"].bold() + Results["prec_micro_list"][i] + '<br\>'
                        writeData.paragraph += Results["Precision_macro_Intro"].bold() + Results["prec_macro_list"][i] + '<br\>'
                        writeData.paragraph += Results["F1_Intro"].bold() + Results["f1_list"][i] + '<br\>'
                        writeData.paragraph += Results["F1_micro_Intro"].bold() + Results["f1_micro_list"][i] + '<br\>'
                        writeData.paragraph += Results["F1_macro_Intro"].bold() + Results["f1_macro_list"][i] + '<br\>'

                        var img = new Image();
                        img.src = 'data:image/jpeg;base64,' + Results["cm_list"][i];

                        writeData.paragraph += `${img.outerHTML} <br\>`

                    }

                    writeData.paragraph += '<br\>'
                    writeData.paragraph += '=========================Results Overall=========================<br\>'
                    writeData.paragraph += Results["Accuracy_Intro_Overall"].bold() + Results["acc_average"] + '<br\>'
                    writeData.paragraph += Results["Precision_Intro_Overall"].bold() + Results["prec_average"] + '<br\>'
                    writeData.paragraph += Results["Precision_micro_Intro_Overall"].bold() + Results["prec_micro_average"] + '<br\>'
                    writeData.paragraph += Results["Precision_macro_Intro_Overall"].bold() + Results["prec_macro_average"] + '<br\>'
                    writeData.paragraph += Results["F1_Intro_Overall"].bold() + Results["f1_average"] + '<br\>'
                    writeData.paragraph += Results["F1_micro_Intro_Overall"].bold() + Results["f1_micro_average"] + '<br\>'
                    writeData.paragraph += Results["F1_macro_Intro_Overall"].bold() + Results["f1_macro_average"] + '<br\>'

                    var img = new Image();
                    img.src = 'data:image/jpeg;base64,' + Results['cm_overall'];

                    writeData.paragraph += `${img.outerHTML} <br\>`

                    document.getElementById("Results").innerHTML = writeData.paragraph;
                }
            }
            else {
                var writeData = {
                    paragraph: ''
                }

                writeData.paragraph += '<FONT COLOR="#ff0000">ERROR: <br>';
                writeData.paragraph += Results[1];
                writeData.paragraph += '</FONT >';

                document.getElementById("Results").innerHTML =  writeData.paragraph;
            }
        }
    });
}

document.getElementById("cyconForm").addEventListener("submit", function (e) {
    e.preventDefault();
    getData(e.target);
});



function displayResults(form) {
    // Collect all form data instances
    var formData = new FormData(form);

    var dict_data = {};

    const projectName = document.getElementById("projectName").value;
    formData.append("projectName", projectName);

    var checkbox = $("#resultForm").find("input[type=checkbox]");
    $.each(checkbox, function (key, val) {
        formData.append($(val).attr('name') + "_checked", $(this).is(':checked'));
    });

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json
    dict_values = { "form": dict_data };

    const sent_data = JSON.stringify(dict_values)

    $.ajax({
        url: "/experiments/getResults",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (Results) {

            var writeData = {
                paragraph: ''
            }

            // Experiment info
            // Phase 1
            // Name of Experiment
            writeData.paragraph += "Experiment Information".bold().italics().big() + "<br\>"
            writeData.paragraph += "Name of Experiment: ".bold().italics() + "<br\>" + dict_data["projectName"] + "<br\><br\>"
            // Goal and Scope
            writeData.paragraph += "Goal and Scope: ".bold().italics() + "<br\>" + dict_data["phase1Text"] + "<br\><br\>"
            // Phase 2
            // Name of Dataset
            writeData.paragraph += "Dataset Information".bold().italics().big() + "<br\>"
            writeData.paragraph += "Dataset File: ".bold().italics() + "<br\>" + dict_data["csvFIle"] + "<br\><br\>"
            // Preoptimization
            writeData.paragraph += "Preoptimization: ".bold().italics() + "<br\>" + dict_data["preoptimization"] + "<br\><br\>"
            // Phase 3
            // Name of Methology
            writeData.paragraph += "Methodology Information".bold().italics().big() + "<br\>"
            writeData.paragraph += "Name of Methodology: ".bold().italics() + "<br\>" + dict_data["methodology"] + "<br\><br\>"
            // Name of Method
            writeData.paragraph += "Method: ".bold().italics() + "<br\>" + dict_data["MLalgorithm"] + "<br\><br\>"
            // Algorithm parameters
            writeData.paragraph += "Method Parameters".bold().italics() + "<br\>"
            for (let i = 0; i < Results["Parameter_Length"]; i++) {
                writeData.paragraph += Results["Parameter_" + i + "_Name"].bold() + ": ".bold() + Results["Parameter_" + i] + "<br\>"
            }

            writeData.paragraph += "<br\>"

            // Validation
            writeData.paragraph += "Validation".bold().italics() + "<br\>"
            writeData.paragraph += "Method: ".bold() + dict_data["validation"] + "<br\>"
            writeData.paragraph += "Random State: ".bold() + Results["Val_Random_State"] + "<br\>"
            writeData.paragraph += "Shuffle: ".bold() + Results["Val_Shuffle"] + "<br\>"

            writeData.paragraph += "<br\>"

            if (Results['Validation'] == "Split") {

                // display the metrics
                var img = new Image();

                img.src = "data:image/png;base64," + Results["cm_overall"];


                // Quick way to do this, this will be changed when Metrics class is created...
                //  Then a loop will go through all metrics, check if each check mark is selected.
                //      Then implement a given sentence and value...
                if (dict_data['Met_ACC_checked'] == "true") {
                    writeData.paragraph += Results["Accuracy_Intro"].bold() + Results["Accuracy"] + '<br\>'
                }


                if (dict_data['Met_Precision_checked'] == "true") {
                    writeData.paragraph += Results["Precision_Intro"] .bold() + Results["Precision"] + "<br\>"
                }

                if (dict_data['Met_Precision_Micro_checked'] == "true") {
                    writeData.paragraph += Results["Precision_micro_Intro"].bold() + Results["Precision_micro"] + "<br\>"
                }

                if (dict_data['Met_Precision_Macro_checked'] == "true") {
                    writeData.paragraph += Results["Precision_macro_Intro"].bold() + Results["Precision_macro"] + "<br\>"
                }


                if (dict_data['Met_F1_checked'] == "true") {
                    writeData.paragraph += Results["F1_Intro"].bold() + Results["F1"] + "<br\>"
                }

                if (dict_data['Met_F1_Micro_checked'] == "true") {
                    writeData.paragraph += Results["F1_micro_Intro"].bold() + Results["F1_micro"] + "<br\>"
                }


                if (dict_data['Met_F1_Macro_checked'] == "true") {
                    writeData.paragraph += Results["F1_macro_Intro"].bold() + Results["F1_macro"] + "<br\>"
                }

                if (dict_data['Met_CM_checked'] == "true") {
                    writeData.paragraph += `${img.outerHTML}`
                }

                //$('#Results').html(data.paragraph);
                document.getElementById("Results").innerHTML = writeData.paragraph;
            }

            else if (Results['Validation'] == "K-Fold") {

                for (let i = 0; i < Results["acc_list"].length; i++) {
                    writeData.paragraph += '=========================Results for Fold ' + i + '=========================<br\>'

                    if (dict_data['Met_ACC_checked'] == "true") {
                        writeData.paragraph += Results["Accuracy_Intro"].bold() + Results["acc_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_Precision_checked'] == "true") {
                        writeData.paragraph += Results["Precision_Intro"].bold() + Results["prec_list"][i] + '<br\>'
                    }

                    if (dict_data['Met_Precision_Micro_checked'] == "true") {
                        writeData.paragraph += Results["Precision_micro_Intro"].bold() + Results["Prec_micro_list"][i] + "<br\>"
                    }

                    if (dict_data['Met_Precision_Macro_checked'] == "true") {
                        writeData.paragraph += Results["Precision_macro_Intro"].bold() + Results["prec_macro_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_F1_checked'] == "true") {
                        writeData.paragraph += Results["F1_Intro"].bold() + Results["f1_list"][i] + '<br\>'
                    }

                    if (dict_data['Met_F1_Micro_checked'] == "true") {
                        writeData.paragraph += Results["F1_micro_Intro"].bold() + Results["f1_micro_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_F1_Macro_checked'] == "true") {
                        writeData.paragraph += Results["F1_macro_Intro"].bold() + Results["f1_macro_list"][i] + '<br\>'
                    }


                    var img = new Image();
                    img.src = 'data:image/jpeg;base64,' + Results["cm_list"][i];

                    if (dict_data['Met_CM_checked'] == "true") {
                        writeData.paragraph += `${img.outerHTML}`
                    }
                    writeData.paragraph += '<br\>'

                }

                writeData.paragraph += '=========================Results Overall=========================<br\>'

                if (dict_data['Met_ACC_checked'] == "true") {
                    writeData.paragraph += Results["Accuracy_Intro_Overall"].bold() + Results["acc_average"] + '<br\>'
                }


                if (dict_data['Met_Precision_checked'] == "true") {
                    writeData.paragraph += Results["Precision_Intro_Overall"].bold() + Results["prec_average"] + '<br\>'
                }

                if (dict_data['Met_Precision_Micro_checked'] == "true") {
                    writeData.paragraph += Results["Precision_micro_Intro_Overall"].bold() + Results["prec_micro_average"] + '<br\>'
                }

                if (dict_data['Met_Precision_Macro_checked'] == "true") {
                    writeData.paragraph += Results["Precision_macro_Intro_Overall"].bold() + Results["prec_macro_average"] + '<br\>'
                }


                if (dict_data['Met_F1_checked'] == "true") {
                    writeData.paragraph += Results["F1_Intro_Overall"].bold() + Results["f1_average"] + '<br\>'
                }

                if (dict_data['Met_F1_Micro_checked'] == "true") {
                    writeData.paragraph += Results["F1_micro_Intro_Overall"].bold() + Results["f1_micro_average"] + '<br\>'
                }


                if (dict_data['Met_F1_Macro_checked'] == "true") {
                    writeData.paragraph += Results["F1_macro_Intro_Overall"].bold() + Results["f1_macro_average"] + '<br\>'
                }


                var img = new Image();
                img.src = 'data:image/jpeg;base64,' + Results['cm_overall'];

                if (dict_data['Met_CM_checked'] == "true") {
                    writeData.paragraph += `${img.outerHTML}`
                }


                document.getElementById("Results").innerHTML = writeData.paragraph;
            }
        }
    });
}

document.getElementById("resultForm").addEventListener("submit", function (e) {
    e.preventDefault();
    displayResults(e.target);
});



function generatePDF(form) {

    let element = document.getElementById('Results')

    
    html2pdf(element, {
        margin: 10,
        filename: "Results.pdf",
        image: { type: 'jpeg', quality: 2 },
        html2canvas: { dpi: 300, letterRendering: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }).get('pdf').then(function (pdf) {
            var totalPages = pdf.internal.getNumberOfPages();

            for (let i = 1; i <= totalPages; i++) {
                pdf.setPage(i);
                pdf.setFontSize(10);
                pdf.setTextColor(150);
                // Add you content in place of example here
                pdf.text("Created using the IDeaL Cycon Tool: https://cycon.nkn.uidaho.edu/cycon", pdf.internal.pageSize.getWidth() - 120, pdf.internal.pageSize.getHeight() - 10);
            }
        }).save();

}

// When the user clicks on div, open the popup
function popupInformation(id) {
    var popup = document.getElementById(id);
    popup.classList.toggle("show");
}

document.getElementById("resultForm").addEventListener("button", function (e) {
    e.preventDefault();
    generatePDF(e.target);
});



// Checks that the CSV file is able to load and displays the original csv information with additional pdf graphs
// such as balance and distibution of data to help the user make informed desitions when preoptimizing.
function checkCSV(form) {
    document.getElementById("csv_Error").innerHTML = "";
    document.getElementById("csv_Results").innerHTML = "";

    var formData = new FormData(form);

    var dict_data = {};

    const projectName = document.getElementById("projectName").value;
    formData.append("projectName", projectName);

    const csvFileName = document.getElementById("csvFile").files[0].name;
    formData.append("csvFileName", csvFileName);

    formData.append("Perform_Preopt", "No")

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        //document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json
    dict_values = { "form": dict_data };

    const sent_data = JSON.stringify(dict_values)

    $("#csv_Title").hide();
    $("#csv_shape").hide();
    $("#csv_Null_Title").hide();
    $("#csv_Null_Results").hide();
    $("#csv_Class_Balance_Title").hide();
    $("#csv_Class_Balance_Results").hide();
    $("#csv_Scale_Title").hide();
    $("#csv_Scale_Results").hide();

    $.ajax({
        url: "/experiments/getCSVResults",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (Results) {
            if (Results[0] == "worked") {

                Results = Results[2]

                var writeData = {
                    paragraph: ''
                }

                document.getElementById("csv_Results").innerHTML = Results['csv_Short'];
                document.getElementById("csv_shape").innerHTML = "Shape: " + Results['shape']
                document.getElementById("csv_Null_Results").innerHTML = Results['null_Count']

                $("#csv_Title").show();
                $("#csv_shape").show();
                $("#csv_Null_Title").show();
                $("#csv_Null_Results").show();

                if (dict_values["class_col"] != "") {
                    document.getElementById("csv_Class_Balance_Results").innerHTML = Results['Number_Classes'];
                    $("#csv_Class_Balance_Title").show();
                    $("#csv_Class_Balance_Results").show();
                }

                document.getElementById("csv_Scale_Results").innerHTML = ""
                if (dict_values["kde_ind"] != "") {
                    if (dict_values["class_col"] != "") {
                        for (i in Results["kde_plots"]) {
                            var img = new Image();
                            img.src = 'data:image/jpeg;base64,' + Results["kde_plots"][i];

                            document.getElementById("csv_Scale_Results").innerHTML += `${img.outerHTML}`

                            $("#csv_Scale_Title").show();
                            $("#csv_Scale_Results").show();
                        }
                    }
                }
            }
            else {
                var writeData = {
                    paragraph: ''
                }

                writeData.paragraph += '<FONT COLOR="#ff0000">ERROR: <br>';
                writeData.paragraph += Results[1];
                writeData.paragraph += '</FONT >';

                document.getElementById("csv_Error").innerHTML = writeData.paragraph;
            }

        },
        error: function (jqXHR, textStatus, errorThrown) {
            var writeData = {
                paragraph: ''
            }

            writeData.paragraph += "ERROR: "
            writeData.paragraph += textStatus
            document.getElementById("csv_Error").innerHTML = writeData.paragraph;
        }
    });
}

document.getElementById("csvForm").addEventListener("submit", function (e) {
    e.preventDefault();
    checkCSV(e.target);
});


// Checks that the CSV file is able to load and displays the csv information after all selected preoptimizations with additional pdf graphs
// such as balance and distibution of data to help the user make informed desitions when preoptimizing.
function checkCSV_Preopt(form) {
    document.getElementById("csv_Error_Preopt").innerHTML = "";
    document.getElementById("csv_Results_Preopt").innerHTML = "";

    var formData = new FormData(form);
    var csvFormData = new FormData(document.getElementById("csvForm"));

    var dict_data = {};

    const projectName = document.getElementById("projectName").value;
    formData.append("projectName", projectName);

    const csvFileName = document.getElementById("csvFile").files[0].name;
    formData.append("csvFileName", csvFileName);

    formData.append("Perform_Preopt", "Yes")

    formData.append("preoptCounter", preoptCounter)

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        dict_data[pair[0]] = pair[1]
    }

    for (var pair of csvFormData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json
    dict_values = { "form": dict_data };

    const sent_data = JSON.stringify(dict_values)

    $("#csv_Title_Preopt").hide();
    $("#csv_shape_Preopt").hide();
    $("#csv_Null_Title_Preopt").hide();
    $("#csv_Null_Results_Preopt").hide();
    $("#csv_Class_Balance_Title_Preopt").hide();
    $("#csv_Class_Balance_Results_Preopt").hide();
    $("#csv_Scale_Title_Preopt").hide();
    $("#csv_Scale_Results_Preopt").hide();

    $.ajax({
        url: "/experiments/getCSVResults",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (Results) {
            if (Results[0] == "worked") {

                Results = Results[2]

                var writeData = {
                    paragraph: ''
                }

                document.getElementById("csv_Results_Preopt").innerHTML = Results['csv_Short'];
                document.getElementById("csv_shape_Preopt").innerHTML = "Shape: " + Results['shape']
                document.getElementById("csv_Null_Results_Preopt").innerHTML = Results['null_Count']

                $("#csv_Title_Preopt").show();
                $("#csv_shape_Preopt").show();
                $("#csv_Null_Title_Preopt").show();
                $("#csv_Null_Results_Preopt").show();

                if (dict_values["class_col"] != "") {
                    document.getElementById("csv_Class_Balance_Results_Preopt").innerHTML = Results['Number_Classes'];
                    $("#csv_Class_Balance_Title_Preopt").show();
                    $("#csv_Class_Balance_Results_Preopt").show();
                }

                document.getElementById("csv_Scale_Results_Preopt").innerHTML = ""
                if (dict_values["kde_ind"] != "") {
                    if (dict_values["class_col"] != "") {
                        for (i in Results["kde_plots"]) {
                            var img = new Image();
                            img.src = 'data:image/jpeg;base64,' + Results["kde_plots"][i];

                            document.getElementById("csv_Scale_Results_Preopt").innerHTML += `${img.outerHTML}`

                            $("#csv_Scale_Title_Preopt").show();
                            $("#csv_Scale_Results_Preopt").show();
                        }
                    }
                }
            }
            else {
                var writeData = {
                    paragraph: ''
                }

                writeData.paragraph += '<FONT COLOR="#ff0000">ERROR: <br>';
                writeData.paragraph += Results[1];
                writeData.paragraph += '</FONT >';

                document.getElementById("csv_Error_Preopt").innerHTML = writeData.paragraph;
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var writeData = {
                paragraph: ''
            }

            writeData.paragraph += '<FONT COLOR="#ff0000">ERROR: <br>';
            writeData.paragraph += "Error with connection to server!";
            writeData.paragraph += '</FONT >';

            document.getElementById("csv_Error_Preopt").innerHTML = writeData.paragraph;
        }
    });
}

document.getElementById("preoptForm").addEventListener("submit", function (e) {
    e.preventDefault();
    checkCSV_Preopt(e.target);
});



// Addes the selected preoptimization to the form. 
function selectPreopt(Preopt, ID_Preopt) {
    if (preoptCounter != 10) {

        var Preopt_selection = document.getElementById(Preopt)
        var Preopt_name = Preopt_selection.options[Preopt_selection.selectedIndex].text
        var Preopt_value = Preopt_selection.value
        //document.getElementById("Results").innerHTML = method_name

        dict_values = { Preopt: Preopt_value };

        const sent_data = JSON.stringify(dict_values)

        // document.getElementById(ID_Preopt).innerHTML = sent_data;

        // document.getElementById(ID_Preopt).innerHTML = "Test 1";

        // Get the parameters for the selected Preopt option.
        $.ajax({
            url: "/experiments/getPreoptParameters",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(sent_data),
            async: false,
            dataType: 'json',
            success: function (data) {
                // Create the html section to place in the cycon page.
                var html_section = document.getElementById(ID_Preopt);

                // create the field box for the new preopt option.
                var field = document.createElement('fieldset');
                // create title for the field.
                var legend = document.createElement('legend');
                legend_text = document.createTextNode(Preopt_name);
                legend.appendChild(legend_text);
                field.appendChild(legend);

                // Create a hidden value that will contain the selected parameter name.
                var textbox = document.createElement("input");
                textbox.type = "text";
                textbox.name = "Preopt_" + preoptCounter;
                textbox.value = Preopt_value;
                textbox.style.display = "none";

                field.appendChild(textbox);

                // Create option to edit the parameter for the preoptimization option.
                for (var Parameter in data) {

                    var Parameter_Name = data[Parameter]["Name"];

                    if (data.hasOwnProperty(Parameter)) {
                        // Create a label, which will be the parameter Name followed by the default value.
                        var name_label = Parameter_Name + " (Default: " + data[Parameter]["Default"] + ") ";
                        var label = document.createElement('label');
                        label.htmlFor = name_label;
                        label.appendChild(document.createTextNode(name_label));
                        let id_info = data[Parameter]["Name"] + "_Info";

                        field.appendChild(label);

                        // Create popup information.
                        let newDiv = document.createElement("div");
                        newDiv.className = "popup";
                        newDiv.onclick = function () { popupInformation(id_info); };

                        let newImage = document.createElement("img");
                        newImage.src = "../../static/Images/information_icon.png";
                        newImage.width = "20";
                        newImage.height = "20";

                        newDiv.appendChild(newImage);

                        let newSpan = document.createElement("span");
                        newSpan.style = "white-space: pre-wrap";
                        newSpan.className = "popuptext";
                        newSpan.id = id_info;
                        newSpan.textContent = data[Parameter]["Definition"];

                        newDiv.appendChild(newSpan);

                        field.appendChild(newDiv);

                        // Create choices and options to edit the parameter

                        fillSection(field, data, Parameter, "Preopt", preoptCounter)
                    }
                }
                // TO DO LATER: Add button to remove the individual preoptimization parameter.

                // add field to div section
                html_section.appendChild(field)

            }
        });

        preoptCounter = preoptCounter + 1;
    }
}

// Removes all preoptimization options.
function clearAllPreopt() {
    document.getElementById("Preopt_Selection").innerHTML = "";
    document.getElementById("csv_Error_Preopt").innerHTML = "";
    preoptCounter = 0;

    document.getElementById("csv_Results").innerHTML = "";
    document.getElementById("csv_shape").innerHTML = "";
    document.getElementById("csv_Null_Results").innerHTML = "";
    document.getElementById("csv_Class_Balance_Results").innerHTML = "";
    document.getElementById("csv_Scale_Results").innerHTML = "";

    $("#csv_Title").hide();
    $("#csv_shape").hide();
    $("#csv_Null_Title").hide();
    $("#csv_Null_Results").hide();
    $("#csv_Class_Balance_Title").hide();
    $("#csv_Class_Balance_Results").hide();
    $("#csv_Scale_Title").hide();
    $("#csv_Scale_Results").hide();

    document.getElementById("csv_Results_Preopt").innerHTML = "";
    document.getElementById("csv_shape_Preopt").innerHTML = "";
    document.getElementById("csv_Null_Results_Preopt").innerHTML = "";
    document.getElementById("csv_Class_Balance_Results_Preopt").innerHTML = "";
    document.getElementById("csv_Scale_Results_Preopt").innerHTML = "";

    $("#csv_Title_Preopt").hide();
    $("#csv_shape_Preopt").hide();
    $("#csv_Null_Title_Preopt").hide();
    $("#csv_Null_Results_Preopt").hide();
    $("#csv_Class_Balance_Title_Preopt").hide();
    $("#csv_Class_Balance_Results_Preopt").hide();
    $("#csv_Scale_Title_Preopt").hide();
    $("#csv_Scale_Results_Preopt").hide();
}


// Method to fill an html paragraph or section via the parameters
function fillSection(section, data, Parameter, Location, counter) {

    var default_p = data[Parameter]["Default"];
    
    var Parameter_Name = data[Parameter]["Name"];

    if (Location == "Preopt") {
        Parameter_Name = "Preopt_" + counter + "_" + data[Parameter]["Name"];
    }


    // Create choices and options to alter the parameter
    for (var Type_Int in data[Parameter]["Type"]) {
        // Selectable options.
        if (data[Parameter]["Type"][Type_Int] == "option") {
            for (var Option_Int in data[Parameter]["Possible"]) {
                // create radio button
                var radio_name = Parameter_Name + "_Input";
                var option = data[Parameter]["Possible"][Option_Int];
                var radio = document.createElement("input");
                radio.type = "radio";
                radio.name = radio_name;
                radio.id = option;
                radio.value = option;
                section.appendChild(radio);
                if (option == default_p) {
                    radio.checked = true;
                }

                // create label for radio button
                var name_label = option;
                var label = document.createElement('label')
                label.htmlFor = name_label;
                label.appendChild(document.createTextNode(name_label));

                section.appendChild(label);
            }
        }

        // Selectable option for a list to be placed in a select element
        if (data[Parameter]["Type"][Type_Int] == "select") {
            if (data[Parameter]["Possible"] == "col_names") {

                select = document.createElement('select');
                select.id = Parameter_Name + "_Input";
                select.name = Parameter_Name + "_Input";

                // Possible choises, (I.E. column titles)
                for (title in columnTitles) {
                    newOption = document.createElement('option');
                    optionText = document.createTextNode(columnTitles[title]);

                    newOption.appendChild(optionText);
                    newOption.setAttribute('value', columnTitles[title]);

                    select.appendChild(newOption);
                }

                // add to section
                section.appendChild(select);
            }
        }

        
        //  Selectable option with a float entry option
        if (data[Parameter]["Type"][Type_Int] == "option_float") {
            for (var Option_Int in data[Parameter]["Possible"]) {
                // create radio button
                var radio_name = Parameter_Name + "_Input";
                var option = data[Parameter]["Possible"][Option_Int];
                var radio = document.createElement("input");
                radio.type = "radio";
                radio.name = radio_name;
                radio.id = option;
                radio.value = option;
                section.appendChild(radio);

                if (typeof default_p != 'number') {
                    if (option == default_p) {
                        radio.checked = true;
                    }
                }

                if (typeof default_p == 'number' && !isNaN(default_p)) {
                    if (option == "float") {
                        radio.check = true;
                    }
                }

                // create label for radio button
                var name_label = option;
                var label = document.createElement('label')
                label.htmlFor = name_label;
                label.appendChild(document.createTextNode(name_label));

                section.appendChild(label);

                if (option == "float") {
                    var selection = Parameter_Name + "_Float_Input";
                    var textbox = document.createElement("input");
                    textbox.type = "text";
                    textbox.name = selection;
                    section.appendChild(textbox);

                    if (typeof default_p == 'number' && !isNaN(default_p)) {
                        texbox.value = default_p;
                    }
                }
            }
        }

        //  Selectable option with a float entery option
        if (data[Parameter]["Type"][Type_Int] == "option_int") {
            for (var Option_Int in data[Parameter]["Possible"]) {
                // create radio button
                var radio_name = Parameter_Name + "_Input";
                var option = data[Parameter]["Possible"][Option_Int];
                var radio = document.createElement("input");
                radio.type = "radio";
                radio.name = radio_name;
                radio.id = option;
                radio.value = option;
                section.appendChild(radio);

                if (typeof default_p != 'number') {
                    if (option == default_p) {
                        radio.checked = true;
                    }
                }

                if (typeof default_p == 'number' && !isNaN(default_p)) {
                    if (option == "int") {
                        radio.check = true;
                    }
                }

                // create label for radio button
                var name_label = option;
                var label = document.createElement('label')
                label.htmlFor = name_label;
                label.appendChild(document.createTextNode(name_label));

                section.appendChild(label);

                if (option == "int") {
                    var selection = Parameter_Name + "_Int_Input";
                    var textbox = document.createElement("input");
                    textbox.type = "text";
                    textbox.name = selection;
                    section.appendChild(textbox);

                    if (typeof default_p == 'number' && !isNaN(default_p)) {
                        texbox.value = default_p;
                    }
                }
            }
        }

        // Integer only
        else if (data[Parameter]["Type"][Type_Int] == "int") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;

            textbox.value = default_p;

            section.appendChild(textbox);
        }

        // Integer or null
        else if (data[Parameter]["Type"][Type_Int] == "int_or_null") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;

            if (typeof default_p == 'number' && !isNaN(default_p)) {
                textbox.value = default_p;
            }

            section.appendChild(textbox);
        }

        // Float or null
        else if (data[Parameter]["Type"][Type_Int] == "float_or_null") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;

            if (typeof default_p == 'number' && !isNaN(default_p)) {
                textbox.value = default_p;
            }

            section.appendChild(textbox);
        }

        // Float only
        else if (data[Parameter]["Type"][Type_Int] == "float") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;

            textbox.value = default_p;

            section.appendChild(textbox);
        }

        // Bool only
        else if (data[Parameter]["Type"][Type_Int] == "bool") {
            for (var Option_Int in data[Parameter]["Possible"]) {
                // create radio button
                var radio_name = Parameter_Name + "_Input";
                var option = data[Parameter]["Possible"][Option_Int];
                var radio = document.createElement("input");
                radio.type = "radio";
                radio.name = radio_name;
                radio.id = option;
                radio.value = option;
                section.appendChild(radio);

                if (option == default_p) {
                    radio.checked = true;
                }

                // create label for radio button
                var name_label = option;
                var label = document.createElement('label')
                label.htmlFor = name_label;
                label.appendChild(document.createTextNode(name_label));

                section.appendChild(label);
            }
        }

        // String entry only
        else if (data[Parameter]["Type"][Type_Int] == "str") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;
            textbox.value = data[Parameter]["Default"];
            section.appendChild(textbox);
        }

        // Equation entry only
        else if (data[Parameter]["Type"][Type_Int] == "equation") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;
            section.appendChild(textbox);
        }
        section.appendChild(document.createElement("br"));
    }
    

    // section.appendChild(document.createElement("br"));
}


// Updates the csv dataset information. Changing selectable column names and resetting the preoptimization.
function changeCSV() {
    clearAllPreopt()

    // create option to select classification column
    const csvFileName = document.getElementById("csvFile").files[0].name;

    dict_values = { "csvFileName": csvFileName };

    const sent_data = JSON.stringify(dict_values)

    $.ajax({
        url: "/experiments/getCSVColumnTitles",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (Results) {

            columnTitles = [];

            for (var title in Results["Tiltes"]) {
                columnTitles.push(Results["Tiltes"][title]);
            }

            ID_section = document.getElementById("class_col_section");
            ID_section.innerHTML = "";

            // create the initial option to choose a column for classifying.
            // label
            var name_label = "Class column:";
            var label = document.createElement('label')
            label.htmlFor = name_label;
            label.appendChild(document.createTextNode(name_label));
            let id_info = "Class_Col_Info";

            ID_section.appendChild(label);

            // Create popup information.
            let newDiv = document.createElement("div");
            newDiv.className = "popup";
            newDiv.onclick = function () { popupInformation(id_info); };

            let newImage = document.createElement("img");
            newImage.src = "../../static/Images/information_icon.png";
            newImage.width = "20";
            newImage.height = "20";

            newDiv.appendChild(newImage);

            let newSpan = document.createElement("span");
            newSpan.style = "white-space: pre-wrap";
            newSpan.className = "popuptext";
            newSpan.id = id_info;
            newSpan.textContent = "The column that contains the information to classify.";

            newDiv.appendChild(newSpan);

            ID_section.appendChild(newDiv);

            select = document.createElement('select');
            select.id = "class_col";
            select.name = "class_col";

            // Possible choises, (I.E. column titles)
            for (title in columnTitles) {
                newOption = document.createElement('option');
                optionText = document.createTextNode(columnTitles[title]);

                newOption.appendChild(optionText);
                newOption.setAttribute('value', columnTitles[title]);

                select.appendChild(newOption);
            }

            // add to section
            ID_section.appendChild(select);

            $("#kde_Input").show();
            document.getElementById("kde_ind").value = "";
        }
    });
}

function clearAllCSV() {

}