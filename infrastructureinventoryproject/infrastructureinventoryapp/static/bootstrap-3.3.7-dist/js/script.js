$.fn.dataTable.ext.type.order['month-grade-pre'] = function ( d ) {
    switch ( d ) {
            case 'January':    return 1;
            case 'February': return 2;
            case 'March':   return 3;
            case 'April':   return 4;
            case 'May':   return 5;
            case 'June':   return 6;
            case 'July':   return 7;
            case 'August':   return 8;
            case 'September':   return 9;
            case 'October':   return 10;
            case 'November':   return 11;
            case 'December':   return 12;
    }
    return 0;
};


$(document).ready(function() {
    $('#example').DataTable( {
        
        select: true,
        
        "autoWidth": true,
        
        "columnDefs": [
                { 
                "type": "month-grade", 
                "targets": 2 
                }
            ],
        
        //export datatable columns not including the "edit" column
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'copy',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                }
            },
            {
                extend: 'csv',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                }
            },
            {
                extend: 'excel',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                }
            },
            {
                extend: 'pdf',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                }
            }
    ], 
        
        
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
});



