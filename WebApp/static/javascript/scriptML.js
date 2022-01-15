$(document).on('submit','#stockform',function(e){
    e.preventDefault();

    $.ajax(
        {
            type:'POST',
            url:'',
            data: $(this).serialize(),
            success: function(response){
                
                // Define Data
                var data = [{
                    x:response['dates'],
                    y:response['creturns'],
                    mode:"lines",
                    name:"creturns",
                    marker_color:'blue'
                },
                {
                    x:response['dates'],
                    y:response['cstrategy'],
                    mode:"lines",
                    name:"cstrategy",
                    marker_color:'green'
                }];
                
                // Define Layout
                var layout = {
                    xaxis: {title: "Timeline", showgrid:false},
                    yaxis: {title: "", showgrid:false},  
                    title: response['model']+": perf = "+response['perf']+" | outperf = "+response['outperf'],
                    plot_bgcolor:"#222233"
                };
                
                // Display using Plotly
                Plotly.newPlot("plotgraph", data, layout);
            }
        }
    );
})
