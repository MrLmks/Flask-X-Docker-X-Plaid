
const context = document.getElementById("graph").getContext("2d")
const element_data_graph = document.getElementById("data_graph")
const category = JSON.parse(element_data_graph.dataset.category)
const amount = JSON.parse(element_data_graph.dataset.amount)

const pie_chart = new Chart(context, {
    type: "pie",
    data: {
        labels: category,
        datasets: [{
            data: amount,
            backgroundColor: [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: "bottom",
            },
            title: {
                display: true,
                text: "Spendings"
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let value = context.parsed;
                        let label = context.label || '';
                        return ` ${label}: ${value.toLocaleString('en-US')} $`;
                    }
                }
            }
        }
    }
});
