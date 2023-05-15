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

                // console.log(tables);
                // }

                // if(uploadId === 'txtFileUpload_2'){
                //   if (tableHealth != null) {
                //     tableHealth.destroy();
                //     $('#CSVtable_2').empty();
                //   }

                //   if(checkCSVHeader(data) == false){
                //     console.log("Dataset must have five columns and have the header of 'Indicator,Metric,Location,Score,Total Score'");
                //   }

                //   tableHealth = populateTable(data,$('#CSVtable_2'));
                // }

                // if(uploadId === 'txtFileUploadEducation'){
                //   if (tableEducation != null) {
                //     tableEducation.destroy();
                //     $('#CSVtableEducation').empty();
                //   }

                //   if(checkCSVHeader(data) == false){
                //     console.log("Dataset must have five columns and have the header of 'Indicator,Metric,Location,Score,Total Score'");
                //   }

                //   tableEducation = populateTable(data,$('#CSVtableEducation'));
                // }

                // if(uploadId === 'txtFileUploadSafety'){
                //   if (tableSafety != null) {
                //     tableSafety.destroy();
                //     $('#CSVtableSafety').empty();
                //   }

                //   if(checkCSVHeader(data) == false){
                //     console.log("Dataset must have five columns and have the header of 'Indicator,Metric,Location,Score,Total Score'");
                //   }

                //   tableSafety = populateTable(data,$('#CSVtableSafety'));
                //}

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
        //var canvas = document.querySelector('#Results');
        //creates image
        //var canvasImg = canvas.toDataURL("image/png", 1.0);

        // We add all the info into one list in order to put them into the pdf
        var list = [];
        // Add the info
        list.push($("#infoHeader").text());
        list.push($("#projectName").val());

        // Add the description
        list.push($("#scopeHeader").text());

        list.push($("phase1Text").val());

        // list.push($("#phase2Header").text());

        // TODO:This should be wrapped in an if()
        // let LifeExpectancyTablePromise = new Promise ((resolve,reject) => {
        //   window.scrollTo(0, 0);
        //   html2canvas($('#csv-displayLifeExpectancy')[0]).then(function (canvas) {
        //         var LifeExpectancyTableImg = canvas.toDataURL("image/png", 1.0);
        //         resolve(LifeExpectancyTableImg);
        //       });
        // });


        // Add the selected equation
        //list.push($("#methodHeader").text());
        //list.push($('input:radio[name="methodCalculation"]:checked').text());

        //$('input:radio[name="methodCalculation"]:checked').each(function () {
        //    var idVal = $(this).attr("id");
        //    list.push($("label[for='" + idVal + "']").text());
        //});

        //var equation_image = null;

        // if ($('input[id=socialMethod]:checked')) {
        //   // list.push($("label[for='socialMethod']").text());

        //   equation_image = document.querySelector('#indicator_image').getAttribute("src");
        // }

        // Add the result
        list.push("Results:");

        //list.push($("#Result1").text());
        //list.push($("#Result2").text());

        //list.push($("#phase4Header").text());

        // Remove the 'screenshot' of CSV table for now, there will be problem if we have table the spans in more than one 'table pages'
        // var LifeExpectancyTablePromiseResult = await LifeExpectancyTablePromise;
        // console.log("++++"+LifeExpectancyTablePromiseResult);
        // createPDF(canvasImg, LifeExpectancyTablePromiseResult, list);

        createPDF(canvasImg, null, equation_image, list);
    });

   
    $("#runMLAExperimentButton").click(async function () {

        document.getElementById("Results").innerHTML = "Hello!";
        document.getElementById("StatusInfo").innerHTML = "Hello!";

        const fileName = document.getElementById("projectNameMLA").value;
        const csvFile = document.getElementById("csvMLA").files[0].name;
        PreOpt = "";

        if (document.getElementById('PreOpt_None').checked) {
            PreOpt = "None";
        }
        else if (document.getElementById('PreOpt_PCA').checked) {
            PreOpt = "PCA";
        }

        Method = "";
        if (document.getElementById('Method_SVM').checked) {
            Method = "SVM";
        }
        else if (document.getElementById('Method_KNN').checked) {
            Method = "KNN";
        }

        Validation = "";
        Validation_Option = "";
        if (document.getElementById('Val_k-Fold').checked) {
            Validation = "K-Fold";
            Validation_Option = document.getElementById("Val_k-Fold_text").value;
        }
        else if (document.getElementById('Val_Split').checked) {
            Validation = "Val-Split";
            Validation_Option = document.getElementById("Val_Split_text").value;
        }

        const dict_values = {
            fileName, csvFile, PreOpt, Method, Validation, Validation_Option
        }
        const sent_data = JSON.stringify(dict_values)

        document.getElementById("StatusInfo").innerHTML = "Processing...";

        $.ajax({
            url: "/experiments/run_experiment",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(sent_data),
            async: false,
            dataType: 'json',
            success: function (data) {

                document.getElementById("StatusInfo").innerHTML = "Completed!";

                if (Validation == "Val-Split") {
                    // obtain the Metrics
                    Accuracy = data["Accuracy"]
                    F1 = data["F1"]
                    F1_micro = data["F1_micro"]
                    F1_macro = data["F1_macro"]
                    Precision = data["Precision"]
                    Precision_micro = data["Precision_micro"]
                    Precision_macro = data["Precision_macro"]
                    Conf_Matrix = data["conf_matrix"]

                    // display the metrics
                    var img = new Image();

                    img.src = '../../static/Images/' + fileName + '.png?' + performance.now();

                    var writeData = {
                        paragraph: 'Accuracy: '.bold() + data["Accuracy"] + '<br\>' +
                            "Precision for Each Class: ".bold() + data["Precision"] + "<br\>" +
                            "Precision (Micro): ".bold() + data["Precision_micro"] + "<br\>" +
                            "Precision (Macro): ".bold() + data["Precision_macro"] + "<br\>" +
                            "F1 for each Class: ".bold() + data["F1"] + "<br\>" +
                            "F1 (Micro): ".bold() + data["F1_micro"] + "<br\>" +
                            "F1 (Macro): ".bold() + data["F1_macro"] + "<br\>" +
                            `${img.outerHTML}`
                    }

                    //$('#Results').html(data.paragraph);
                    document.getElementById("Results").innerHTML = writeData.paragraph;
                }

                else if (Validation == "K-Fold") {
                    var writeData = {
                        paragraph: ''
                    }

                    document.getElementById("Results").innerHTML = "Test 1"

                    for (let i = 0; i < data["acc_list"].length; i++) {
                        writeData.paragraph += '=========================Results for Fold ' + i + '=========================<br\>'
                        writeData.paragraph += 'Accuracy: '.bold() + data["acc_list"][i] + '<br\>'
                        writeData.paragraph += 'Precision for each class: '.bold() + data["prec_list"][i] + '<br\>'
                        writeData.paragraph += 'Precision (Micro): '.bold() + data["prec_micro_list"][i] + '<br\>'
                        writeData.paragraph += 'Precision (Macro): '.bold() + data["prec_macro_list"][i] + '<br\>'
                        writeData.paragraph += 'F1 for each class: '.bold() + data["f1_list"][i] + '<br\>'
                        writeData.paragraph += 'F1 (Micro): '.bold() + data["f1_micro_list"][i] + '<br\>'
                        writeData.paragraph += 'F1 (Macro): '.bold() + data["f1_macro_list"][i] + '<br\>'

                        var img = new Image();
                        img.src = '../../static/Images/' + fileName + "_fold_" + i + '.png?' + performance.now();

                        document.getElementById("Results").innerHTML = "Test 3"

                        writeData.paragraph += `${img.outerHTML} <br\>`
                    }

                    writeData.paragraph += '<br\>'
                    writeData.paragraph += '=========================Results Overall=========================<br\>'
                    writeData.paragraph += 'Average Accuracy: '.bold() + data["acc_average"] + '<br\>'
                    writeData.paragraph += 'Average Precision for Each Class: '.bold() + data["prec_average"] + '<br\>'
                    writeData.paragraph += 'Average Precision (Micro): '.bold() + data["prec_micro_average"] + '<br\>'
                    writeData.paragraph += 'Average Precision (Macro): '.bold() + data["prec_macro_average"] + '<br\>'
                    writeData.paragraph += 'Average F1 for Each Class: '.bold() + data["f1_average"] + '<br\>'
                    writeData.paragraph += 'Average F1 (Micro): '.bold() + data["f1_micro_average"] + '<br\>'
                    writeData.paragraph += 'Average F1 (Macro): '.bold() + data["f1_macro_average"] + '<br\>'

                    var img = new Image();
                    img.src = '../../static/Images/' + fileName + '_Collective.png?' + performance.now()

                    writeData.paragraph += `${img.outerHTML} <br\>`

                    document.getElementById("Results").innerHTML = writeData.paragraph;
                }
            },
            error: e => $('#ResultMLA').replaceWith(e)
        });

        /*
        function changeMethod() {
            if (document.getElementById('Method_SVM').checked) {
                // If SVM is selected display SVM parameters
                dict_values_ = { Method: "SVM" };

                const sent_data = JSON.stringify(dict_values)
                $.ajax({
                    url: "/experiments/getMethodParameters",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(sent_data),
                    async: false,
                    dataType: 'json',
                    success: function (data) {

                        for (var option in data['parameters_Info']) {
                            var Parameters = document.getElementById("Parameters");

                            if (data['parameters_Info'].hasOwnProperty(option)) {
                                var pair = data['parameters_Info'][option];
                                var checkbox = document.createElement("input");
                                checkbox.type = "checkbox";
                                checkbox.name = pair;
                                checkbox.value = pair;
                                Parameters.appendChild(checkbox);

                                var label = document.createElement('label')
                                label.htmlFor = pair;
                                label.appendChild(document.createTextNode(pair));

                                Parameters.appendChild(label);
                                Parameters.appendChild(document.createElement("br"));
                            }
                        }
                    }

            } else if (document.getElementById('Method_KNN').checked) {
                // If KNN is selected display KNN parameters
                ;

            }
            */



    });
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
                    var label = document.createElement('label')
                    label.htmlFor = name_label;
                    label.appendChild(document.createTextNode(name_label));

                    s1.appendChild(label);

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
    //document.getElementById("Results").innerHTML += formData;

    //document.getElementById("Results").innerHTML = "Test!";

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

            //document.getElementById("Results").innerHTML = Results['Validation'];
            //document.getElementById("StatusInfo").innerHTML = "Completed!";
            
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

                var writeData = {
                    paragraph: 'Accuracy: '.bold() + Results["Accuracy"] + '<br\>' +
                        "Precision for Each Class: ".bold() + Results["Precision"] + "<br\>" +
                        "Precision (Micro): ".bold() + Results["Precision_micro"] + "<br\>" +
                        "Precision (Macro): ".bold() + Results["Precision_macro"] + "<br\>" +
                        "F1 for each Class: ".bold() + Results["F1"] + "<br\>" +
                        "F1 (Micro): ".bold() + Results["F1_micro"] + "<br\>" +
                        "F1 (Macro): ".bold() + Results["F1_macro"] + "<br\>" +
                        `${img.outerHTML}`
                }

                document.getElementById("Results").innerHTML = "Test 6";

                //$('#Results').html(data.paragraph);
                document.getElementById("Results").innerHTML = writeData.paragraph;
            }

            else if (Results['Validation'] == "K-Fold") {
                var writeData = {
                    paragraph: ''
                }

                document.getElementById("Results").innerHTML = "Testing 1";

                for (let i = 0; i < Results["acc_list"].length; i++) {
                    writeData.paragraph += '=========================Results for Fold ' + i + '=========================<br\>'
                    writeData.paragraph += 'Accuracy: '.bold() + Results["acc_list"][i] + '<br\>'
                    writeData.paragraph += 'Precision for each class: '.bold() + Results["prec_list"][i] + '<br\>'
                    writeData.paragraph += 'Precision (Micro): '.bold() + Results["prec_micro_list"][i] + '<br\>'
                    writeData.paragraph += 'Precision (Macro): '.bold() + Results["prec_macro_list"][i] + '<br\>'
                    writeData.paragraph += 'F1 for each class: '.bold() + Results["f1_list"][i] + '<br\>'
                    writeData.paragraph += 'F1 (Micro): '.bold() + Results["f1_micro_list"][i] + '<br\>'
                    writeData.paragraph += 'F1 (Macro): '.bold() + Results["f1_macro_list"][i] + '<br\>'

                    document.getElementById("Results").innerHTML = "Testing 2";
                    var img = new Image();
                    img.src = 'data:image/jpeg;base64,' + Results["cm_list"][i];

                    writeData.paragraph += `${img.outerHTML} <br\>`

                    document.getElementById("Results").innerHTML = "Test 3";
                }

                document.getElementById("Results").innerHTML = "Test 4";

                writeData.paragraph += '<br\>'
                writeData.paragraph += '=========================Results Overall=========================<br\>'
                writeData.paragraph += 'Average Accuracy: '.bold() + Results["acc_average"] + '<br\>'
                writeData.paragraph += 'Average Precision for Each Class: '.bold() + Results["prec_average"] + '<br\>'
                writeData.paragraph += 'Average Precision (Micro): '.bold() + Results["prec_micro_average"] + '<br\>'
                writeData.paragraph += 'Average Precision (Macro): '.bold() + Results["prec_macro_average"] + '<br\>'
                writeData.paragraph += 'Average F1 for Each Class: '.bold() + Results["f1_average"] + '<br\>'
                writeData.paragraph += 'Average F1 (Micro): '.bold() + Results["f1_micro_average"] + '<br\>'
                writeData.paragraph += 'Average F1 (Macro): '.bold() + Results["f1_macro_average"] + '<br\>'

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
    //document.getElementById("Results").innerHTML += formData;

    document.getElementById("Results").innerHTML = "Test!";

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
            document.getElementById("sentJSON").innerHTML = Results['Validation'];

            if (Results['Validation'] == "Split") {

                document.getElementById("sentJSON").innerHTML = "Test 3";
                // obtain the Metrics
                Accuracy = Results["Accuracy"]
                F1 = Results["F1"]
                F1_micro = Results["F1_micro"]
                F1_macro = Results["F1_macro"]
                Precision = Results["Precision"]
                Precision_micro = Results["Precision_micro"]
                Precision_macro = Results["Precision_macro"]
                Conf_Matrix = Results["cm_overall"]

                document.getElementById("sentJSON").innerHTML = "Test 4";

                // display the metrics
                var img = new Image();

                img.src = "data:image/png;base64," + Results["cm_overall"];

                document.getElementById("sentJSON").innerHTML = "Test 5";
                var writeData = {
                    paragraph: ''
                }

                document.getElementById("sentJSON").innerHTML = "Test 1";

                // Quick way to do this, this will be changed when Metrics class is created...
                //  Then a loop will go through all metrics, check if each check mark is selected.
                //      Then implement a given sentence and value...
                if (dict_data['Met_ACC_checked'] == "true") {
                    writeData.paragraph += 'Accuracy: '.bold() + Results["Accuracy"] + '<br\>'
                }


                if (dict_data['Met_Precision_checked'] == "true") {
                    writeData.paragraph += "Precision for Each Class: ".bold() + Results["Precision"] + "<br\>"
                }

                if (dict_data['Met_Precision_Micro_checked'] == "true") {
                    writeData.paragraph += "Precision (Micro): ".bold() + Results["Precision_micro"] + "<br\>"
                }

                if (dict_data['Met_Precision_Macro_checked'] == "true") {
                    writeData.paragraph += "Precision (Macro): ".bold() + Results["Precision_micro"] + "<br\>"
                }


                if (dict_data['Met_F1_checked'] == "true") {
                    writeData.paragraph += "F1 for each Class: ".bold() + Results["F1"] + "<br\>"
                }

                if (dict_data['Met_F1_Micro_checked'] == "true") {
                    writeData.paragraph += "F1 (Micro): ".bold() + Results["F1_micro"] + "<br\>"
                }


                if (dict_data['Met_F1_Macro_checked'] == "true") {
                    writeData.paragraph += "F1 (Macro): ".bold() + Results["F1_macro"] + "<br\>"
                }

                if (dict_data['Met_CM_checked'] == "true") {
                    writeData.paragraph += `${img.outerHTML}`
                }

                //$('#Results').html(data.paragraph);
                document.getElementById("Results").innerHTML = writeData.paragraph;
            }

            else if (Results['Validation'] == "K-Fold") {
                var writeData = {
                    paragraph: ''
                }

                document.getElementById("Results").innerHTML = "Testing 1";

                for (let i = 0; i < Results["acc_list"].length; i++) {
                    writeData.paragraph += '=========================Results for Fold ' + i + '=========================<br\>'

                    if (dict_data['Met_ACC_checked'] == "true") {
                        writeData.paragraph += 'Accuracy: '.bold() + Results["acc_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_Precision_checked'] == "true") {
                        writeData.paragraph += 'Precision for each class: '.bold() + Results["prec_list"][i] + '<br\>'
                    }

                    if (dict_data['Met_Precision_Micro_checked'] == "true") {
                        writeData.paragraph += "Precision (Micro): ".bold() + Results["Precision_micro"] + "<br\>"
                    }

                    if (dict_data['Met_Precision_Macro_checked'] == "true") {
                        writeData.paragraph += 'Precision (Macro): '.bold() + Results["prec_macro_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_F1_checked'] == "true") {
                        writeData.paragraph += 'F1 for each class: '.bold() + Results["f1_list"][i] + '<br\>'
                    }

                    if (dict_data['Met_F1_Micro_checked'] == "true") {
                        writeData.paragraph += 'F1 (Micro): '.bold() + Results["f1_micro_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_F1_Macro_checked'] == "true") {
                        writeData.paragraph += 'F1 (Macro): '.bold() + Results["f1_macro_list"][i] + '<br\>'
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
                    writeData.paragraph += 'Average Accuracy: '.bold() + Results["acc_average"] + '<br\>'
                }


                if (dict_data['Met_Precision_checked'] == "true") {
                    writeData.paragraph += 'Average Precision for Each Class: '.bold() + Results["prec_average"] + '<br\>'
                }

                if (dict_data['Met_Precision_Micro_checked'] == "true") {
                    writeData.paragraph += 'Average Precision (Micro): '.bold() + Results["prec_micro_average"] + '<br\>'
                }

                if (dict_data['Met_Precision_Macro_checked'] == "true") {
                    writeData.paragraph += 'Average Precision (Macro): '.bold() + Results["prec_macro_average"] + '<br\>'
                }


                if (dict_data['Met_F1_checked'] == "true") {
                    writeData.paragraph += 'Average F1 for Each Class: '.bold() + Results["f1_average"] + '<br\>'
                }

                if (dict_data['Met_F1_Micro_checked'] == "true") {
                    writeData.paragraph += 'Average F1 (Micro): '.bold() + Results["f1_micro_average"] + '<br\>'
                }


                if (dict_data['Met_F1_Macro_checked'] == "true") {
                    writeData.paragraph += 'Average F1 (Macro): '.bold() + Results["f1_macro_average"] + '<br\>'
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
    //document.getElementById("Results").innerHTML += formData;

    document.getElementById("Results").innerHTML = "Test!";

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
            document.getElementById("sentJSON").innerHTML = Results['Validation'];

            if (Results['Validation'] == "Split") {

                document.getElementById("sentJSON").innerHTML = "Test 3";
                // obtain the Metrics
                Accuracy = Results["Accuracy"]
                F1 = Results["F1"]
                F1_micro = Results["F1_micro"]
                F1_macro = Results["F1_macro"]
                Precision = Results["Precision"]
                Precision_micro = Results["Precision_micro"]
                Precision_macro = Results["Precision_macro"]
                Conf_Matrix = Results["cm_overall"]

                document.getElementById("sentJSON").innerHTML = "Test 4";

                // display the metrics
                var img = new Image();

                img.src = "data:image/png;base64," + Results["cm_overall"];

                document.getElementById("sentJSON").innerHTML = "Test 5";
                var writeData = {
                    paragraph: ''
                }

                document.getElementById("sentJSON").innerHTML = "Test 1";

                // Quick way to do this, this will be changed when Metrics class is created...
                //  Then a loop will go through all metrics, check if each check mark is selected.
                //      Then implement a given sentence and value...
                if (dict_data['Met_ACC_checked'] == "true") {
                    writeData.paragraph += 'Accuracy: '.bold() + Results["Accuracy"] + '<br\>'
                }


                if (dict_data['Met_Precision_checked'] == "true") {
                    writeData.paragraph += "Precision for Each Class: ".bold() + Results["Precision"] + "<br\>"
                }

                if (dict_data['Met_Precision_Micro_checked'] == "true") {
                    writeData.paragraph += "Precision (Micro): ".bold() + Results["Precision_micro"] + "<br\>"
                }

                if (dict_data['Met_Precision_Macro_checked'] == "true") {
                    writeData.paragraph += "Precision (Macro): ".bold() + Results["Precision_micro"] + "<br\>"
                }


                if (dict_data['Met_F1_checked'] == "true") {
                    writeData.paragraph += "F1 for each Class: ".bold() + Results["F1"] + "<br\>"
                }

                if (dict_data['Met_F1_Micro_checked'] == "true") {
                    writeData.paragraph += "F1 (Micro): ".bold() + Results["F1_micro"] + "<br\>"
                }


                if (dict_data['Met_F1_Macro_checked'] == "true") {
                    writeData.paragraph += "F1 (Macro): ".bold() + Results["F1_macro"] + "<br\>"
                }

                if (dict_data['Met_CM_checked'] == "true") {
                    writeData.paragraph += `${img.outerHTML}`
                }

                //$('#Results').html(data.paragraph);
                document.getElementById("Results").innerHTML = writeData.paragraph;
            }

            else if (Results['Validation'] == "K-Fold") {
                var writeData = {
                    paragraph: ''
                }

                document.getElementById("Results").innerHTML = "Testing 1";

                for (let i = 0; i < Results["acc_list"].length; i++) {
                    writeData.paragraph += '=========================Results for Fold ' + i + '=========================<br\>'

                    if (dict_data['Met_ACC_checked'] == "true") {
                        writeData.paragraph += 'Accuracy: '.bold() + Results["acc_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_Precision_checked'] == "true") {
                        writeData.paragraph += 'Precision for each class: '.bold() + Results["prec_list"][i] + '<br\>'
                    }

                    if (dict_data['Met_Precision_Micro_checked'] == "true") {
                        writeData.paragraph += "Precision (Micro): ".bold() + Results["Precision_micro"] + "<br\>"
                    }

                    if (dict_data['Met_Precision_Macro_checked'] == "true") {
                        writeData.paragraph += 'Precision (Macro): '.bold() + Results["prec_macro_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_F1_checked'] == "true") {
                        writeData.paragraph += 'F1 for each class: '.bold() + Results["f1_list"][i] + '<br\>'
                    }

                    if (dict_data['Met_F1_Micro_checked'] == "true") {
                        writeData.paragraph += 'F1 (Micro): '.bold() + Results["f1_micro_list"][i] + '<br\>'
                    }


                    if (dict_data['Met_F1_Macro_checked'] == "true") {
                        writeData.paragraph += 'F1 (Macro): '.bold() + Results["f1_macro_list"][i] + '<br\>'
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
                    writeData.paragraph += 'Average Accuracy: '.bold() + Results["acc_average"] + '<br\>'
                }


                if (dict_data['Met_Precision_checked'] == "true") {
                    writeData.paragraph += 'Average Precision for Each Class: '.bold() + Results["prec_average"] + '<br\>'
                }

                if (dict_data['Met_Precision_Micro_checked'] == "true") {
                    writeData.paragraph += 'Average Precision (Micro): '.bold() + Results["prec_micro_average"] + '<br\>'
                }

                if (dict_data['Met_Precision_Macro_checked'] == "true") {
                    writeData.paragraph += 'Average Precision (Macro): '.bold() + Results["prec_macro_average"] + '<br\>'
                }


                if (dict_data['Met_F1_checked'] == "true") {
                    writeData.paragraph += 'Average F1 for Each Class: '.bold() + Results["f1_average"] + '<br\>'
                }

                if (dict_data['Met_F1_Micro_checked'] == "true") {
                    writeData.paragraph += 'Average F1 (Micro): '.bold() + Results["f1_micro_average"] + '<br\>'
                }


                if (dict_data['Met_F1_Macro_checked'] == "true") {
                    writeData.paragraph += 'Average F1 (Macro): '.bold() + Results["f1_macro_average"] + '<br\>'
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
            // dom: 'Bfrtip',
            // buttons: [
            //     {
            //         text: 'Get selected data',
            //         action: function () {
            //             // var count = table.rows( { selected: true } ).count();

            //             // events.prepend( '<div>'+count+' row(s) selected</div>' );
            //             // console.log(table.rows({seleted: true}).data()[0]);
            //             var data  = table.rows({seleted: true}).data()[0];

            //             var result = data[0]*data[1]+data[2]*data[3];
            //             console.log(data);

            //             results.append($( "<i>"+result+"</i>"));
            //         }
            //     }
            // ]
        });
    }


}