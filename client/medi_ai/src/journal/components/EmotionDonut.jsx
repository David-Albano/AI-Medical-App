import React, { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { fetchEmotionProportion } from '../calls/journalAPIs';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

// Register Chart.js elements and plugins
ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

export default function EmotionDonut() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        data: [],
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
        ],
      },
    ],
  });

  useEffect(() => {
    fetchEmotionProportion().then(data => {
      const counts = data.map(d => d.count);
      const total = counts.reduce((a, b) => a + b, 0);

      setChartData({
        labels: data.map(d => d.emotion),
        datasets: [
          {
            data: counts,
            backgroundColor: [
              '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
            ],
          },
        ],
        total: total,
      });
    });
  }, []);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          pointStyle: 'circle',
          font: { size: 14 },
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const dataset = context.dataset;
            const total = dataset.data.reduce((a, b) => a + b, 0);
            const value = dataset.data[context.dataIndex];
            const percentage = ((value / total) * 100).toFixed(1);
            return ` value: ${value} - (${percentage}%)`;
          },
        },
      },
      datalabels: {
        color: '#fff',
        font: { weight: 'bold', size: 14 },
        formatter: (value, context) => {
          const dataset = context.chart.data.datasets[0].data;
          const total = dataset.reduce((a, b) => a + b, 0);
          const percentage = ((value / total) * 100).toFixed(0);
          return percentage > 0 ? `${percentage}%` : '';
        },
      },
    },
  };

  return (
    <div style={{ height: '620px' }}>
      <Doughnut data={chartData} options={options} />
    </div>
  );
}
