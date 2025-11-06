// src/App.js
import React from 'react';
import SentimentChart from '../components/SentimentChart';
import EmotionDonut from '../components/EmotionDonut';
import JournalHeatmap from '../components/JournalHeatmap';

function JournalDashboardsPage() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>Journal Dashboard</h1>

      <div
        style={{
          display: 'flex',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '2rem',
          alignItems: 'start'
        }}
      > 
          <div style={{ display: "flex", flexDirection: "column", gap: "2rem", }}>
              <div style={{ width: "1000px", padding: '1rem', background: '#f9f9f9', borderRadius: '8px', boxShadow: '0 2px 6px rgba(0,0,0,0.1)' }}>
                <h2 style={{ textAlign: 'center' }}>Sentiment Over Time</h2>
                <SentimentChart />
              </div>

              <div style={{width: "1000px",  padding: '1rem', background: '#f9f9f9', borderRadius: '8px', boxShadow: '0 2px 6px rgba(0,0,0,0.1)' }}>
                <h2 style={{ textAlign: 'center' }}>Daily Journal Activity</h2>
                <JournalHeatmap />
              </div>
          </div>

          <div style={{ width: "700px", padding: '1rem', background: '#f9f9f9', borderRadius: '8px', boxShadow: '0 2px 6px rgba(0,0,0,0.1)' }}>
              <h2 style={{ textAlign: 'center' }}>Emotion Proportion</h2>
              <br />
              <EmotionDonut />
          </div>
      </div>
    </div>
  );
}

export default JournalDashboardsPage;
