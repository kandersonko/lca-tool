
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

var ctx = document.getElementById('myChart').getContext('2d');
var chart = initializeChart(ctx);
