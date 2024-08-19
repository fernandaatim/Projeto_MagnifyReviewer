document.addEventListener("DOMContentLoaded", function() {
    let card = document.getElementById("card");
    let cardSpinner = document.getElementById("card-spinner");
    let fileInput = document.getElementById("file-input");
    let fileBtn = document.getElementById("file-btn");
  
    fileBtn.addEventListener("click", function() {
      cardSpinner.style.display = "flex"; 
    });
  
    fileInput.addEventListener("change", function() {
      let formData = new FormData();
      formData.append("arquivo", fileInput.files[0]);
  
      fetch('/processar_emails', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
  
      .then(result =>{
        cardSpinner.style.display="none";
        fillTable();
        location.reload();
      })
      .catch(error => {
          cardSpinner.style.display = "none"
          console.error(error);
      });
    });
  });