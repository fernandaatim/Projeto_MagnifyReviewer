const fileForm = document.getElementById("file-form");
const fileInput = document.getElementById("file-input");
const fileBtn = document.getElementById("file-btn");
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

fileBtn.addEventListener("click", (e) => {
  e.preventDefault();
  fileInput.click();
});

fileInput.addEventListener("change", (e) => {
  const arquivo = fileInput.files[0];
  if (arquivo) {
    document.getElementById("file-message").style.visibility = "visible";
    document.getElementById("file-name").textContent = `File selected: ${fileInput.files[0].name}`;

    let formData = new FormData();
    formData.append("arquivo",arquivo);
    fetch('/processar_emails', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())

    .then(result =>{
      document.getElementById("file-message").style.visibility = "hidden";
      fillTable();
    })
  }
});

function fillTable() {
  fetch('/resultados', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => {
      return response.text();
  })
  .then(csvData => {
      const tableBody = document.getElementById('tb-resultados');
      tableBody.innerHTML = '';
      const rows = csvData.trim().split('\n').filter(row => row.trim() !== '');
      rows.slice(1).forEach(row => {
          const columns = row.split(',').map(column => column.trim());
          const tr = document.createElement('tr');
          columns.forEach(column => {
              const td = document.createElement('td');
              td.textContent = column;
              tr.appendChild(td);
          });
          tableBody.appendChild(tr);
      });
  });
}

window.onload = fillTable;