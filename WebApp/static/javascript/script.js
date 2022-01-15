$(document).on('submit','#stockform',function(e){
    e.preventDefault();

    $.ajax(
        {
            type:'POST',
            url:'',
            data: $(this).serialize(),
            success: function(response){
                var xArray = response['X'];
                var yArray = response['Y'];
                
                // Define Data
                var data = [{
                    x:xArray,
                    y:yArray,
                    mode:"lines",
                    name:"Close price",
                    marker_color:'#42a7ff'
                },
                {
                    x:xArray,
                    open:response['Open'],
                    high:response['High'],
                    low:response['Low'],
                    close:response['Close'],
                    type:"candlestick",
                    name:"Candle stick",
                }];
                
                // Define Layout
                var layout = {
                    xaxis: {title: "Timeline", showgrid:false},
                    yaxis: {title: "Close Price", showgrid:false},  
                    title: "Price Chart",
                    plot_bgcolor:"#222233"
                };
                
                // Display using Plotly
                Plotly.newPlot("plotgraph", data, layout);
            }
        }
    );
})
