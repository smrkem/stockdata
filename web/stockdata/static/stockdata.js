$( document ).ready(function() {
    if ($("#price_volume_history_data").length) {
      init_volume_graph($("#price_volume_history_data").data('pv_data'));
    }

});

function init_volume_graph(volume_data) {
  var graph_wrapper = $("#graph_wrapper");

  var graph = $('<div class="graph" id="volume_graph" style="padding: 10px; margin: 10px; border: 1px solid #aaa;">');

  graph_wrapper.append(graph);
    console.log("in init_volume_graph. graph width: " + graph.width());

  var details = $('<div class="graph_details">');
  graph.append(details);
  var title = $('<h2 class="graph_title">');
  start_date = volume_data.pv_data[0].Date;
  end_date = volume_data.pv_data[volume_data.pv_data.length - 1].Date;
  title.text(`Trading Volume History ${start_date} to ${end_date}`);
  details.append(title);


  var plot_wrap = $('<div class="plot_wrap">');
  graph.append(plot_wrap);

  var plot = $('<canvas class="plot"  style="width: 100%;">');
  plot_wrap.append(plot);

  plot_against_date(plot, volume_data.pv_data);

}


function plot_against_date(plot, data) {
  var parts = data[0].Date.split('-');
  var lastDate = new Date(parts[0], parts[1] - 1, parts[2]);

  var parts = data[data.length - 1].Date.split('-');
  var firstDate = new Date(parts[0], parts[1] - 1, parts[2]);

  var oneDay = 24 * 60 * 60 * 1000;
  var numDays = Math.round((lastDate.getTime() - firstDate.getTime()) / oneDay);

  // console.log(firstDate, lastDate);
  // console.log(numDays);
  console.log(plot.width());
  console.log("in plot_against_date. graph_wrapper width: " + $("#graph_wrapper").width());

  var ctx = plot[0].getContext('2d');
  ctx.moveTo(0,0);
  ctx.lineTo(200,100);
  ctx.stroke();

}







function init_price_graph(price_data) {
  console.log(price_data);
  var graph = $('<div class="graph" id="price_graph">');
  var details = $('<div class="graph_details">');
  var title = $('<h2 class="graph_title">');
  start_date = price_data.pv_data[0].Date;
  end_date = price_data.pv_data[price_data.pv_data.length - 1].Date;
  title.text(`Price History ${start_date} to ${end_date}`);
  details.append(title);
  graph.append(details);

  var plot_wrap = $('<div id="plot_wrap">');
  var plot = $('<canvas id="plot">');
  plot_wrap.append(plot);
  graph.append(plot_wrap);
  $("#graph_wrapper").append(graph);
}



















function init_pv_trend_data_graph() {
  max_volume = 0;
  min_volume = 0;
  volume_p75 = 0;
  log_multiplier = 0;
  graph = $("#price-volume-trend-graph");
  // pv_trend_data = graph.data('pv_data');

  // graph.append()
  draw_rects()
  // console.log(pv_trend_data);
}

function draw_rects() {
  rect_width = rect_height = 7;
  rect_horizontal_space = 2;
  rect_vertical_space = 2;
  graph = $("#price-volume-trend-graph");
  month_labels = graph.find("#month-labels");
  grid = graph.find("#day-data-rects");


  pv_trend_data = graph.data('pv_data');
  console.log(pv_trend_data);
  max_volume = pv_trend_data.max_volume;
  min_volume = pv_trend_data.min_volume;
  volume_p75 = pv_trend_data.volume_p75;
  log_multiplier = 1 / Math.log(max_volume);
  left_offset = 0;

  first_date = pv_trend_data.pv_data.pop()
  date_arr = first_date.Date.split("-");
  d = new Date(parseInt(date_arr[0]), parseInt(date_arr[1]) - 1, parseInt(date_arr[2]))
  prevDay = d.getDay();
  prevMonth = d.getMonth();
  top_offset = prevDay * (rect_height + rect_vertical_space);
  opacity = get_rect_opacity(first_date.Volume)

  if (Math.abs(first_date.pct_change) > 3) {
    fill = (first_date.pct_change > 0) ? "#0f0" : "#f00";
  }
  else
    fill = "#aaa";

  grid.append(get_rect(top_offset, left_offset, fill, opacity));

  while (date = pv_trend_data.pv_data.pop()) {
    // console.log(date.Date);
    date_arr = date.Date.split("-");

    // months are zero indexed !!
    d = new Date(parseInt(date_arr[0]), parseInt(date_arr[1]) - 1, parseInt(date_arr[2]))
    currentDay = d.getDay();
    currentMonth = d.getMonth();

    // increase left_offset when current getDay < prev getDay
    if (currentDay < prevDay) {
      left_offset += (rect_width + rect_horizontal_space);
    }

    // add month label when current getMonth != prev getMonth
    if (currentMonth != prevMonth) {
      month_labels.append(get_month_label(currentMonth, left_offset));
    }

    top_offset = currentDay * (rect_height + rect_vertical_space);
    opacity = get_rect_opacity(date.Volume)


    if (Math.abs(date.pct_change) > 2) {
      fill = (date.pct_change > 0) ? "#5abd5a" : "#f00";
      // fill = (date.pct_change > 0) ? "#0f0" : "#f00";
    }
    else
      fill = "#aaa";

    grid.append(get_rect(top_offset, left_offset, fill, opacity));

    prevDay = currentDay;
    prevMonth = currentMonth;
  }
}

function get_rect(top_offset, left_offest, fill, opacity) {
  return $(`<rect style="top: ${top_offset}px; left: ${left_offest}px; background: ${fill}; opacity: ${opacity};"></rect>`);
}

function get_month_label(month, left_offset) {
  var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];
  return $(`<label style="left: ${left_offset}px;">${monthNames[month]}</label>`)
}

function get_rect_opacity(volume) {

  opacity = 0.4 * (1 - (volume_p75 - volume)/volume_p75) + 0.3;
  if (opacity > 1) {
    console.log(opacity);
  }
  // opacity = 0.7 * (1 - (max_volume - volume)/max_volume) + 0.3;
  return opacity;
}
