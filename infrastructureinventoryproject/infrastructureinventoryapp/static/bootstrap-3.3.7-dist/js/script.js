


$(document).ready(function() {

    if(document.getElementById("hw-support") != null)
    {
        hwSupport = document.getElementById("hw-support");
        var hwDate = hwSupport.textContent;
        if(hwDate != "None")
            {
                var hwDateMilliseconds = Date.parse(hwDate);
                var todayMilliseconds = Date.parse(new Date());
                var difference = hwDateMilliseconds - todayMilliseconds;
                if(difference <= 0)
                    hwSupport.style.color = "red";
                else if(difference < 2592000000)
                    hwSupport.style.color = "orange";

            }
    }

    $('#example').DataTable( {
        "scrollX": true,
        "select": true,
        "paging": false,

        //export datatable columns
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'copy',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
                }
            },
            {
                extend: 'csv',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
                }
            },
            {
                extend: 'excel',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
                }
            },
            {
                extend: 'pdf',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
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

        "createdRow": function(row, data, dataIndex)
        {
            var hwDate = data[22];
            if(hwDate != "None")
            {
                var hwDateMilliseconds = Date.parse(hwDate);
                var todayMilliseconds = Date.parse(new Date());
                var difference = hwDateMilliseconds - todayMilliseconds;
                if(difference <= 0)
                    $(row).addClass('red');
                else if(difference < 2592000000)
                    $(row).addClass('orange');

            }
        },

    });

});


//table click redirect to details page
$('#example').on( 'click', 'tbody tr', function () {
  window.location.href = $(this).data('href');
});









