// TODO: minify
const LINECOLORS = [
  'red',
  'blue',
  'green',
];

function protocolsChart(conversations) {
  // console.debug(`Conversation received:\n${JSON.stringify(conversations, null, 2)}`);
  if (!(conversations instanceof Object)) {
      return;
  }
  const data = {
    datasets: [],
  };
  let min_x = 0;
  let max_x = 0;
  for (let i = 0; i < Object.keys(conversations).length; i++) {
    const protocolName = Object.keys(conversations)[i];
    const protocolData = Object.values(conversations)[i];
    // console.debug(`Protocol: ${protocolName}\nData: ${JSON.stringify(protocolData)}`);
    protocolData.forEach(element => {
      element.x = element.x * 1000;
      if (min_x === 0) { min_x = element.x }
      if (max_x === 0) { max_x = element.x }
      if (element[0] < min_x) { min_x = element.x }
      if (element[0] > max_x) { max_x = element.x }
    });
    // console.debug(`min X = ${min_x} | max X = ${max_x}`);
    const dataset = {
      label: protocolName,
      data: protocolData,
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
          text: 'Data Profile by Protocol',
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
            text: 'Bytes',
            display: true,
          },
          min: 0,
        }
      }
    }
  });
}

function totalDataChart(conversations) {
  const data = {
    labels: [],
    datasets: [],
  };
  const dataset = {
    label: 'Total Data Bytes',
    backgroundColor: [],
    data: [],
  }
  for (let i = 0; i < Object.keys(conversations).length; i++) {
    const protocolName = Object.keys(conversations)[i];
    const protocolData = Object.values(conversations)[i];
    let totalbytes = 0;
    protocolData.forEach(element => {
      totalbytes += element.y;
    });
    data.labels.push(protocolName);
    dataset.backgroundColor.push(LINECOLORS[i]);
    dataset.data.push(totalbytes);
  }
  data.datasets.push(dataset);
  const ctx = document.getElementById('pieChart').getContext('2d');
  return new Chart(ctx, {
    type: 'pie',
    data: data,
    options: {
      // responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Total Data Use by Protocol',
        }
      },
    }
  });
}