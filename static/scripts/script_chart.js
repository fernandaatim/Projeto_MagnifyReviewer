
const showchart = document.getElementById('mediaChart');
const showTable = document.getElementById('table-scores');
const tableBody = document.getElementById('tb-resultados');

function toggle()
{
  switch (document.getElementById('chart-btn').textContent)
  {
    case "Statistics":
      showTable.classList.add("d-none");
      showchart.classList.remove("d-none");
      document.getElementById('chart-btn').textContent = "Table";
      var gramatica    = [];
      var espacamento  = [];
      var saudacao     = [];
      var finalizacao  = [];
      var Rgramatica   = 0;
      var Respacamento = 0;
      var Rsaudacao    = 0;
      var Rfinalizacao = 0;
      for(i =0; i< tableBody.childNodes.length;i++)
      {
        gramatica.push(parseInt(tableBody.childNodes[i].childNodes[1].textContent));
        espacamento.push(parseInt(tableBody.childNodes[i].childNodes[2].textContent));
        saudacao.push(parseInt(tableBody.childNodes[i].childNodes[3].textContent));
        finalizacao.push(parseInt(tableBody.childNodes[i].childNodes[4].textContent));
        Rgramatica = gramatica.reduce((a, b) => a + b, 0);
        Respacamento = espacamento.reduce((a, b) => a + b, 0);
        Rsaudacao = saudacao.reduce((a, b) => a + b, 0);
        Rfinalizacao = finalizacao.reduce((a, b) => a + b, 0);
      };
      const data = [Rgramatica, Respacamento, Rsaudacao, Rfinalizacao];
      const labels = ['Gramática', 'Finalização', 'Saudação', 'Espaçamento'];
      const total = data.reduce((a, b) => a + b, 0);
      const percent = data.map((value) => (value / total) * 100);

      const chartData =
      {
        labels: labels,
        datasets:
        [{
          label: 'Média de ocorrências',
          data: data,
          backgroundColor:
          [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
          ],
          borderColor:
          [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
          ],
          borderWidth: 1
        },
      ]
      };
      const config =
      {
        type: 'doughnut',
        data: chartData,
        options:
        {
          responsive: true,
          plugins:
          {
            legend:
            {
              position: 'top',
            },
            title:
            {
              display: true,
              text: 'Estatísticas'
            },
            tooltip:
            {
              callbacks:
              {
                label: (tooltipItem) =>
                {
                  return `${tooltipItem.dataset.label.trim()}: \u00A0${tooltipItem.formattedValue.trim()} (${percent[tooltipItem.dataIndex]}%)`;
                }
              },
              multiKeyBackground: false,
              bodySpacing: 4,
              caretSize: 1,
              cornerRadius: 9,
              padding: 10,
            }
          }
        },
      };

      try
      {
        mediaChart = new Chart(showchart, config);
      }
      catch (error)
      {
        mediaChart.destroy();
        mediaChart = new Chart(showchart, config);
      }      
      
    break;
    case "Table":
      showchart.classList.add("d-none");
      showTable.classList.remove("d-none");
      document.getElementById('chart-btn').textContent = "Statistics";
      if(!mediaChart === null && !mediaChart === undefined)
      {
        mediaChart.destroy();
      }
      break;
  }
}