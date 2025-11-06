
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { fetchSentimentOverTime } from '../calls/journalAPIs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function SentimentChart() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Average Sentiment Score',
        data: [],
        borderColor: 'rgba(75,192,192,1)',
        backgroundColor: 'rgba(75,192,192,0.2)',
        fill: true,
      }
    ]
  });

  useEffect(() => {
    fetchSentimentOverTime().then(data => {

      let sentimentalData = {
        labels: data?.map((d) => d?.date_only),
        datasets: [
          {
            label: 'Average Sentiment Score',
            data: data?.map((d) => d?.avg_sentiment_score),
            borderColor: 'rgba(75,192,192,1)',
            backgroundColor: 'rgba(75,192,192,0.2)',
            fill: true,
          }
        ]
      };

      setChartData(sentimentalData)

    });
  }, []);


  return (
    <>
      {chartData.labels ? <Line data={chartData} /> : <p>Loading chart...</p>}
    </>
  );
}
