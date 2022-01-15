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
                var eTable="<table class='table table-striped table-dark'><thead><th>Lags</th><th>Perf</th><th>Outperf</th></thead><tbody>"
                for(var i=0; i<response['lags'].length;i++)
                {
                    eTable += "<tr>";
                    eTable += "<td>"+response['lags'][i]+"</td>";
                    eTable += "<td>"+response['perf'][i]+"</td>";
                    eTable += "<td>"+response['outperf'][i]+"</td>";
                    eTable += "</tr>";
                }
                eTable +="</tbody></table>";
                $("#loader").hide();
                $('#forTable').html(eTable);
            }
        }
    );
})
