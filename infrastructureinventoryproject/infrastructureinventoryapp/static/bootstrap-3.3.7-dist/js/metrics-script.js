$(document).ready(function() {
    $('#transcode-rel').DataTable( {
        order: [[0, 'asc']],
        rowGroup: {
            startRender: null,
            endRender: function ( rows, group ) {
 
                var calcAvg = rows
                    .data()
                    .pluck(1)
                    .reduce( function (a, b) {
                        return a + b*1;
                    }, 0) / rows.count();
 
                return $('<tr/>')
                    .append( '<td colspan="3">Average</td>' )
                    .append( '<td>'+calcAvg.toFixed(0)+'</td>' )
            },
    
    });
});
    
$(document).ready(function() {
    $('#postp-rel').DataTable( {
    
    });
});

$(document).ready(function() {
    $('#inf-rel').DataTable( {
    
    });
});
    
$(document).ready(function() {
    $('#trans-rel').DataTable( {
    
    });
});
    
$(document).ready(function() {
    $('#workflow-rel').DataTable( {
    
    });
});
    
$(document).ready(function() {
    $('#transcode-avail').DataTable( {
    
    });
});
    
$(document).ready(function() {
    $('#postp-avail').DataTable( {
    
    });
});
    
$(document).ready(function() {
    $('#inf-avail').DataTable( {
    
    });
});
    
$(document).ready(function() {
    $('#trans-avail').DataTable( {
    
    });
});
    
$(document).ready(function() {
    $('#workf-avail').DataTable( {
    
    });
});