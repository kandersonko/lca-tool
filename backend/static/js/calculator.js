function calculate(e) {

  const inputEquations = document.getElementsByClassName("input-equation");
  const equations = Array.from(inputEquations).map(x => x.value);
  console.log("equations: ", equations);
  const csvFile = $("#txtFileUpload_1")[0].files[0];
  console.log("csv: ", csvFile)
  const data = new FormData();
  data.append("csv_file", csvFile);
  data.append("equations", equations);
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
      const output = `<span>${name}: ${response.results}</span/>`;
      $("#results").html(output);
    },
    error: function(error){
      console.log("error", error);
      $("#results").html("There is an error in your entries!");
    }
  });
}

let equation_counter = 1;

function addEquation(event) {
  equation_counter += 1;
  console.log("button clicked: ", event.target);
  const button = event.target;
  const equation = `<textarea name="equation_${equation_counter}" class="input-equation" rows="1" cols="30" value="" placeholder="Enter the equation" style="margin-right: .5rem"></textarea> <br />`;

  $(equation).insertBefore(button);
}
