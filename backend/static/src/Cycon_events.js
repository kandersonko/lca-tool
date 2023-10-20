var preoptCounter = 0;
var layerCounter = 0;
var callbackCounter = 0;
var columnTitles = [];

// Indicatiors is callback is already chosen to be used.
var Using_EarlyStopping = false;
var Using_ReduceLROnPlateau = false;

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

function changeLayerCategory(category, ID_Layers) {
    var category_selection = document.getElementById(category)
    var category_name = category_selection.value

    dict_values = { Category: category_name };

    const sent_data = JSON.stringify(dict_values)

    $.ajax({
        url: "/experiments/getCategoryLayers",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(sent_data),
        async: false,
        dataType: 'json',
        success: function (data) {
            select = document.getElementById(ID_Layers);
            select.options.length = 0;
            // Remove existing options in the selection
            var len = select.length;
            for (var i = 0; i < len; i++) {
                select.remove(0);
            }

            // For each preoptimization in the category, create a selection possibility.
            for (var Layer in data) {
                var Layer_Name = data[Layer]["Name"];
                var Layer_Display_Name = data[Layer]["Display_Name"];

                if (data.hasOwnProperty(Layer)) {
                    newOption = document.createElement('option');
                    optionText = document.createTextNode(Layer_Display_Name);

                    newOption.appendChild(optionText);
                    newOption.setAttribute('value', Layer_Name);

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
                    var name_label = Parameter_Name + " (Default: " + data[Parameter]["Default_value"] + ") ";
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

                    fillSection(field, data, Parameter, ID_Parameters, 0,)
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

function getData(files, fileSelected, choice) {
    const form = document.getElementById("MLAI_Form");
    console.log("get form :", form, files, choice, fileSelected);
    // Copy over information from element outside of form to the copy inside form
    document.getElementById("projectName_copy").value = document.getElementById("projectName").value;
    document.getElementById("phase1Text_copy").value = document.getElementById("phase1Text").value;
    document.getElementById("csvFile_copy").value = document.getElementById("csvFile").value;

    // Collect all form data instances
    var formData = new FormData(form);

    var dict_data = {};

    const class_column = document.getElementById("class_col").value;
    formData.append("class_col", class_column);

    formData.append("preoptCounter", preoptCounter)
    formData.append("layerCounter", layerCounter)
    formData.append("callbackCounter", callbackCounter)

    //var checkbox = $("#cyconForm").find("input[type=checkbox]");
    //$.each(checkbox, function (key, val) {
    //    formData.append($(val).attr('name') + "_checked", $(this).is(':checked'));
    //});

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    // Preoptimization form
    const preoptform = document.getElementById("preoptForm");

    var preoptForm = new FormData(preoptform);

    // iterate through entries...
    for (var pair of preoptForm.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    // Methodology form
    const methodform = document.getElementById("methodologyForm");

    var methodForm = new FormData(methodform);

    // iterate through entries...
    for (var pair of methodForm.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    // MLA form
    const mla_form = document.getElementById("MLA_Form");

    var mla_Form = new FormData(mla_form);

    // iterate through entries...
    for (var pair of mla_Form.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    // DLANN form
    const dlann_form = document.getElementById("DLANN_Form");

    var dlann_Form = new FormData(dlann_form);

    // iterate through entries...
    for (var pair of dlann_Form.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    // Model Compile Form
    const model_compile_form = document.getElementById("Model_Compile_Form");

    var model_compile_Form = new FormData(model_compile_form);

    // iterate through entries...
    for (var pair of model_compile_Form.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    // Model Validation Form
    const model_val_form = document.getElementById("Model_Validation_Form");

    var model_val_Form = new FormData(model_val_form);

    // iterate through entries...
    for (var pair of model_val_Form.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json

    // const csvFileName = document.getElementById("csvFile").files[0].name;
    // const csvFile = document.getElementById("csvFile").files[0];
    let csvFileName;
    let csvFile;
    // create option to select classification column
    if(choice === "Choose uploaded file") {
        const foundFile = files.find(f => f.filename === fileSelected);
        const data = JSON.parse(JSON.stringify(foundFile.content));
        console.log("data: ", data, );

        // Create CSV content
        const csvContent = createCSV(data);

        // Create Blob from CSV content
        const csvBlob = createCSVBlob(csvContent);

        csvFileName = fileSelected;
        csvFile = csvBlob;

        console.log("get csv: ", csvFile, csvBlob)
    } else {
        csvFileName = document.getElementById("csvFile").files[0].name;
        csvFile = document.getElementById("csvFile").files[0];
    }
    console.log("getData", files, fileSelected, csvFile);


    const data = new FormData();
    data.append("processes", JSON.stringify(dict_data))
    data.append("csvFileName", csvFileName)
    data.append("csvFile", csvFile)

    $.ajax({
        url: "/experiments/run_experiment",
        data: data,
        type: "POST",
        dataType: 'json',
        processData: false, // important
        contentType: false, // important,
        success: function (Results) {
            document.getElementById("Results").innerHTML += "Hello?";
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
                writeData.paragraph += "Dataset File: ".bold().italics() + "<br\>" + csvFileName + "<br\><br\>"
                // Preoptimization
                writeData.paragraph += "Preoptimization: ".bold().italics() + "<br\>"
                for (let i = 0; i < preoptCounter; i++) {
                    writeData.paragraph += dict_data["Preopt_" + i] + "<br\>"
                }
                writeData.paragraph += "<br\>"
                // Phase 3
                // Name of Methology
                writeData.paragraph += "Methodology Information".bold().italics().big() + "<br\>"
                writeData.paragraph += "Name of Methodology: ".bold().italics() + "<br\>" + dict_data["methodology"] + "<br\><br\>"

                // Information to provide for MLA
                if (dict_data["methodology"] == "MLA") {

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
                        writeData.paragraph += `${img.outerHTML}` + "<br\>"

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
                    document.getElementById("Results").innerHTML = writeData.paragraph;
                        document.getElementById("Results").innerHTML = writeData.paragraph;
                    }
                }

                // Information to provide for DLANN"
                if (dict_data["methodology"] == "DLANN") {
                    // Neural Network information
                    writeData.paragraph += "Neural Network: ".bold().italics() + "<br\>"
                    for (let i = 0; i < layerCounter; i++) {
                        writeData.paragraph += dict_data["Layer_" + i] + "<br\>"
                    }
                    writeData.paragraph += "<br\>"

                    // Validation
                    writeData.paragraph += "Validation:".bold().italics() + "<br\>"
                    writeData.paragraph += "Test Split: ".bold() + dict_data["Validation_test_split_Input"] + "<br\>"
                    writeData.paragraph += "Validation Split: ".bold() + dict_data["Validation_validation_split_Input"] + "<br\>"
                    writeData.paragraph += "Random State: ".bold() + dict_data["Validation_random_state_Input"] + "<br\>"
                    writeData.paragraph += "Shuffle Before Split: ".bold() + dict_data["Validation_shuffle_before_split_Input"] + "<br\>"
                    writeData.paragraph += "Shuffle Before Epoch: ".bold() + dict_data["Validation_shuffle_before_epoch_Input"] + "<br\>"
                    writeData.paragraph += "Batch Size: ".bold() + dict_data["Validation_batch_size_Input"] + "<br\>"
                    writeData.paragraph += "Verbose: ".bold() + dict_data["Validation_verbose_Input"] + "<br\>"


                    writeData.paragraph += "<br\>"
                    writeData.paragraph += "Callbacks: ".bold().italics() + "<br\>"
                    for (let i = 0; i < callbackCounter; i++) {
                        writeData.paragraph += dict_data["Callback_" + i] + "<br\>"
                    }

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
                        writeData.paragraph += `${img.outerHTML}` + "<br\>"

                        var img_1 = new Image();
                        img_1.src = "data:image/png;base64," + Results["acc_history"];
                        writeData.paragraph += `${img_1.outerHTML}` + "<br\>"

                        var img_2 = new Image();
                        img_2.src = "data:image/png;base64," + Results["loss_history"];
                        writeData.paragraph += `${img_2.outerHTML}` + "<br\>"


                        //$('#Results').html(data.paragraph);
                        document.getElementById("Results").innerHTML = writeData.paragraph;
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

                document.getElementById("Results").innerHTML = writeData.paragraph;
            }
        }
    });
}

// document.getElementById("cyconForm").addEventListener("submit", function (e) {
//     e.preventDefault();
//     getData(e.target);
// });



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
                    writeData.paragraph += Results["Precision_Intro"].bold() + Results["Precision"] + "<br\>"
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
                    writeData.paragraph += `${img.outerHTML}` + "<br\>"
                }

                if (dict_data["methodology"] == "DLANN") {
                    var img = new Image();

                    img.src = "data:image/png;base64," + Results["acc_history"];

                    writeData.paragraph += `${img.outerHTML}` + "<br\>"

                    var img = new Image();

                    img.src = "data:image/png;base64," + Results["loss_history"];

                    writeData.paragraph += `${img.outerHTML}` + "<br\>"
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
    });

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
function checkCSV(files, fileSelected, choice) {
    const form = document.getElementById("csvForm");
    document.getElementById("csv_Error").innerHTML = "";
    document.getElementById("csv_Results").innerHTML = "";

    var formData = new FormData(form);

    var dict_data = {};

    const projectName = document.getElementById("projectName").value;
    formData.append("projectName", projectName);

    formData.append("Perform_Preopt", "No")

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        //document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json

    $("#csv_Title").hide();
    $("#csv_Null_Title").hide();
    $("#csv_Null_Results").hide();
    $("#csv_Class_Balance_Title").hide();
    $("#csv_Class_Balance_Results").hide();
    $("#csv_Scale_Title").hide();
    $("#csv_Scale_Results").hide();

    // const csvFileName = document.getElementById("csvFile").files[0].name;
    // const csvFile = document.getElementById("csvFile").files[0];

    let csvFileName;
    let csvFile;
    // create option to select classification column
    if(choice === "Choose uploaded file") {
        const foundFile = files.find(f => f.filename === fileSelected);
        const data = JSON.parse(JSON.stringify(foundFile.content));
        console.log("data: ", data, );

        // Create CSV content
        const csvContent = createCSV(data);

        // Create Blob from CSV content
        const csvBlob = createCSVBlob(csvContent);

        csvFileName = fileSelected;
        csvFile = csvBlob;

        console.log("created csv: ", csvFile, csvBlob)
    } else {
        csvFileName = document.getElementById("csvFile").files[0].name;
        csvFile = document.getElementById("csvFile").files[0];
    }
    console.log("changeCSV", files, fileSelected, csvFile);


    const data = new FormData();
    data.append("processes", JSON.stringify(dict_data))
    data.append("csvFileName", csvFileName)
    data.append("csvFile", csvFile)

    //document.getElementById("Results").innerHTML += data;

    $.ajax({
        url: "/experiments/getCSVResults",
        data: data,
        type: "POST",
        dataType: 'json',
        processData: false, // important
        contentType: false, // important,
        success: function (Results) {
            if (Results[0] == "worked") {

                Results = Results[2]

                var writeData = {
                    paragraph: ''
                }

                document.getElementById("csv_Results").innerHTML = Results['csv_Short'];
                document.getElementById("csv_Null_Results").innerHTML = Results['null_Count']

                $("#csv_Title").show();
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

    const class_column = document.getElementById("class_col").value;
    formData.append("class_col", class_column);

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

    $("#csv_Title_Preopt").hide();
    $("#csv_Null_Title_Preopt").hide();
    $("#csv_Null_Results_Preopt").hide();
    $("#csv_Class_Balance_Title_Preopt").hide();
    $("#csv_Class_Balance_Results_Preopt").hide();
    $("#csv_Scale_Title_Preopt").hide();
    $("#csv_Scale_Results_Preopt").hide();

    const csvFileName = document.getElementById("csvFile").files[0].name;
    const csvFile = document.getElementById("csvFile").files[0];

    const data = new FormData();
    data.append("processes", JSON.stringify(dict_data))
    data.append("csvFileName", csvFileName)
    data.append("csvFile", csvFile)

    document.getElementById("Results").innerHTML += data;

    $.ajax({
        url: "/experiments/getCSVResults",
        data: data,
        type: "POST",
        dataType: 'json',
        processData: false, // important
        contentType: false, // important,
        success: function (Results) {
            if (Results[0] == "worked") {

                Results = Results[2]

                var writeData = {
                    paragraph: ''
                }

                document.getElementById("csv_Results_Preopt").innerHTML = Results['csv_Short'];
                document.getElementById("csv_Null_Results_Preopt").innerHTML = Results['null_Count']

                $("#csv_Title_Preopt").show();
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
    if (preoptSubmit == 'Check') {
        checkCSV_Preopt(e.target);
    } else if (preoptSubmit == 'Download') {
        downloadCSV(e.target);
    } else {
        //invalid action!
    }
});

var preoptSubmit = ""

function changePreoptSubmit(value) {
    preoptSubmit = value
}

function downloadCSV(form) {
    var fileName = "CyberTraining.csv";

    document.getElementById("csv_Error_Preopt").innerHTML = "";
    document.getElementById("csv_Results_Preopt").innerHTML = "";

    var formData = new FormData(form);
    var csvFormData = new FormData(document.getElementById("csvForm"));

    var dict_data = {};

    const projectName = document.getElementById("projectName").value;
    formData.append("projectName", projectName);

    const class_column = document.getElementById("class_col").value;
    formData.append("class_col", class_column);

    formData.append("Perform_Preopt", "Yes")

    formData.append("preoptCounter", preoptCounter)

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        //document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    for (var pair of csvFormData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        //document.getElementById("Results").innerHTML += pair[0] + ": " + pair[1] + "<br\>";
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json

    const csvFileName = document.getElementById("csvFile").files[0].name;
    const csvFile = document.getElementById("csvFile").files[0];

    const data = new FormData();
    data.append("processes", JSON.stringify(dict_data))
    data.append("csvFileName", csvFileName)
    data.append("csvFile", csvFile)

    $.ajax({
        url: "/experiments/downloadCSV",
        data: data,
        type: "POST",
        dataType: 'json',
        processData: false, // important
        contentType: false, // important,
        success: function (Results) {
            if (Results[0] == "worked") {
                Results = Results[2]

                var element = document.createElement('a');
                element.setAttribute('href', Results["csv_data"]);
                element.setAttribute('download', fileName);

                document.body.appendChild(element);

                element.click();

                document.body.removeChild(element);

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



// Addes the selected preoptimization to the form. 
function selectPreopt(Preopt, ID_Preopt) {
    if (preoptCounter != 10) {

        var Preopt_selection = document.getElementById(Preopt)
        var Preopt_name = Preopt_selection.options[Preopt_selection.selectedIndex].text
        var Preopt_value = Preopt_selection.value
        //document.getElementById("Results").innerHTML = method_name

        dict_values = { Preopt: Preopt_value };

        const sent_data = JSON.stringify(dict_values)

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
                        var name_label = Parameter_Name + " (Default: " + data[Parameter]["Default_value"] + ") ";
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

// Addes the selected preoptimization to the form. 
function selectCallback(Callback, ID_Callback) {
    var Callback_selection = document.getElementById(Callback)
    var Callback_name = Callback_selection.options[Callback_selection.selectedIndex].text
    var Callback_value = Callback_selection.value

    var addCallback = false;

    document.getElementById("Results").innerHTML = Callback_value

    // Check if the callback has already been added, if not add it, if so do nothing.
    if (Callback_value == "EarlyStopping") {
        if (!Using_EarlyStopping) {
            addCallback = true;
        }
    }
    if (Callback_value == "ReduceLROnPlateau") {
        if (!Using_ReduceLROnPlateau) {
            addCallback = true;
        }
    }

    // Continue to obtain the callback information.
    if (addCallback) {

        //document.getElementById("Results").innerHTML = method_name

        dict_values = { Callback: Callback_value };

        const sent_data = JSON.stringify(dict_values)

        // Get the parameters for the selected Preopt option.
        $.ajax({
            url: "/experiments/getCallbackParameters",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(sent_data),
            async: false,
            dataType: 'json',
            success: function (data) {
                // Create the html section to place in the cycon page.
                var html_section = document.getElementById(ID_Callback);

                // create the field box for the new preopt option.
                var field = document.createElement('fieldset');
                // create title for the field.
                var legend = document.createElement('legend');
                legend_text = document.createTextNode(Callback_name);
                legend.appendChild(legend_text);
                field.appendChild(legend);

                // Create a hidden value that will contain the selected parameter name.
                var textbox = document.createElement("input");
                textbox.type = "text";
                textbox.name = "Callback_" + callbackCounter;
                textbox.value = Callback_value;
                textbox.style.display = "none";

                field.appendChild(textbox);

                // Create option to edit the parameter for the preoptimization option.
                for (var Parameter in data) {

                    var Parameter_Name = data[Parameter]["Name"];

                    if (data.hasOwnProperty(Parameter)) {
                        // Create a label, which will be the parameter Name followed by the default value.
                        var name_label = Parameter_Name + " (Default: " + data[Parameter]["Default_value"] + ") ";
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

                        fillSection(field, data, Parameter, "Callback", callbackCounter)
                    }
                }
                // TO DO LATER: Add button to remove the individual preoptimization parameter.

                // add field to div section
                html_section.appendChild(field)

                // Change the indication that the callback is in use.
                if (Callback_value == "EarlyStopping") {
                    if (!Using_EarlyStopping) {
                        Using_EarlyStopping = true;
                    }
                }
                if (Callback_value == "ReduceLROnPlateau") {
                    if (!Using_ReduceLROnPlateau) {
                        Using_ReduceLROnPlateau = true;
                    }
                }
            }
        });

        callbackCounter = callbackCounter + 1;
    }
}

function getCompilerOptions(ID_Compiler) {
    document.getElementById(ID_Compiler).innerHTML = "";

    $.ajax({
        url: "/experiments/getCompilerOptions",
        type: "POST",
        contentType: "application/json",
        async: false,
        dataType: 'json',
        success: function (data) {
            // Create the html section to place in the cycon page.
            var html_section = document.getElementById(ID_Compiler);

            // create the field box for the new layer option.
            var field = document.createElement('fieldset');
            // create title for the field.
            var legend = document.createElement('legend');
            legend_text = document.createTextNode("Compiler");
            legend.appendChild(legend_text);
            field.appendChild(legend);

            // Create option to edit the parameter for the NN layer option.
            for (var Parameter in data["Parameters"]) {
                //document.getElementById("Results").innerHTML += "<br><br>"
                //document.getElementById("Results").innerHTML += data["Parameters"][Parameter]["Name"]
                //document.getElementById("Results").innerHTML += data["Parameters"][Parameter]["Default_value"]
                //document.getElementById("Results").innerHTML += data["Parameters"][Parameter]["Definition"]


                //var Parameter_Name = data["Parameters"][Parameter]["Name"];

                if (data["Parameters"].hasOwnProperty(Parameter)) {
                    // Create a label, which will be the parameter Name followed by the default value.
                    var name_label = data["Parameters"][Parameter]["Name"] + " (Default: " + data["Parameters"][Parameter]["Default_value"] + ") ";
                    var label = document.createElement('label');
                    label.htmlFor = name_label;
                    label.appendChild(document.createTextNode(name_label));
                    let id_info = data["Parameters"][Parameter]["Name"] + "_Info";

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

                    newSpan = document.createElement("span");
                    newSpan.style = "white-space: pre-wrap";
                    newSpan.className = "popuptext";
                    newSpan.id = id_info;
                    newSpan.textContent = data["Parameters"][Parameter]["Definition"];

                    newDiv.appendChild(newSpan);

                    field.appendChild(newDiv);

                    // Create choices and options to edit the parameter
                    fillSection(field, data["Parameters"], Parameter, "Compiler", 0)
                }
            }

            // add field to div section
            html_section.appendChild(field)
        }
    });
}

// Obtains and fills out the validation section for the DLANN
function getValidationOptions(ID_Val) {
    document.getElementById(ID_Val).innerHTML = "";

    $.ajax({
        url: "/experiments/getValidationOptions",
        type: "POST",
        contentType: "application/json",
        async: false,
        dataType: 'json',
        success: function (data) {
            // Create the html section to place in the cycon page.
            var html_section = document.getElementById(ID_Val);

            // create the field box for the new layer option.
            var field = document.createElement('fieldset');
            // create title for the field.
            var legend = document.createElement('legend');
            legend_text = document.createTextNode("Validation");
            legend.appendChild(legend_text);
            field.appendChild(legend);

            // Create option to edit the parameter for the NN layer option.
            for (var Parameter in data["Parameters"]) {

                if (data["Parameters"].hasOwnProperty(Parameter)) {
                    // Create a label, which will be the parameter Name followed by the default value.
                    var name_label = data["Parameters"][Parameter]["Name"] + " (Default: " + data["Parameters"][Parameter]["Default_value"] + ") ";
                    var label = document.createElement('label');
                    label.htmlFor = name_label;
                    label.appendChild(document.createTextNode(name_label));
                    let id_info = data["Parameters"][Parameter]["Name"] + "_Info";

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

                    newSpan = document.createElement("span");
                    newSpan.style = "white-space: pre-wrap";
                    newSpan.className = "popuptext";
                    newSpan.id = id_info;
                    newSpan.textContent = data["Parameters"][Parameter]["Definition"];

                    newDiv.appendChild(newSpan);

                    field.appendChild(newDiv);

                    // Create choices and options to edit the parameter
                    fillSection(field, data["Parameters"], Parameter, "Validation", 0)
                }
            }

            // add field to div section
            html_section.appendChild(field)
        }
    });
}

// Addes the selected layer to the form. 
function selectLayers(Layer, ID_Layer) {
    if (layerCounter != 20) {

        var Layer_selection = document.getElementById(Layer)
        var Layer_name = Layer_selection.options[Layer_selection.selectedIndex].text
        var Layer_value = Layer_selection.value
        //document.getElementById("Results").innerHTML = method_name

        dict_values = { Layer: Layer_value };

        const sent_data = JSON.stringify(dict_values)

        // Get the parameters for the selected layer option.
        $.ajax({
            url: "/experiments/getLayerParameters",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(sent_data),
            async: false,
            dataType: 'json',
            success: function (data) {
                // Create the html section to place in the cycon page.
                var html_section = document.getElementById(ID_Layer);

                // create the field box for the new layer option.
                var field = document.createElement('fieldset');
                // create title for the field.
                var legend = document.createElement('legend');
                legend_text = document.createTextNode(Layer_name);
                legend.appendChild(legend_text);
                field.appendChild(legend);

                // Create a hidden value that will contain the selected parameter name.
                var textbox = document.createElement("input");
                textbox.type = "text";
                textbox.name = "Layer_" + layerCounter;
                textbox.value = Layer_value;
                textbox.style.display = "none";

                field.appendChild(textbox);

                // Create option to edit the parameter for the NN layer option.
                for (var Parameter in data) {

                    var Parameter_Name = data[Parameter]["Name"];

                    if (data.hasOwnProperty(Parameter)) {
                        // Create a label, which will be the parameter Name followed by the default value.
                        var name_label = Parameter_Name + " (Default: " + data[Parameter]["Default_value"] + ") ";
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

                        fillSection(field, data, Parameter, "Layer", layerCounter)
                    }
                }
                // TO DO LATER: Add button to remove the individual NN layer.

                // add field to div section
                html_section.appendChild(field)

            }
        });

        layerCounter = layerCounter + 1;
    }
}

// Removes all csv check information
function clearAllCSV() {
    document.getElementById("csv_Error_Preopt").innerHTML = "";

    document.getElementById("csv_Results").innerHTML = "";
    document.getElementById("csv_Null_Results").innerHTML = "";
    document.getElementById("csv_Class_Balance_Results").innerHTML = "";
    document.getElementById("csv_Scale_Results").innerHTML = "";

    $("#csv_Title").hide();
    $("#csv_Null_Title").hide();
    $("#csv_Null_Results").hide();
    $("#csv_Class_Balance_Title").hide();
    $("#csv_Class_Balance_Results").hide();
    $("#csv_Scale_Title").hide();
    $("#csv_Scale_Results").hide();
}

// Removes all preoptimization options.
function clearAllPreopt() {
    document.getElementById("Preopt_Selection").innerHTML = "";
    preoptCounter = 0;

    document.getElementById("csv_Results_Preopt").innerHTML = "";
    document.getElementById("csv_Null_Results_Preopt").innerHTML = "";
    document.getElementById("csv_Class_Balance_Results_Preopt").innerHTML = "";
    document.getElementById("csv_Scale_Results_Preopt").innerHTML = "";

    $("#csv_Title_Preopt").hide();
    $("#csv_Null_Title_Preopt").hide();
    $("#csv_Null_Results_Preopt").hide();
    $("#csv_Class_Balance_Title_Preopt").hide();
    $("#csv_Class_Balance_Results_Preopt").hide();
    $("#csv_Scale_Title_Preopt").hide();
    $("#csv_Scale_Results_Preopt").hide();
}

// Removes all callback options.
function clearAllCallbacks() {
    document.getElementById("Callback_Selection").innerHTML = "";
    callbackCounter = 0;

    Using_EarlyStopping = false;
    Using_ReduceLROnPlateau = false;
}

// Removes all layer options.
function clearAllNN() {
    document.getElementById("Layers_Selection").innerHTML = "";
    layerCounter = 0;
}


// Method to fill an html paragraph or section via the parameters
function fillSection(section, data, Parameter, Location, counter) {

    var default_opt = data[Parameter]["Default_option"];
    var default_value = data[Parameter]["Default_value"];

    var Parameter_Name = data[Parameter]["Name"];

    if (Location == "Preopt") {
        Parameter_Name = "Preopt_" + counter + "_" + data[Parameter]["Name"];
    }

    else if (Location == "Layer") {
        Parameter_Name = "Layer_" + counter + "_" + data[Parameter]["Name"];
    }

    else if (Location == "Callback") {
        Parameter_Name = "Callback_" + counter + "_" + data[Parameter]["Name"];
    }

    else if (Location == "Compiler" || Location == "Validation") {
        Parameter_Name = Location + "_" + data[Parameter]["Name"];
    }

    else {
        Parameter_Name = data[Parameter]["Name"];
    }



    // Create choices and options to alter the parameter
    for (var Type_Int in data[Parameter]["Type"]) {
        // Selectable options.
        if (data[Parameter]["Type"][Type_Int] == "option" || data[Parameter]["Type"][Type_Int] == "option_integer" || data[Parameter]["Type"][Type_Int] == "option_dtype") {
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
                if (option == default_opt) {
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

        // Selectable checkboxes for multiple options to be selected.
        if (data[Parameter]["Type"][Type_Int] == "checkbox") {
            for (var Option_Int in data[Parameter]["Possible"]) {
                // create checkbox
                var check_name = Parameter_Name + "_Input";
                var option = data[Parameter]["Possible"][Option_Int];
                var checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.name = checkbox_name;
                checkbox.id = option;
                section.appendChild(checkbox);
                if (option == default_opt) {
                    checkbox.checked = true;
                }

                // create label for radio button
                var name_label = option;
                var label = document.createElement('label')
                label.htmlFor = name_label;
                label.appendChild(document.createTextNode(name_label));

                section.appendChild(label);
            }
        }

        // Selectable options with input types.
        if (data[Parameter]["Type"][Type_Int] == "option_input" || data[Parameter]["Type"][Type_Int] == "option_input_dtype") {
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
                if (option == default_opt) {
                    radio.checked = true;
                }

                // create label for radio button
                var name_label = option;
                var label = document.createElement('label')
                label.htmlFor = name_label;
                label.appendChild(document.createTextNode(name_label));

                section.appendChild(label);

                // set default.
                if (typeof default_value != 'number') {
                    if (option == default_opt) {
                        radio.checked = true;
                    }
                }

                if (typeof default_value == 'number' && !isNaN(default_value)) {
                    if (option == default_opt) {
                        radio.check = true;
                    }
                }

                if (option == "str") {
                    var selection = Parameter_Name + "_String_Input";
                    var textbox = document.createElement("input");
                    textbox.type = "text";
                    textbox.name = selection;
                    textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";
                    section.appendChild(textbox);

                    if (default_opt == 'str') {
                        textbox.value = default_value;
                    }
                }

                if (option == "int") {
                    var selection = Parameter_Name + "_Int_Input";
                    var textbox = document.createElement("input");
                    textbox.type = "text";
                    textbox.name = selection;
                    textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";
                    section.appendChild(textbox);

                    if (default_opt == "int") {
                        if (typeof default_value == 'number' && !isNaN(default_value)) {
                            textbox.value = default_value;
                        }
                    }
                }

                if (option == "float") {
                    var selection = Parameter_Name + "_Float_Input";
                    var textbox = document.createElement("input");
                    textbox.type = "text";
                    textbox.name = selection;
                    textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";
                    section.appendChild(textbox);

                    if (default_opt == "float") {
                        if (typeof default_value == 'number' && !isNaN(default_value)) {
                            textbox.value = default_value;
                        }
                    }
                }
            }
        }

        // Selectable option for a list to be placed in a select element
        if (data[Parameter]["Type"][Type_Int] == "select") {
            if (data[Parameter]["Possible"] == "col_names") {

                select = document.createElement('select');
                select.id = Parameter_Name + "_Input";
                select.name = Parameter_Name + "_Input";
                select.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";

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

                if (typeof default_opt != 'number') {
                    if (option == default_opt) {
                        radio.checked = true;
                    }
                }

                if (typeof default_opt == 'number' && !isNaN(default_opt)) {
                    if (option == "float") {
                        radio.checked = true;
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
                    textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";
                    section.appendChild(textbox);

                    if (typeof default_opt == 'number' && !isNaN(default_opt)) {
                        textbox.value = default_opt;
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

                if (typeof default_opt != 'number') {
                    if (option == default_opt) {
                        radio.checked = true;
                    }
                }

                if (typeof default_opt == 'number' && !isNaN(default_opt)) {
                    if (option == "int") {
                        radio.checked = true;
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
                    textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";
                    section.appendChild(textbox);

                    if (typeof default_opt == 'number' && !isNaN(default_opt)) {
                        textbox.value = default_opt;
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
            textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";

            textbox.value = default_opt;

            section.appendChild(textbox);
        }

        // Integer or null
        else if (data[Parameter]["Type"][Type_Int] == "int_or_null") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;
            textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";

            if (typeof default_opt == 'number' && !isNaN(default_opt)) {
                textbox.value = default_opt;
            }

            section.appendChild(textbox);
        }

        // Float or null
        else if (data[Parameter]["Type"][Type_Int] == "float_or_null") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;
            textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";

            if (typeof default_opt == 'number' && !isNaN(default_opt)) {
                textbox.value = default_opt;
            }

            section.appendChild(textbox);
        }

        // Float only
        else if (data[Parameter]["Type"][Type_Int] == "float") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;

            textbox.value = default_opt;
            textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";

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

                if (option == default_opt) {
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
            textbox.value = data[Parameter]["Default_value"];
            textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";
            section.appendChild(textbox);
        }

        // Equation entry only
        else if (data[Parameter]["Type"][Type_Int] == "equation") {

            var selection = Parameter_Name + "_Input";
            var textbox = document.createElement("input");
            textbox.type = "text";
            textbox.name = selection;
            textbox.className = "w-64 px-2 py-1 border border-gray-400 rounded-lg bg-white";
            section.appendChild(textbox);
        }
        section.appendChild(document.createElement("br"));
    }


    // section.appendChild(document.createElement("br"));
}

// Function to create a CSV file from an array of data
function createCSV(dataArray) {
  const csvContent = dataArray.map(row => row.join(',')).join('\n');
  return csvContent;
}

// Function to create a Blob from CSV content
function createCSVBlob(csvContent) {
  return new Blob([csvContent], { type: 'text/csv' });
}

// Updates the csv dataset information. Changing selectable column names and resetting the preoptimization.
function changeCSV(files, selectedFile, choice) {
    clearAllCSV()
    clearAllPreopt()

    let csvFileName;
    let csvFile;
    // create option to select classification column
    if(choice === "Choose uploaded file") {
        const foundFile = files.find(f => f.filename === selectedFile);
        const data = JSON.parse(JSON.stringify(foundFile.content));
        console.log("data: ", data, );

        // Create CSV content
        const csvContent = createCSV(data);

        // Create Blob from CSV content
        const csvBlob = createCSVBlob(csvContent);

        csvFileName = selectedFile;
        csvFile = csvBlob;

        console.log("created csv: ", csvFile, csvBlob)
    } else {
        csvFileName = document.getElementById("csvFile").files[0].name;
        csvFile = document.getElementById("csvFile").files[0];
    }
    console.log("changeCSV", files, selectedFile, csvFile);

    dict_values = { "csvFileName": csvFileName, "csvFile": csvFile };

    const sent_data = JSON.stringify(dict_values)

    const data = new FormData();
    data.append("processes", JSON.stringify(dict_values))
    data.append("csvFileName", csvFileName)
    data.append("csvFile", csvFile)

    $.ajax({
        url: "/experiments/getCSVColumnTitles",
        data: data,
        type: "POST",
        dataType: 'json',
        processData: false, // important
        contentType: false, // important,
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
            select.className = "px-2 py-1 mr-2 rounded-md border border-gray-400";

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

// Checks that the CSV file is able to load and displays the csv information after all selected preoptimizations with additional pdf graphs
// such as balance and distibution of data to help the user make informed desitions when preoptimizing.
function checkModel() {
    const form = document.getElementById("DLANN_Form");
    document.getElementById("model_Error").innerHTML = "";
    document.getElementById("model_Results").innerHTML = "";

    var formData = new FormData(form);

    var dict_data = {};

    formData.append("layerCounter", layerCounter)

    // iterate through entries...
    for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
        dict_data[pair[0]] = pair[1]
    }

    //Send information to run model experiment.
    // will save into a json file tilted the "projectName".json
    $("#model_Error").hide();
    $("#model_Title").hide();
    $("#model_Results").hide();

    const sent_data = JSON.stringify(dict_data)

    const data = new FormData();
    data.append("processes", JSON.stringify(dict_data))

    $.ajax({
        url: "/experiments/getModelSummary",
        data: data,
        type: "POST",
        dataType: 'json',
        processData: false, // important
        contentType: false, // important,
        success: function (Results) {
            if (Results[0] == "worked") {

                Results = Results[2]

                var writeData = {
                    paragraph: ''
                }

                document.getElementById("model_Results").innerHTML = Results['model_summary'];

                $("#model_Title").show();
                $("#model_Results").show();
            }
            else {
                var writeData = {
                    paragraph: ''
                }

                writeData.paragraph += '<FONT COLOR="#ff0000">ERROR: <br>';
                writeData.paragraph += Results[0];
                writeData.paragraph += Results[1];
                writeData.paragraph += '</FONT >';

                document.getElementById("model_Error").innerHTML = writeData.paragraph;

                $("#model_Error").show();
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var writeData = {
                paragraph: ''
            }

            writeData.paragraph += '<FONT COLOR="#ff0000">ERROR: <br>';
            writeData.paragraph += "Error with connection to server!";
            writeData.paragraph += '</FONT >';

            document.getElementById("model_Preopt").innerHTML = writeData.paragraph;
        }
    });
}

document.getElementById("DLANN_Form").addEventListener("submit", function (e) {
    e.preventDefault();
    checkModel(e.target);
});

var DLANN_Submit = ""

function DLANNSubmit(value) {
    DLANN_Submit = value
}