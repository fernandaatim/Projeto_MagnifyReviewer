document.getElementById('export-btn').addEventListener('click', function() {
    const tableBody = document.getElementById('tb-resultados');
    const rows = Array.from(tableBody.getElementsByTagName('tr'));
    const headers = Array.from(document.querySelectorAll('#cabecao th')).map(th => th.textContent.trim());

    const tableData = rows.map(row => {
        const cells = Array.from(row.getElementsByTagName('td'));
        return cells.map(cell => cell.textContent.trim());
    });

    const docDefinition = {
        content: [
            {
                table: {
                    headerRows: 1,
                    widths: Array(headers.length).fill('*'),
                    body: [
                        headers.map(header => ({ text: header, style: 'tableHeader' })),
                        ...tableData.map((row, index) => row.map(cell => ({
                            text: cell,
                            style: 'tableCell',
                            fillColor: index % 2 === 0 ? '#f2f2f2' : '#ffffff' //Efeito "zebrado"
                        })))
                    ]
                },
                layout: {
                    hLineWidth: function() { return 0.5; },
                    vLineWidth: function() { return 0.5; },
                    hLineColor: function() { return '#aaaaaa'; }, 
                    vLineColor: function() { return '#aaaaaa'; },
                    paddingLeft: function() { return 4; }, 
                    paddingRight: function() { return 4; },
                }
            }
        ],
        styles: {
            tableHeader: {
                fontSize: 12,
                fillColor: '#005691',
                color: 'white',
                bold: true,
                alignment: 'center' 
            },
            tableCell: {
                fontSize: 12,
                alignment: 'center' 
            }
        }
    };

    pdfMake.createPdf(docDefinition).download('documento.pdf');
});
