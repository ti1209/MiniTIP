"use strict";
const TIPDeviceDashboard = function () {
    const firstPortlet = function () {
        const portlet = $("#first-portlet");

        if (portlet === 0) {
            return false;
        }

        const dailyChart = new DailyChart('first-chart');

        $.ajax({
            type: "GET",
            url: "/api_device/daily_chart/?today_count",
            dataType: "json",
            error: function () {
                alert("Error in First Portlet");
            },
            success: function (data) {
                dailyChart.set('', data['daily_count'], '#41D3BD');
                $(function (){
                    $('#today_count').append(data['today_count']);
                })
            }
        });
    };

    const secondPortlet = function () {
        const portlet = $("#second-portlet");

        if (portlet === 0) {
            return false;
        }

        $.ajax({
            type: "GET",
            url: "/api_device/statistics_per_period/",
            dataType: "json",
            error: function () {
                alert("Error in Second Portlet");
            },
            success: function (data) {
                $(function () {
                    $('#daily_average').append(data['daily_average']);
                    $('#total_sum').append(data['total_sum']);
                    $('#weekly_average').append(data['weekly_average']);
                    $('#weekly_sum').append(data['weekly_sum']);
                    $('#monthly_average').append(data['monthly_average']);
                    $('#monthly_sum').append(data['monthly_sum']);
                })
            }
        });
    };

    const thirdPortlet = function () {
        const portlet = $("#third-portlet");

        if (portlet === 0) {
            return false;
        }

        $.ajax({
            type: "GET",
            url: "/api_device/policy_applied_status/",
            dataType: "json",
            error: function () {
                alert("Error in Third Portlet");
            },
            success: function (data) {
                $(function () {
                    $('#non-default').append(data['non_default'] + '대&nbsp;/');
                    $('#total').append(data['total'] + '대');
                    $('#non-default-rate').append(data['non_default_rate'] + '%');
                    $('#progress-bar').attr('style', 'width: ' + data['non_default_rate'] + '%');
                })
            }
        });
    };

    const fourthPortlet = function () {
        const portlet = $("#fourth-portlet");

        if (portlet === 0) {
            return false;
        }

        const monthlyChart = new MonthlyChart('fourth-chart');

        $.ajax({
            type: "GET",
            url: "/api_device/monthly_chart/",
            dataType: "json",
            error: function () {
                alert("Error in Fourth Portlet!");
            },
            success: function (data) {
                monthlyChart.add({
                    backgroundColor: '#67D5B5',
                    borderWidth: 2,
                    borderColor: '#67D5B5',
                    fill: false,
                    lineTension: 0,
                    data: data['monthly_count']
            });
            }
        });
    };

    const fifthPortlet = function () {
        const portlet = $("#fifth-portlet");

        if (portlet === 0) {
            return false;
        }

        $.ajax({
            type: "GET",
            url: "/api_device/os_version_list/",
            dataType: "json",
            error: function () {
                alert("Error in Fifth Portlet");
            },
            success: function (data) {
                $(function () {
                    $('#windows').append(data['windows_count'] + '대');
                    $('#mac').append(data['macOS_count'] + '대');
                    $('#linux').append(data['linux_count'] + '대');
                    $('#unknown').append(data['unknown_count'] + '대');
                })
            }
        });
    };

    const sixthPortlet = function () {
        const portlet = $("#sixth-portlet");

        if (portlet.length === 0) {
            return false;
        }

        $.ajax({
            type: "GET",
            url: "/api_device/license_valid_status/",
            dataType: "json",
            error: function () {
                alert("Error in Sixth Portlet!");
            },
            success: function (result) {
                var ctx = document.getElementById('sixth-chart').getContext('2d');

                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['무효', '유효'],
                        datasets: [{
                            backgroundColor: ['#a5d296', '#60c5ba'],
                            data: [result['invalid'], result['valid']]
                        }]
                    },
                    options: {
                        tooltips: {
                            mode: 'nearest',
                            intersect: false
                        },
                        responsive: true,
                        legend: {
                            position: 'left',
                        },
                    }
                });
            }
        });
    };

    const seventhPortlet = function () {
        const portlet = $("#seventh-portlet");

        if (portlet.length === 0) {
            return false;
        }

        $.ajax({
            type: "GET",
            url: "/api_device/version_update_status/",
            dataType: "json",
            error: function () {
                alert("Error in Seventh Portlet");
            },
            success: function (result) {
                var ctx = document.getElementById('seventh-chart').getContext("2d");


                new Chart(ctx, {
                    type: 'horizontalBar',
                    data: {
                        datasets: [{
                            data: [result['update_count'], result['outdated_count']],
                            backgroundColor: ['#5CAB7D', '#44633F']
                        }],
                        labels: ['Old', 'New']
                    },
                    options: {
                        responsive: true,
                        legend: {
                            display: false,
                        },
                        animation: {
                            animateScale: true,
                            animateRotate: true
                        }
                    }
                });
            }
        });
    };

    const eighthPortlet = function () {
        const portlet = $("#eighth-portlet");

        if (portlet === 0) {
            return false;
        }

        $.ajax({
            type: "GET",
            url: "/api_device/device_active_status/",
            dataType: "json",
            error: function () {
                alert("Error in Eight Portlet");
            },
            success: function (data) {
                $(function () {
                    $('#online').append(data['online'] + '%');
                    $('#online-progress-bar').attr('style', 'width: ' + data['online'] + '%');
                    $('#thirty').append(data['thirty'] + '%');
                    $('#thirty-progress-bar').attr('style', 'width: ' + data['thirty'] + '%');
                    $('#ninety').append(data['ninety'] + '%');
                    $('#ninety-progress-bar').attr('style', 'width: ' + data['ninety'] + '%');
                })
            }
        });
    };

    // const ninthPortlet = function () {
    //     const portlet = $("#ninth-portlet");
    //
    //     if (portlet === 0) {
    //         return false;
    //     }
    //
    //     const table = portlet.find('table');
    //     table.DataTable();
    // };
    //
    // const tenthPortlet = function () {
    //     const portlet = $("#tenth-portlet");
    //
    //     if (portlet === 0) {
    //         return false;
    //     }
    //
    //     const table = portlet.find('table');
    //     table.DataTable();
    // };
    //
    // const eleventhPortlet = function () {
    //     const portlet = $("#eleventh-portlet");
    //
    //     if (portlet === 0) {
    //         return false;
    //     }
    //
    //     const table1 = portlet.find('#eleventh-table1');
    //     const datatable1 = table1.DataTable({
    //         scrollX: true
    //     });
    //
    //     const table2 = portlet.find('#eleventh-table2');
    //     const datatable2 = table2.DataTable({
    //         scrollX: true
    //     });
    //
    //     $('a[data-toggle="tab"]').on('shown.bs.tab', function () {
    //         datatable1.columns.adjust();
    //         datatable2.columns.adjust();
    //     });
    // };
    //
    // const twelfthPortlet = function () {
    //     const portlet = $("#twelfth-portlet");
    //
    //     if (portlet === 0) {
    //         return false;
    //     }
    //
    //     const table = portlet.find('table');
    //     table.DataTable();
    // };

    return {
        init: function () {
            firstPortlet();
            secondPortlet();
            thirdPortlet();
            fourthPortlet();
            fifthPortlet();
            sixthPortlet();
            seventhPortlet();
            eighthPortlet();
            // ninthPortlet();
            // tenthPortlet();
            // eleventhPortlet();
            // twelfthPortlet();
        }
    };
}();

jQuery(document).ready(function () {
    TIPDeviceDashboard.init();
});