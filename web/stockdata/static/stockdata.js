$( document ).ready(function() {
    if ($("#price-volume-trend-graph").length) {
      init_pv_trend_data_graph();
    }

});

function init_pv_trend_data_graph() {
  console.log( "got data - woot!" );
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
  left_offset = 0;

  first_date = pv_trend_data.pv_data.pop()
  date_arr = first_date.Date.split("-");
  d = new Date(parseInt(date_arr[0]), parseInt(date_arr[1]) - 1, parseInt(date_arr[2]))
  prevDay = d.getDay();
  prevMonth = d.getMonth();
  top_offset = prevDay * (rect_height + rect_vertical_space);
  grid.append(get_rect(top_offset, left_offset, '#ddd'));

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
    grid.append(get_rect(top_offset, left_offset, '#ddd'));

    prevDay = currentDay;
    prevMonth = currentMonth;
  }
}

function get_rect(top_offset, left_offest, fill) {
  return $(`<rect style="top: ${top_offset}px; left: ${left_offest}px; background: ${fill};"></rect>`);
}

function get_month_label(month, left_offset) {
  var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];
  return $(`<label style="left: ${left_offset}px;">${monthNames[month]}</label>`)
}
