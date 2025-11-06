import React, { useEffect, useState } from 'react';
import CalendarHeatmap from 'react-calendar-heatmap';
import 'react-calendar-heatmap/dist/styles.css';
import '../styles/JournalDashboardsPage.css'
import { fetchDailyJournalActivity } from '../calls/journalAPIs';

export default function JournalHeatmap() {
  const [data, setData] = useState([]);
  const [totalEntries, setTotalEntries] = useState(0);
  const [maxCount, setMaxCount] = useState(1);

  const currentYear = new Date().getFullYear();

  useEffect(() => {
    fetchDailyJournalActivity().then(entries => {
      const formatted = entries.map(d => ({
        date: d.date_only,
        count: d.count
      }));

      const total = formatted.reduce((sum, e) => sum + e.count, 0);
      const max = Math.max(...formatted.map(e => e.count), 1);

      setData(formatted);
      setTotalEntries(total);
      setMaxCount(max);
    });
  }, []);

  // Color intensity adapts to actual max activity
  const getColorClass = value => {
    if (!value) return 'color-empty';
    const intensity = value.count / maxCount;
    if (intensity > 0.75) return 'color-scale-4';
    if (intensity > 0.5) return 'color-scale-3';
    if (intensity > 0.25) return 'color-scale-2';
    return 'color-scale-1';
  };

  return (
    <div style={{ textAlign: 'center', height: '280px' }}>
      <h3 style={{ marginBottom: '0.7rem' }}>{currentYear} Journal Activity</h3>
      <div style={{ marginBottom: '0.8rem', color: '#555', fontSize: '0.9rem' }}>
        Total entries this year: <strong>{totalEntries}</strong>
      </div>
      <br />

      <CalendarHeatmap
        startDate={new Date(currentYear, 0, 1)}
        endDate={new Date()}
        values={data}
        classForValue={getColorClass}
        showWeekdayLabels
      />
    </div>
  );
}
