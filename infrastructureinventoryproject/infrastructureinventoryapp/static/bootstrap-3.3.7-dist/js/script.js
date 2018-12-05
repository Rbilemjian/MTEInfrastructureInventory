


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

    var table = $('#example').DataTable( {
        "scrollX": true,
        "select": true,
        "paging": true,

        //export datatable columns
        dom: 'Bfrtipl',
        buttons: ['copy', 'csv', 'excel', 'pdf'],


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
            var hwDate = data[23];
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









