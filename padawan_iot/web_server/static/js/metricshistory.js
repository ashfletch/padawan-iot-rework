function historyPicker() {
  $('input[name="metricsHistory"]').daterangepicker({
    autoapply: true,
    linkedCalendars: false,
    alwaysShowCalendars: true,
    drops: "auto",
    maxDate: moment.utc().format(),
    timePicker: true,
    timePicker24Hour: true,
    timePickerIncrement: 5,
    ranges: {
      'Last Day': [moment.utc().subtract(1, 'days'), moment.utc()],
      'Last 7 Days': [moment.utc().subtract(6, 'days'), moment.utc()]
    },
    startDate: moment.utc().startOf('minute').subtract(1, 'days'),
    endDate: moment.utc().startOf('minute'),
    locale: {
      format: 'YYYY-MM-DDTHH:mm',
      separator: ' to '
    }
  },
    function (start, end, label) {
      console.log('Date range selected: ' +
        start.format('YYYY-MM-DDThh:mm:ssZ') +
        ' to ' + end.format('YYYY-MM-DDThh:mm:ssZ') +
        ' (predefined range: ' + label + ')');
    });
  $('.drp-calendar.right').hide();
  $('.drp-calendar.left').addClass('single');
  $('.calendar.table').on('DOMSubtreeModified', function () {
    let el = $('.prev.available').parent().children().last();
    if (el.hasClass('next available')) { return; }
    el.addClass('next available');
    el.append('<span></span>');
  });
}

const LINECOLORS = [
  'red',
  'blue',
  'green',
];

function metricsChart(metrics) {
  // console.debug(`Conversation received:\n${JSON.stringify(metrics, null, 2)}`);
  if (!(metrics instanceof Object)) {
    return;
  }
  const data = {
    datasets: [],
  };
  let min_x = 0;
  let max_x = 0;
  for (let i = 0; i < Object.keys(metrics).length; i++) {
    const seriesName = Object.keys(metrics)[i];
    const seriesData = Object.values(metrics)[i];
    // console.debug(`BeamType: ${seriesName}\nData:\n${JSON.stringify(seriesData)}`);
    seriesData.forEach(element => {
      element.x = element.x * 1000;
      if (min_x === 0) { min_x = element.x }
      if (max_x === 0) { max_x = element.x }
      if (element.x < min_x) { min_x = element.x }
      if (element.x > max_x) { max_x = element.x }
    });
    // console.debug(`min X = ${min_x} | max X = ${max_x}`);
    const dataset = {
      label: seriesName,
      data: seriesData,
      borderColor: LINECOLORS[i] || 'black',
      fill: false,
      spanGaps: false,
    };
    console.debug(`Dataset:\n${JSON.stringify(dataset)}`)
    data.datasets.push(dataset);
  }
  const ctx = document.getElementById('tsChart').getContext('2d');
  return new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
      plugins: {
        title: {
          display: true,
          text: 'SNR by Beam Type',
        }
      },
      scales: {
        x: {
          title: {
            text: 'Time Recorded (UTC)',
            display: true,
          },
          type: 'time',
          ticks: {
              callback: function(value, index, values) {
                  if (!values[index]) { return }
                  return moment.utc(values[index]['value']).format();
              }
          }
        },
        y: {
          title: {
            text: 'SNR [dB]',
            display: true,
          },
          min: 0,
        }
      }
    }
  });
}
