// This isn't necessary but it keeps the editor from thinking L and carto are typos
/* global L, carto */

//initialize map
if (this.map) {
  this.map.remove();
}

var map = L.map("map", {
  center: [38.896394, -98.290011],
  zoom: 4
});

// Add base layer
L.tileLayer(
  "https://{s}.basemaps.cartocdn.com/rastertiles/dark_nolabels/{z}/{x}/{y}.png",
  {
    maxZoom: 18
  }
).addTo(map);

// Initialize Carto
var client = new carto.Client({
  apiKey: "c7f445b9a5c3b84e71f8e0381f23a7a9d8002186",
  username: "nikhita-stord"
});

/*
 * Here I am creating 6 nodes
 */

// Reno - Initialze data source
var reno_source = new carto.source.SQL("SELECT * FROM carto_js_reno");
var reno_style = new carto.style.CartoCSS(`
  #layer {
  polygon-fill: ramp([ground_transit], (#084594, #4292c6, #6baed6, #c6dbef, #eff3ff), jenks);
  polygon-comp-op: darken;
  }
  #layer::outline {
  line-width: 0.02;
  line-color: #ffffff;
  line-opacity: 0.5;
  }
`);

var reno_layer = new carto.layer.Layer(reno_source, reno_style);
// ----------------------------------------------------------------

// Atlanta  Initialze data source
var atlanta_source = new carto.source.SQL("SELECT * FROM carto_js_atlanta");
var atlanta_style = new carto.style.CartoCSS(`
  #layer {
  polygon-fill: ramp([ground_transit], (#084594, #4292c6, #6baed6, #c6dbef, #eff3ff), jenks);
  polygon-comp-op: darken;
  }
  #layer::outline {
  line-width: 0.02;
  line-color: #ffffff;
  line-opacity: 0.5;
  }
`);
var atlanta_layer = new carto.layer.Layer(atlanta_source, atlanta_style);
// ----------------------------------------------------------------

// Dallas  Initialze data source
var dallas_source = new carto.source.SQL("SELECT * FROM carto_js_dallas");
var dallas_style = new carto.style.CartoCSS(`
  #layer {
  polygon-fill: ramp([ground_transit], (#084594, #4292c6, #6baed6, #c6dbef, #eff3ff), jenks);
  polygon-comp-op: darken;
  }
  #layer::outline {
  line-width: 0.02;
  line-color: #ffffff;
  line-opacity: 0.5;
  }
`);
var dallas_layer = new carto.layer.Layer(dallas_source, dallas_style);
// ----------------------------------------------------------------

// Las Vegas  Initialze data source
var las_vegas_source = new carto.source.SQL("SELECT * FROM carto_js_las_vegas");
var las_vegas_style = new carto.style.CartoCSS(`
  #layer {
  polygon-fill: ramp([ground_transit], (#084594, #4292c6, #6baed6, #c6dbef, #eff3ff), jenks);
  polygon-comp-op: darken;
  }
  #layer::outline {
  line-width: 0.02;
  line-color: #ffffff;
  line-opacity: 0.5;
  }
`);
var las_vegas_layer = new carto.layer.Layer(las_vegas_source, las_vegas_style);
// ----------------------------------------------------------------

// chicago  Initialze data source
var chicago_source = new carto.source.SQL("SELECT * FROM carto_js_chicago");
var chicago_style = new carto.style.CartoCSS(`
  #layer {
  polygon-fill: ramp([ground_transit], (#084594, #4292c6, #6baed6, #c6dbef, #eff3ff), jenks);
  polygon-comp-op: darken;
  }
  #layer::outline {
  line-width: 0.02;
  line-color: #ffffff;
  line-opacity: 0.5;
  }
`);
var chicago_layer = new carto.layer.Layer(chicago_source, chicago_style);
// ----------------------------------------------------------------

// north_haven  Initialze data source
var north_haven_source = new carto.source.SQL("SELECT * FROM carto_js_north_haven");
var north_haven_style = new carto.style.CartoCSS(`
  #layer {
  polygon-fill: ramp([ground_transit], (#084594, #4292c6, #6baed6, #c6dbef, #eff3ff), jenks);
  polygon-comp-op: darken;
  }
  #layer::outline {
  line-width: 0.02;
  line-color: #ffffff;
  line-opacity: 0.5;
  }
`);
var north_haven_layer = new carto.layer.Layer(north_haven_source, north_haven_style);
// ----------------------------------------------------------------

/*
 * Here I have finished adding the 6 nodes
 */

// This function gets all checked values
function getSelectedCheckboxValues(name) {
  const checkboxes = document.querySelectorAll(`input[name="${name}"]:checked`);
  let values = [];
  checkboxes.forEach(checkbox => {
    values.push(checkbox.value);
  });
  if (values.length == 0){
    alert('Please select at least one node');
    //the statements after throw won't be executed
    throw 'JS stops here';
  } else {
    return values;
  }
}

// this is the button to change layers
var btn = document.querySelector("#btn");
// This listens to the click and Apply
btn.addEventListener("click", event => {
  
  // Don't remove layers if current client is empty
  if (client.getLayers().length > 0){
    client.removeLayers(client.getLayers());
  }

  // make the selected node array
  let selected_nodes = getSelectedCheckboxValues("node");
  //console.log(selected_nodes);

  // make Node STORD graphic
  // making th in ('Reno','Atlanta', etc.) statement
  let selected_nodes_string = "(";
  for(let i=0;i<selected_nodes.length;i++){
    selected_nodes_string += "'";
    selected_nodes_string += selected_nodes[i];
    selected_nodes_string += "'";
    if(i < selected_nodes.length-1){
      selected_nodes_string += ",";
    }
  }
  selected_nodes_string += ")";
  //console.log(selected_nodes_string);
 
  let stord_logo_where_query = "WHERE name in " + selected_nodes_string;
  let stord_logo_final_query = "SELECT * FROM stord_markets " + stord_logo_where_query
  
  var stord_logo_source = new carto.source.SQL(stord_logo_final_query);
  //console.log(stord_logo_final_query);
  var stord_logo_style = new carto.style.CartoCSS(`
    #layer {
    marker-width: 40.5;
    marker-fill: #EE4D5A;
    marker-fill-opacity: 0.9;
    marker-file: url('https://s3.amazonaws.com/com.cartodb.users-assets.production/production/nikhita-stord/assets/20210510170728Symbol%20White%20Black.png');
    marker-allow-overlap: true;
    marker-line-width: 1;
    marker-line-color: #FFFFFF;
    marker-line-opacity: 1;
    }
  `);
  
  var stord_logo_layer = new carto.layer.Layer(stord_logo_source, stord_logo_style);
  // end of making Node STORD Graphic
  
  // loop through array to add node layers
  for (const node of selected_nodes) {
    if (node == "Reno") {
      client.addLayer(reno_layer);
    } else if (node == "Atlanta") {
      client.addLayer(atlanta_layer);
    } else if (node == "Dallas"){
      client.addLayer(dallas_layer);
    } else if (node == "Las Vegas"){
      client.addLayer(las_vegas_layer);
    } else if (node == "Chicago"){
      client.addLayer(chicago_layer);
    } else if (node == "North Haven"){
      client.addLayer(north_haven_layer);
    }
  }
  // adding STORD logo to map
  client.addLayer(stord_logo_layer);
  //console.log(stord_logo_layer);
  
  // Add the data to the map as a layer
  client.getLeafletLayer().addTo(map);
  client.on('error', function (clientError) {
    console.error(clientError.message);
  });
  
  
  // ------------ Start of Formula Calculation ------------------------- //
  
  // Get an array of all layers from the client, including the Logo Layer
  let current_layers_array = client.getLayers();
  

  // datasets of nodes 
  let reno_query_string = " carto_js_reno ";
  let atlanta_query_string = " carto_js_atlanta ";
  let dallas_query_string = " carto_js_dallas ";
  let las_vegas_query_string = " carto_js_las_vegas ";
  let chicago_query_string = " carto_js_chicago ";
  let north_haven_query_string = " carto_js_north_haven ";
  
  
  // a dictionary to map node name and node query string
  let node_dict = {"Reno":reno_query_string, "Atlanta":atlanta_query_string, "Dallas":dallas_query_string, "Las Vegas":las_vegas_query_string,"Chicago":chicago_query_string, "North Haven":north_haven_query_string};

  // 2 Node Dynamic Query
  let n2_from_string = "FROM" + node_dict[selected_nodes[0]] + "f," + node_dict[selected_nodes[1]] + "s ";
  let n2_select_string = "SELECT least(f.zone, s.zone) as zone, least(f.ground_transit, s.ground_transit) as ground_transit, f.population as population ";
  let n2_where_string = "WHERE f.destination_zip = s.destination_zip";
  let n2_final_query = n2_select_string + n2_from_string + n2_where_string;
  
  // 3 Node Dynamic Query
  let n3_from_string = "FROM" + node_dict[selected_nodes[0]] + "f," + node_dict[selected_nodes[1]] + "s, " + node_dict[selected_nodes[2]] + "w ";
  let n3_select_string = "SELECT least(f.zone, s.zone, w.zone) as zone, least(f.ground_transit, s.ground_transit, w.ground_transit) as ground_transit, f.population as population ";
  let n3_where_string = "WHERE f.destination_zip = s.destination_zip and w.destination_zip = s.destination_zip";
  let n3_final_query = n3_select_string + n3_from_string + n3_where_string;
  
  // 4 Node Dynamic Query
  let n4_from_string = "FROM" + node_dict[selected_nodes[0]] + "f," + node_dict[selected_nodes[1]] + "s, " + node_dict[selected_nodes[2]] + "w, " + node_dict[selected_nodes[3]] + "x ";
  let n4_select_string = "SELECT least(f.zone, s.zone, w.zone, x.zone) as zone, least(f.ground_transit, s.ground_transit, w.ground_transit, x.ground_transit) as ground_transit, f.population as population ";
  let n4_where_string = "WHERE f.destination_zip = s.destination_zip and w.destination_zip = s.destination_zip and x.destination_zip = w.destination_zip";
  let n4_final_query = n4_select_string + n4_from_string + n4_where_string;
  
  // 5 Node Dynamic Query
  let n5_from_string = "FROM" + node_dict[selected_nodes[0]] + "f," + node_dict[selected_nodes[1]] + "s, " + node_dict[selected_nodes[2]] + "w, " + node_dict[selected_nodes[3]] + "x, " + node_dict[selected_nodes[4]] + "y ";
  let n5_select_string = "SELECT least(f.zone, s.zone, w.zone, x.zone, y.zone) as zone, least(f.ground_transit, s.ground_transit, w.ground_transit, x.ground_transit, y.ground_transit) as ground_transit, f.population as population ";
  let n5_where_string = "WHERE f.destination_zip = s.destination_zip and w.destination_zip = s.destination_zip and x.destination_zip = w.destination_zip and y.destination_zip = x.destination_zip";
  let n5_final_query = n5_select_string + n5_from_string + n5_where_string;
  
  // 6 Node Dynamic Query
  let n6_from_string = "FROM" + node_dict[selected_nodes[0]] + "f," + node_dict[selected_nodes[1]] + "s, " + node_dict[selected_nodes[2]] + "w, " + node_dict[selected_nodes[3]] + "x, " + node_dict[selected_nodes[4]] + "y, " + node_dict[selected_nodes[5]] + "z ";
  let n6_select_string = "SELECT least(f.zone, s.zone, w.zone, x.zone, y.zone, z.zone) as zone, least(f.ground_transit, s.ground_transit, w.ground_transit, x.ground_transit, y.ground_transit, z.ground_transit) as ground_transit, f.population as population ";
  let n6_where_string = "WHERE f.destination_zip = s.destination_zip and w.destination_zip = s.destination_zip and x.destination_zip = w.destination_zip and y.destination_zip = x.destination_zip and z.destination_zip = y.destination_zip";
  let n6_final_query = n6_select_string + n6_from_string + n6_where_string;
  
  // number of node selection 
  if (selected_nodes.length == 1) {
    var current_layer = current_layers_array[0];
    var current_source = current_layer.getSource();
    var copy_current_source = new carto.source.SQL("SELECT * FROM " + node_dict[selected_nodes[0]]);
  } else if (selected_nodes.length == 2){
    var current_source = new carto.source.SQL(n2_final_query);
    var copy_current_source = new carto.source.SQL(n2_final_query);
  } else if (selected_nodes.length == 3){
    var current_source = new carto.source.SQL(n3_final_query);
    var copy_current_source = new carto.source.SQL(n3_final_query);
  } else if (selected_nodes.length == 4){
    var current_source = new carto.source.SQL(n4_final_query);
    var copy_current_source = new carto.source.SQL(n4_final_query);
  } else if (selected_nodes.length == 5){
    var current_source = new carto.source.SQL(n5_final_query);
    var copy_current_source = new carto.source.SQL(n5_final_query);
  } else if (selected_nodes.length == 6){
    var current_source = new carto.source.SQL(n6_final_query);
    var copy_current_source = new carto.source.SQL(n6_final_query);
  } 
  // end of Dynamic Query
  
  
  // Create formula Dataview - avg Zone 
  const zone_formulaDataview = new carto.dataview.Formula(current_source, "zone", {
    operation: carto.operation.AVG
  });
  
  // Create formula Dataview - avg transit time
  const transit_formulaDataview = new carto.dataview.Formula(current_source, "ground_transit", {
    operation: carto.operation.AVG
  });
  
  // adding the formulaViews to the client
  client.addDataview(zone_formulaDataview);
  client.addDataview(transit_formulaDataview);
  
  zone_formulaDataview.on("dataChanged", data => {
    let operation_string = zone_formulaDataview.getData().operation;
    let result_string = zone_formulaDataview
      .getData()
      .result.toString()
      .slice(0, 5);
    document.getElementsByName("zone_output")[0].value = result_string;
  });

  client.addDataview(transit_formulaDataview);

  transit_formulaDataview.on("dataChanged", data => {
    let operation_string = transit_formulaDataview.getData().operation;
    let result_string = transit_formulaDataview
      .getData()
      .result.toString()
      .slice(0, 5);
    document.getElementsByName("transit_output")[0].value = result_string;
  });
  
  zone_formulaDataview.on("error", error => {
    alert(error.message);
    //console.log('The error is here');
  });
  
  
  transit_formulaDataview.on("error", error => {
    alert(error.message);
    //console.log('The error is here');
  });
  
  
  
  //-------------------two-day-percent calc ---------------------------------------------//
  // make a copy of current source
  		// Create a filter by ground transit less than 3 days
  const ground_transit_Filter = new carto.filter.Range('ground_transit', { lt: 3});

  // Add filter to the existing source
  copy_current_source.addFilter(ground_transit_Filter);
  
  // Create formula Dataview - two-day-percent calc
  const percent_transit_formulaDataview = new carto.dataview.Formula(copy_current_source, "population", {
    operation: carto.operation.SUM
  });
  
  // adding the formulaViews to the client
  client.addDataview(percent_transit_formulaDataview);
  
  percent_transit_formulaDataview.on("dataChanged", data => {
    let operation_string = percent_transit_formulaDataview.getData().operation;
    let result = percent_transit_formulaDataview
      .getData()
      .result / 306654447 * 100;
    let result_string = result.toString().slice(0, 5) + "%";
    document.getElementsByName("percent_output")[0].value = result_string;
  });
  
  
});

// end of change layer button



