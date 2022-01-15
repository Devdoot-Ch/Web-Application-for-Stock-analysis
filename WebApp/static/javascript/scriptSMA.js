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
                    x:response['X'],
                    y:response['Y'],
                    mode:"lines",
                    name:"Close price",
                    marker_color:'#42a7ff'
                },
                {
                    x:response['X'],
                    y:response['smaShort'],
                    mode:"lines",
                    name:"SMA short",
                    marker_color:'white'
                },
                {
                    x:response['X'],
                    y:response['smaLong'],
                    mode:"lines",
                    name:"SMA long",
                    marker_color:'green'
                }];
                
                // Define Layout
                var layout = {
                    xaxis: {title: "Timeline", showgrid:false},
                    yaxis: {title: "", showgrid:false},  
                    title: "SMA "+response['short']+" | SMA "+response['long'],
                    plot_bgcolor:"#222233"
                };
                
                // Display using Plotly
                Plotly.newPlot("plotgraph", data, layout);
            }
        }
    );
})
