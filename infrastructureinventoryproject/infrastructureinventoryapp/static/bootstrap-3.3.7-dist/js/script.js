


$(document).ready(function() {

    $('#simple-table').DataTable({
        "select": false,
        "paging": false,
        dom: 'tr'
    });

    var table = $('#example').DataTable( {
        "scrollX": true,
        "select": true,
        "paging": true,

        //export datatable columns
        dom: 'Bfrtipl',
        buttons: ['copy', 'csv', 'excel'],


// individual column searching
        initComplete: function () {
            this.api().columns('.select-filter').every( function () {
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo( $(column.footer()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );

                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );

                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        },
    });

    $('#uncheck-all').on('click', function() {
        $('input[type="checkbox"]').prop('checked', false);
        });
    $('#check-all').on('click', function() {
        $('input[type="checkbox"]').prop('checked', true);
});

//table click redirect to details page
$('#example').on( 'click', 'tbody tr', function () {
  window.location.href = $(this).data('href');
});


});









