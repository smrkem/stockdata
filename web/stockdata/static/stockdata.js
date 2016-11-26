$( document ).ready(function() {
    if ($("#price-volume-trend-graph").length) {
      console.log( "got data - woot!" );
      pv_trend_data = $("#price-volume-trend-graph").data('pv_data');
      console.log(pv_trend_data);
    }

});
