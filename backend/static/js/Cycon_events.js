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



function changeAlgorithm(algorithms, Parameters) {
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
            var s1 = document.getElementById(Parameters);
            s1.innerHTML = "";

            for (var Parameter in data) {
                //document.getElementById("Results").innerHTML += data[Parameter]["Name"] + " ";

                var Parameter_Name = data[Parameter]["Name"];
                var s1 = document.getElementById(Parameters);

                if (data.hasOwnProperty(Parameter)) {
                    // Create a checkbox to select to alter parameter from default.
                    var pair = data[Parameter]["Name"];
                    var checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.name = pair;
                    checkbox.value = pair;
                    s1.appendChild(checkbox);

                    // Create a label, which will be the parameter Name followed by the default value.
                    var name_label = pair + " (Default: " + data[Parameter]["Default"] + ") ";
                    var label = document.createElement('label');
                    label.htmlFor = name_label;
                    label.appendChild(document.createTextNode(name_label));
                    let id_info = data[Parameter]["Name"] + "_Info";

                    s1.appendChild(label);

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

                    s1.appendChild(newDiv);

                    //document.getElementById("Results").innerHTML += data[Parameter]["Possible"] + " ";
                    //document.getElementById("Results").innerHTML += data[Parameter]["Possible"][0] + " ";


                    for (var Type_Int in data[Parameter]["Type"]) {
                        //document.getElementById("Results").innerHTML += data[Parameter]["Type"] + " ";
                        //document.getElementById("Results").innerHTML += data[Parameter]["Type"][Type_Int] + " ";


                        if (data[Parameter]["Type"][Type_Int] == "option") {
                            for (var Option_Int in data[Parameter]["Possible"]) {
                                // create radio button
                                var radio_name = pair + "_Input";
                                var option = data[Parameter]["Possible"][Option_Int];
                                var radio = document.createElement("input");
                                radio.type = "radio";
                                radio.name = radio_name;
                                radio.id = option;
                                radio.value = option;
                                s1.appendChild(radio);

                                // create label for radio button
                                var name_label = option;
                                var label = document.createElement('label')
                                label.htmlFor = name_label;
                                label.appendChild(document.createTextNode(name_label));

                                s1.appendChild(label);
                            }
                        }

                        if (data[Parameter]["Type"][Type_Int] == "option_float") {
                            for (var Option_Int in data[Parameter]["Possible"]) {
                                // create radio button
                                var radio_name = pair + "_Input";
                                var option = data[Parameter]["Possible"][Option_Int];
                                var radio = document.createElement("input");
                                radio.type = "radio";
                                radio.name = radio_name;
                                radio.id = option;
                                radio.value = option;
                                s1.appendChild(radio);

                                // create label for radio button
                                var name_label = option;
                                var label = document.createElement('label')
                                label.htmlFor = name_label;
                                label.appendChild(document.createTextNode(name_label));

                                s1.appendChild(label);

                                if (option == "float") {
                                    var selection = pair + "_Float_Input";
                                    var textbox = document.createElement("input");
                                    textbox.type = "text";
                                    textbox.name = selection;
                                    s1.appendChild(textbox);
                                }
                            }
                        }

                        // Input of type int will create a textbox.
                        else if (data[Parameter]["Type"][Type_Int] == "int") {

                            var selection = pair + "_Input";
                            var textbox = document.createElement("input");
                            textbox.type = "text";
                            textbox.name = selection;
                            s1.appendChild(textbox);
                        }

                        else if (data[Parameter]["Type"][Type_Int] == "int_or_null") {

                            var selection = pair + "_Input";
                            var textbox = document.createElement("input");
                            textbox.type = "text";
                            textbox.name = selection;
                            s1.appendChild(textbox);
                        }

                        else if (data[Parameter]["Type"][Type_Int] == "float_or_null") {

                            var selection = pair + "_Input";
                            var textbox = document.createElement("input");
                            textbox.type = "text";
                            textbox.name = selection;
                            s1.appendChild(textbox);
                        }

                        else if (data[Parameter]["Type"][Type_Int] == "float") {

                            var selection = pair + "_Input";
                            var textbox = document.createElement("input");
                            textbox.type = "text";
                            textbox.name = selection;
                            s1.appendChild(textbox);
                        }

                        else if (data[Parameter]["Type"][Type_Int] == "bool") {
                            for (var Option_Int in data[Parameter]["Possible"]) {
                                // create radio button
                                var radio_name = pair + "_Input";
                                var option = data[Parameter]["Possible"][Option_Int];
                                var radio = document.createElement("input");
                                radio.type = "radio";
                                radio.name = radio_name;
                                radio.id = option;
                                radio.value = option;
                                s1.appendChild(radio);

                                // create label for radio button
                                var name_label = option;
                                var label = document.createElement('label')
                                label.htmlFor = name_label;
                                label.appendChild(document.createTextNode(name_label));

                                s1.appendChild(label);
                            }
                        }

                        else if (data[Parameter]["Type"][Type_Int] == "string") {

                            var selection = pair + "_Input";
                            var textbox = document.createElement("input");
                            textbox.type = "text";
                            textbox.name = selection;
                            s1.appendChild(textbox);
                        }
                        else if (data[Parameter]["Type"][Type_Int] == "equation") {

                            var selection = pair + "_Input";
                            var textbox = document.createElement("input");
                            textbox.type = "text";
                            textbox.name = selection;
                            s1.appendChild(textbox);
                        }
                    }

                    s1.appendChild(document.createElement("br"));
                }
            }
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

    //document.getElementById("StatusInfo").innerHTML = "Processing...";

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

                document.getElementById("Results").innerHTML = "Test 3";
                // obtain the Metrics
                Accuracy = Results["Accuracy"]
                F1 = Results["F1"]
                F1_micro = Results["F1_micro"]
                F1_macro = Results["F1_macro"]
                Precision = Results["Precision"]
                Precision_micro = Results["Precision_micro"]
                Precision_macro = Results["Precision_macro"]
                Conf_Matrix = Results["cm_overall"]

                document.getElementById("Results").innerHTML = "Test 4";

                // display the metrics
                var img = new Image();

                img.src = "data:image/png;base64," + Results["cm_overall"];

                document.getElementById("Results").innerHTML = "Test 5";

                writeData.paragraph += '=========================Results=========================<br\>'
                writeData.paragraph +=  Results["Accuracy_Intro"].bold() + Results["Accuracy"] + '<br\>' 
                writeData.paragraph += Results["Precision_Intro"].bold() + Results["Precision"] + "<br\>" 
                writeData.paragraph += Results["Precision_micro_Intro"].bold() + Results["Precision_micro"] + "<br\>" 
                writeData.paragraph += Results["Precision_macro_Intro"].bold() + Results["Precision_macro"] + "<br\>" 
                writeData.paragraph += Results["F1_Intro"].bold() + Results["F1"] + "<br\>" 
                writeData.paragraph += Results["F1_micro_Intro"].bold() + Results["F1_micro"] + "<br\>" 
                writeData.paragraph += Results["F1_macro_Intro"].bold() + Results["F1_macro"] + "<br\>" 
                writeData.paragraph += `${img.outerHTML}`

                document.getElementById("Results").innerHTML = "Test 6";

                //$('#Results').html(data.paragraph);
                document.getElementById("Results").innerHTML = writeData.paragraph;
            }

            else if (Results['Validation'] == "K-Fold") {

                document.getElementById("Results").innerHTML = "Testing 1";

                for (let i = 0; i < Results["acc_list"].length; i++) {
                    writeData.paragraph += '=========================Results for Fold ' + i + '=========================<br\>'
                    writeData.paragraph += Results["Accuracy_Intro"].bold() + Results["acc_list"][i] + '<br\>'
                    writeData.paragraph += Results["Precision_Intro"].bold() + Results["prec_list"][i] + '<br\>'
                    writeData.paragraph += Results["Precision_micro_Intro"].bold() + Results["prec_micro_list"][i] + '<br\>'
                    writeData.paragraph += Results["Precision_macro_Intro"].bold() + Results["prec_macro_list"][i] + '<br\>'
                    writeData.paragraph += Results["F1_Intro"].bold() + Results["f1_list"][i] + '<br\>'
                    writeData.paragraph += Results["F1_micro_Intro"].bold() + Results["f1_micro_list"][i] + '<br\>'
                    writeData.paragraph += Results["F1_macro_Intro"].bold() + Results["f1_macro_list"][i] + '<br\>'

                    document.getElementById("Results").innerHTML = "Testing 2";
                    var img = new Image();
                    img.src = 'data:image/jpeg;base64,' + Results["cm_list"][i];

                    writeData.paragraph += `${img.outerHTML} <br\>`

                    document.getElementById("Results").innerHTML = "Test 3";
                }

                document.getElementById("Results").innerHTML = "Test 4";

                writeData.paragraph += '<br\>'
                writeData.paragraph += '=========================Results Overall=========================<br\>'
                writeData.paragraph += Results["Accuracy_Intro_Overall"].bold() + Results["acc_average"] + '<br\>'
                writeData.paragraph += Results["Precision_Intro_Overall"].bold() + Results["prec_average"] + '<br\>'
                writeData.paragraph += Results["Precision_micro_Intro_Overall"].bold() + Results["prec_micro_average"] + '<br\>'
                writeData.paragraph += Results["Precision_macro_Intro_Overall"].bold() + Results["prec_macro_average"] + '<br\>'
                writeData.paragraph += Results["F1_Intro_Overall"].bold() + Results["f1_average"] + '<br\>'
                writeData.paragraph += Results["F1_micro_Intro_Overall"].bold() + Results["f1_micro_average"] + '<br\>'
                writeData.paragraph += Results["F1_macro_Intro_Overall"].bold() + Results["f1_macro_average"] + '<br\>'

                document.getElementById("Results").innerHTML = "Test 5";

                var img = new Image();
                img.src = 'data:image/jpeg;base64,' + Results['cm_overall'];

                writeData.paragraph += `${img.outerHTML} <br\>`

                document.getElementById("Results").innerHTML = "Test 6";

                document.getElementById("Results").innerHTML = writeData.paragraph;
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

                document.getElementById("Results").innerHTML = "Testing 1";

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
    document.getElementById("csv_Results").innerHTML = "";

    var formData = new FormData(form);

    var dict_data = {};

    const projectName = document.getElementById("projectName").value;
    formData.append("projectName", projectName);

    const csvFileName = document.getElementById("csvFile").files[0].name;
    formData.append("csvFileName", csvFileName);

    var checkbox = $("#csvForm").find("input[type=checkbox]");
    $.each(checkbox, function (key, val) {
        formData.append($(val).attr('name') + "_checked", $(this).is(':checked'));
    });

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("csv_Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json
    dict_values = { "form": dict_data };

    const sent_data = JSON.stringify(dict_values)

    $.ajax({
        url: "/experiments/getCSVResults",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (Results) {

            var writeData = {
                paragraph: ''
            }

            document.getElementById("csv_Results").innerHTML = Results['csv_Short'];
            document.getElementById("csv_Null_Results").innerHTML = Results['null_Count']

            if (dict_values["class_col"] != "") {
                document.getElementById("csv_Class_Balance_Results").innerHTML = Results['Number_Classes'];
            }

            if (dict_values["kde_ind"] != "") {
                if (dict_values["class_col"] != "") {
                    for (i in Results["kde_plots"]) {
                        var img = new Image();
                        img.src = 'data:image/jpeg;base64,' + Results["kde_plots"][i];

                        document.getElementById("csv_Scale_Results").innerHTML += `${img.outerHTML}`
                    }
                }
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var writeData = {
                paragraph: ''
            }

            writeData.paragraph += "ERROR: "

            writeData.paragraph += textStatus

            document.getElementById("csv_Results").innerHTML = writeData.paragraph;
        }
    });
}

document.getElementById("csvForm").addEventListener("submit", function (e) {
    e.preventDefault();
    checkCSV(e.target);
});