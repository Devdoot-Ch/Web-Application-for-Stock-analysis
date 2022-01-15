$(document).on('submit','#stockform',function(e){
    e.preventDefault();

    $.ajax(
        {
            type:'POST',
            url:'',
            data: $(this).serialize(),
            beforeSend: function(){
                $("#loader").show();
            },
            success: function(response){
                var eTable="<table class='table table-striped table-dark'><thead><th>SMA short</th><th>SMA long</th><th>Performance</th></thead><tbody>"
                for(var i=0; i<response['SMA_S'].length;i++)
                {
                    eTable += "<tr>";
                    eTable += "<td>"+response['SMA_S'][i]+"</td>";
                    eTable += "<td>"+response['SMA_L'][i]+"</td>";
                    eTable += "<td>"+response['performance'][i]+"</td>";
                    eTable += "</tr>";
                }
                eTable +="</tbody></table>";
                $("#loader").hide();
                $('#forTable').html(eTable);
            }
        }
    );
})
