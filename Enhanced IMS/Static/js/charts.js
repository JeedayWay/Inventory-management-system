document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('inventoryChart').getContext('2d');

    // Sample data - in a real app, this would come from the server
    const inventoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Electronics', 'Office Supplies', 'Furniture', 'Food & Beverages'],
            datasets: [{
                label: 'Current Stock Levels',
                data: [65, 59, 80, 45],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(153, 102, 255, 0.6)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});