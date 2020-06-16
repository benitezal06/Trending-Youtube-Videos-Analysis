
// Use D3 to create an event handler
d3.selectAll("body").on("change", updatePage);

function updatePage() {
  // Use D3 to select the dropdown menu
  var dropdownMenu = d3.selectAll("#selectOption").node();
  // Assign the dropdown menu item ID to a variable
  var dropdownMenuID = dropdownMenu.id;
  // Assign the dropdown menu option to a variable
  var selectedOption = dropdownMenu.value;

  console.log(selectedOption);

url1 = `http://127.0.0.1:5000/${selectedOption}`
url2 = `http://127.0.0.1:5000/${selectedOption}id`

//this promise is used to access the jsons containing the string categories
d3.json(url2).then(function(datas){
    var catDic = {}
    var id_array = datas[0].items;
    console.log("This is the Id Array:")
    console.log(id_array);
   
    id_array.forEach(function(category){
        catDic[category.id] = category.snippet.title
    
      

})

//this promise is used to access the csv's containing all the trending youtube videos

d3.json(url1).then(function(dataChoosen){

    console.log(dataChoosen);
    // store summary of categories
    var data_summary = [] ; 
                        
    dataChoosen.forEach(function(data1) {
        
        found=false;
        for (var i = 0, len = data_summary.length; i < len; i++){
        
            if (data1["category_id"] == data_summary[i]["cat_id"]){

                    //console.log("whattt");
                    data_summary[i]["cat_count"]+=1;
                    data_summary[i]["cat_ave_likes"] += data1.likes;
                    data_summary[i]["cat_ave_dislikes"] += data1.dislikes;
                    data_summary[i]["cat_ave_comments"] += data1.comment_count; 
                    data_summary[i]["cat_ave_views"] += data1.views;
                    data_summary[i]["cat_ave_likes_dislikes"] = 1;
                    found =true;
                    break;        
            
            };
         
        
        };
        if(!found){
            //console.log(data1["category_id"])
            //console.log(data_summary[i]["cat_id"])
            var dic_to_push = {}
            dic_to_push["cat_id"] = data1.category_id;
            dic_to_push["cat_count"] = 1;
            dic_to_push["cat_ave_likes"] = data1.likes;
            dic_to_push["cat_ave_dislikes"] = data1.dislikes;
            dic_to_push["cat_ave_comments"] = data1.comment_count; 
            dic_to_push["cat_ave_views"] = data1.views;
            dic_to_push["cat_ave_likes_dislikes"] = 1;
            data_summary.push(dic_to_push);          
        }
        
        });
        


        numCatList = []
        data_summary.forEach(function(data3){

            data3["cat_ave_likes"] /= data3.cat_count;
            data3["cat_ave_dislikes"] /= data3.cat_count ;
            data3["cat_ave_comments"] /= data3.cat_count; 
            data3["cat_ave_views"] /= data3.cat_count;
            data3["cat_ave_likes_dislikes"] /= data3.cat_count;
            numCatList.push(data3.cat_id)
        
        
    });
    //below creates a list of labels
    console.log(numCatList)
    stringCatList = []
    numCatList.forEach(function(numCat){
        stringCatList.push(catDic[numCat])
    })
    console.log("this is stringCatlist")
    console.log(stringCatList)




    //set the dimensions and margins of the graph
    var margin = {top: 60, right: 250, bottom: 80, left: 50},
    width = 890 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#myData")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");

    // Add X axis

    // var x = d3.scaleLinear()
    // .domain([0, 260000])
    // .range([ 0, width ]);
    // svg.append("g")
    // .attr("transform", "translate(0," + height + ")")
    // .call(d3.axisBottom(x));

    var x = d3.scaleLog()
    .domain([6420, 260000])
    .range([ 0, width ]);
    svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

    svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .style("text-decoration", "underline")  
        .text(`${selectedOption.toUpperCase()} Youtube Trending Videos`);

    // Add X axis label:
    svg.append("text")
    .attr("text-anchor", "end")
    .attr("x", 400)
    .attr("y", 400 )
    .text("Average Likes Per Category");


    // Add Y axis

    // var y = d3.scaleLinear() 
    // .domain([0, 84000])
    // .range([ height, 0]);

    var y = d3.scaleLog()
    .domain([1500, 85000])
    .range([ height, 0]);
    svg.append("g")
    .call(d3.axisLeft(y));

   

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - 55)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Average Comments Per Category");

    

    // Add scale for bubble size (two options one radius and another area)

    // var z = d3.scaleLinear()
    // .domain([50,10000 ])
    // .range([ 1, 40]);

    var sqrtScale = d3.scaleSqrt()
	.domain([6, 10000])//50
    .range([1, 40]);
    
    //hardcoding the labels
    // var labels = ["22:People & Blogs","24:Entertainment","23:Comedy","28:Science & Technology","1:Film & Animation",
    //             "25:News & Politics","17:Sports","10:Music","15:Pets & Animals","27:Education","26:Howto & Style","2:Autos & Vehicles",
    //             "19:Travel & Events","20:Gaming","29:Nonprofits & Activism","43:Shows"]

    // bubble color

    var bubbleColor = d3.scaleOrdinal()
    .domain(numCatList)
    .range(d3.schemeSet2);

    // tool tip
    var tooltip = d3.select("#myData")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "black")
    .style("border-radius", "5px")
    .style("padding", "10px")
    .style("color", "white")

  
    var showTooltip = function(d) {
    tooltip
    .transition()
    .duration(200)

    tooltip
    .style("opacity", 1)
    .html("Category: " + d.cat_id +"-"+catDic[d.cat_id])
    .style("left", (d3.mouse(this)[0]+30) + "px")
    .style("top", (d3.mouse(this)[1]+30) + "px")
    }

    var moveTooltip = function(d) {
    tooltip
    .style("left", (d3.mouse(this)[0]+30) + "px")
    .style("top", (d3.mouse(this)[1]+30) + "px")
    }
    var hideTooltip = function(d) {
    tooltip
    .transition()
    .duration(200)
    .style("opacity", 0)
    }

    
            
    //Add circles
    svg.append('g')
    .selectAll("dot")
    .data(data_summary)
    .enter()
    .append("circle")
        .attr("cx", function (d) { return x(d.cat_ave_likes); } )
        .attr("cy", function (d) { return y(d.cat_ave_comments);} )
        .attr("r", function (d) { return sqrtScale(d.cat_count); } )
        .style("fill", function (d) { return bubbleColor(d.cat_id); } )
        
        .style("opacity", "0.7")
        .attr("stroke", "black")
        .on("mouseover", showTooltip )
        .on("mousemove", moveTooltip )
        .on("mouseleave", hideTooltip )

    // Add one dot in the legend for each name.
    var size = 15
    
    svg.selectAll("myrect")
      .data(numCatList)
      .enter()
      .append("circle")
        .attr("cx", 690)
        .attr("cy", function(d,i){ return 30 + i*(size+5)}) // 100 is where the first dot appears. 25 is the distance between dots
        .attr("r", 7)
        .style("fill", function(d){ return bubbleColor(d)})
        

    // Add labels beside legend dots
    svg.selectAll("mylabels")
      .data(stringCatList)
      .enter()
      .append("text")
        .attr("x", 690 + size*.8)
        .attr("y", function(d,i){ return 25 + i * (size + 5) + (size/2)}) // 100 is where the first dot appears. 25 is the distance between dots
        .style("fill", function(d){ return bubbleColor(d)})
        .text(function(d){ return d})
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle")
        
    
  
    

})
})

}
