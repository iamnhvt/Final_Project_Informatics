google.charts.load('current', {
    'packages': ['table']
});
google.charts.setOnLoadCallback(drawTable);

function drawTable() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Name');
    data.addColumn('string', 'Country');
    data.addColumn('number', 'Salary');
    data.addColumn('boolean', 'Full Time Employee');
    data.addRows([
        ['Abb', 'Australia', { v: 232323, f: '$232323' }, false],
        ['Abb1', 'Australia', { v: 232323, f: '$232323' }, false],
        ['Abdasd', 'Australia', { v: 232323, f: '$232323' }, false],
        ['Tai', 'Australia', { v: 232323, f: '$232323' }, false],
        ['Abbc', 'Australia', { v: 232323, f: '$232323' }, false]

    ]);

    var options = {
        allowHtml: true,
        showRowNumber: true,
        width: '100%',
        heiht: '100%',
        pagingButtons: "auto"
    };

    var formatter = new google.visualization.ColorFormat();
    formatter.addGradientRange(8000, 200000, 'black', '#db7f58', '#db281c');
    formatter.format(data, 1);

    var table = new google.visualization.Table(document.getElementById("table"));
    var formatterBar = new google.visualization.BarFormat({
        width: 120
    });
    formatterBar.format(data, 1);
    table.draw(data, options)
}