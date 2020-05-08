"use strict";
const DailyChart = function (src) {
    const the = this;

    if (!document.getElementById(src)) {
        return;
    }

    const ctx = document.getElementById(src).getContext("2d");

    const dayLabels = Array(30);
    for (const i of dayLabels.keys()) {
        dayLabels[i] = moment().subtract(29 - i, 'day').format('MM/DD');
    }

    const mainConfig = {
        type: 'line',
        data: {
            labels: dayLabels,
            datasets: []
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: false,
            },
            tooltips: {
                enabled: true,
                intersect: false,
                mode: 'nearest',
                bodySpacing: 5,
                yPadding: 10,
                xPadding: 10,
                caretPadding: 0,
                displayColors: false,
                titleFontColor: '#ffffff',
                cornerRadius: 4,
                footerSpacing: 0,
                titleSpacing: 0
            },
            legend: {
                display: false,
                labels: {
                    usePointStyle: false
                }
            },
            hover: {
                mode: 'index'
            },
            scales: {
                xAxes: [{
                    display: false,
                    scaleLabel: {
                        display: false,
                        labelString: 'Day'
                    },
                    ticks: {
                        display: false,
                        beginAtZero: true,
                    }
                }],
                yAxes: [{
                    display: false,
                    scaleLabel: {
                        display: false,
                        labelString: 'Device'
                    },
                    gridLines: {
                        color: '#eef2f9',
                        drawBorder: false,
                        offsetGridLines: true,
                        drawTicks: false
                    },
                    ticks: {
                        display: false,
                        beginAtZero: true
                    }
                }]
            },
            elements: {
                point: {
                    radius: 0,
                    borderWidth: 0,
                    hoverRadius: 0,
                    hoverBorderWidth: 0
                }
            },
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0
                }
            }
        }
    };

    const chart = new Chart(ctx, mainConfig);

    const Plugin = {
        set: function (label, data, color) {
            if (!Array.isArray(data)) {
                console.error("'data' parameter of DailyChart.set() is only allowed array type.");
            }

            const borderWidth = 2;

            const gradient = ctx.createLinearGradient(0, 0, 0, 100);
            gradient.addColorStop(0, Chart.helpers.color(color).alpha(0.3).rgbString());
            gradient.addColorStop(1, Chart.helpers.color(color).alpha(0).rgbString());

            const dataset = {
                label: label,
                data: data,
                borderColor: color,
                borderWidth: borderWidth,
                backgroundColor: gradient
            };

            chart.data.datasets.push(dataset);

            chart.update();
        }
    };

    for (const key in Plugin) {
        the[key] = Plugin[key];
    }

    return the;
};

"use strict";
const MonthlyChart = function (src) {
    const the = this;

    if (!document.getElementById(src)) {
        return;
    }

    const ctx = document.getElementById(src).getContext("2d");

    const monthLabels = Array(12);
    for (const i of monthLabels.keys()) {
        monthLabels[i] = moment().subtract(11 - i, 'months').format('YYYY/MM');
    }

    const mainConfig = {
        type: 'line',
        data: {
            labels: monthLabels,
            datasets: []
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: false,
            scales: {
                xAxes: [{
                    categoryPercentage: 0.35,
                    barPercentage: 0.70,
                    display: true,
                    scaleLabel: {
                        display: false,
                        labelString: 'Day'
                    },
                    gridLines: false,
                    ticks: {
                        display: true,
                        beginAtZero: true,
                        fontColor: KTApp.getBaseColor('shape', 3),
                        fontSize: 13,
                        padding: 10
                    }
                }],
                yAxes: [{
                    categoryPercentage: 0.35,
                    barPercentage: 0.70,
                    display: true,
                    scaleLabel: {
                        display: false,
                        labelString: 'Value'
                    },
                    gridLines: {
                        color: KTApp.getBaseColor('shape', 2),
                        drawBorder: false,
                        offsetGridLines: false,
                        drawTicks: false,
                        borderDash: [3, 4],
                        zeroLineWidth: 1,
                        zeroLineColor: KTApp.getBaseColor('shape', 2),
                        zeroLineBorderDash: [3, 4]
                    },
                    ticks: {
                        display: true,
                        beginAtZero: true,
                        fontColor: KTApp.getBaseColor('shape', 3),
                        fontSize: 13,
                        padding: 10
                    }
                }]
            },
            title: {
                display: false,
            },
            hover: {
                mode: 'index'
            },
            tooltips: {
                enabled: true,
                intersect: false,
                mode: 'nearest',
                bodySpacing: 5,
                yPadding: 10,
                xPadding: 10,
                caretPadding: 0,
                displayColors: false,
                titleFontColor: '#ffffff',
                cornerRadius: 4,
                footerSpacing: 0,
                titleSpacing: 0
            },
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0
                }
            }
        }
    };

    const chart = new Chart(ctx, mainConfig);

    const Plugin = {
        set: function (dataset) {
            if (!Array.isArray(dataset)) {
                console.error("'dataset' parameter of MonthlyChart.set() is only allowed array type.");
            }

            chart.data.datasets = dataset;

            chart.update();

        },

        add: function (dataset) {
            chart.data.datasets.push(dataset);

            chart.update();

        }
    };


    for (const key in Plugin) {
        the[key] = Plugin[key];
    }

    return the;
};