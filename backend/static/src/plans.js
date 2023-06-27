const planSelect = document.getElementById('plan-select');
const csvFilesDiv = document.getElementById('csv-files');
const choosePlanBtn = document.getElementById('choose-plan-btn');

// Hide the CSV files list by default
csvFilesDiv.style.display = 'none';

// Show the CSV files list when the user selects the "Premium" plan
planSelect.addEventListener('change', (event) => {
  if (event.target.value === 'premium') {
    csvFilesDiv.style.display = 'block';
  } else {
    csvFilesDiv.style.display = 'none';
  }
});

// Download the selected CSV file when the user clicks on a file link
csvFilesDiv.addEventListener('click', (event) => {
  const link = event.target.closest('a');
  if (link) {
    event.preventDefault();
    const filename = link.getAttribute('href');
    const downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', filename);
    downloadLink.setAttribute('download', '');
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  }
});

// Prevent the form from submitting when the user clicks the "Choose Plan" button
choosePlanBtn.addEventListener('click', (event) => {
  event.preventDefault();
});
