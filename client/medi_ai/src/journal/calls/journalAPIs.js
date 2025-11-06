// src/api/journalApi.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const fetchSentimentOverTime = async () => {
  const res = await axios.get(`${API_BASE_URL}/journal/sentiment-over-time/`);
  console.log('\n\n res: ', res.data)
  return res.data;
};

export const fetchEmotionProportion = async () => {
  const res = await axios.get(`${API_BASE_URL}/journal/emotion-proportion/`);
  return res.data;
};

export const fetchDailyJournalActivity = async () => {
  const res = await axios.get(`${API_BASE_URL}/journal/daily-journal-activity/`);
  return res.data;
};
