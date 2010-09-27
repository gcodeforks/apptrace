/*!
 * Apptrace JavaScript
 *
 * Copyright 2010, Tobias Rodaebel
 */
$(function () {
  var options = {
    lines: { show: true },
    points: { show: true },
    xaxis: { tickDecimals: 0, tickSize: 1 },
    legend: { container: $('#legend'), noColumns: 10 }
  };

  var memory = $("#memory");
  var memory_series = {};
  var memory_data = [];

  var details = $("#details");
  var details_series = {};
  var details_data = [];

  function updateData(data) {
    var records = JSON.parse(data);

    memory_series = {};
    memory_data = [];

    details_series = {};
    details_data = [];

    if (records.length == 0)
      return null;

    for (i=0; i<records.length; i++) {
      var record = records[i];
      var cumulated_size = 0;

      for (j=0; j<record.entries.length; j++) {
        var entry = record.entries[j];

        if (!details_series[entry.name]) {
          details_series[entry.name] = {label: entry.name, data: []};
        }

        details_series[entry.name].data.push([record.index,
                                              entry.dominated_size]);

        cumulated_size += entry.dominated_size;
      }

      if (!memory_series['cumulated']) {
        memory_series['cumulated'] = {label: 'cumulated', data: [],
                                      lines: {fill: true}};
      }

      memory_series['cumulated'].data.push([record.index,
                                            cumulated_size]);
    }
    for (var key in memory_series)
      memory_data.push(memory_series[key]);

    for (var key in details_series)
      details_data.push(details_series[key]);

    $.plot(memory, memory_data, options);
    $.plot(details, details_data, options);
  }

  $('#refresh').click(function() {
    var button = $(this);
    var url = button.siblings('a').attr('href');
    $.ajax({
      url: url,
      method: 'GET',
      success: updateData
    });
  });

  $('#refresh').click();
});
