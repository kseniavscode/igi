document.addEventListener('DOMContentLoaded', function () {

    class MathChartManager {
        constructor() {
            this.xStartInput = document.getElementById('x_start');
            this.xEndInput = document.getElementById('x_end');
            this.xStepInput = document.getElementById('x_step');
            this.epsInput = document.getElementById('epsilon');

            this.plotBtn = document.getElementById('plot_btn');
            this.downloadBtn = document.getElementById('download_chart_btn');
            this.tableBody = document.getElementById('chart_table_body');
            this.canvas = document.getElementById('mathChart');

            this.chartInstance = null; 

            this.init();
        }

        init() {
            this.plotBtn.addEventListener('click', () => this.calculateAndPlot());
            this.downloadBtn.addEventListener('click', () => this.downloadChartImage());
            this.calculateAndPlot();
        }

        exactFunction(x) {
            return Math.log((x + 1) / (x - 1));
        }

        taylorSeries(x, eps) {
            let sum = 0;
            let n = 0;
            let term = 0;
            const maxIterations = 2000; 

            do {
                const denominator = (2 * n + 1) * Math.pow(x, 2 * n + 1);
                term = 1 / denominator;
                sum += term;
                n++;
            } while (Math.abs(2 * term) > eps && n < maxIterations);

            return {
                value: 2 * sum, 
                termsCount: n
            };
        }

        calculateAndPlot() {
            const xStart = parseFloat(this.xStartInput.value);
            const xEnd = parseFloat(this.xEndInput.value);
            const step = parseFloat(this.xStepInput.value);
            const eps = parseFloat(this.epsInput.value);

            if (xStart <= 1) {
                alert('По формуле x должен быть строго больше 1 (|x| > 1)!');
                return;
            }

            const labels = [];      
            const seriesData = [];   
            const exactData = [];    
            const tableRows = [];   

            for (let x = xStart; x <= xEnd + 0.0001; x += step) {
                const roundedX = parseFloat(x.toFixed(2));
                const exactVal = this.exactFunction(roundedX);
                const seriesRes = this.taylorSeries(roundedX, eps);
                const seriesVal = seriesRes.value;
                const error = Math.abs(seriesVal - exactVal);

                labels.push(roundedX);
                seriesData.push(seriesVal);
                exactData.push(exactVal);

                tableRows.push({
                    x: roundedX,
                    n: seriesRes.termsCount,
                    series: seriesVal.toFixed(6),
                    exact: exactVal.toFixed(6),
                    error: error.toExponential(4) 
                });
            }

            this.renderTable(tableRows);
            this.renderChart(labels, seriesData, exactData);
        }

        renderTable(rows) {
            this.tableBody.innerHTML = '';
            rows.forEach(r => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${r.x}</td>
                    <td><span class="badge_terms">${r.n}</span></td>
                    <td>${r.series}</td>
                    <td>${r.exact}</td>
                    <td>${r.error}</td>
                `;
                this.tableBody.appendChild(tr);
            });
        }

        renderChart(labels, seriesData, exactData) {
            if (this.chartInstance) {
                this.chartInstance.destroy();
            }

            const ctx = this.canvas.getContext('2d');

            this.chartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Exact Math F(x) [Math.log]',
                            data: exactData,
                            borderColor: '#029cee', 
                            backgroundColor: 'transparent',
                            borderWidth: 3.5,       
                            borderDash: [7, 7],     
                            pointRadius: 4,         
                            pointBackgroundColor: '#0288d1',
                            tension: 0.3,
                            order: 1              
                        },
                        {
                            label: 'Series F(x) [Taylor Approximation]',
                            data: seriesData,
                            borderColor: '#54f75c', // Насыщенный зеленый
                            backgroundColor: 'rgba(46, 125, 50, 0.08)',
                            borderWidth: 3,
                            pointRadius: 0,         
                            tension: 0.3,
                            order: 2              
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 1200,
                        easing: 'easeInOutQuart'
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Comparison of Taylor Series and Math.log((x+1)/(x-1))',
                            font: { size: 16, weight: 'bold' },
                            color: '#472801'
                        },
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                font: { size: 13, weight: 'bold' }
                            }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Argument (X)',
                                font: { size: 14, weight: 'bold' },
                                color: '#333'
                            },
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Function Value Y = f(X)',
                                font: { size: 14, weight: 'bold' },
                                color: '#333'
                            },
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        }
                    }
                }
            });
        }

        downloadChartImage() {
            if (!this.chartInstance) return;

            const imageURL = this.canvas.toDataURL('image/png');

            const link = document.createElement('a');
            link.download = 'taylor_series_chart_variant11.png';
            link.href = imageURL;
            link.click();
        }
    }

    new MathChartManager();
});