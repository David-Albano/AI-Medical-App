import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../styles/JournalEntryPage.css';  // Import CSS for styling

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const JournalEntryPage = () => {
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [responseData, setResponseData] = useState(null);
    const [error, setError] = useState(null);

    const handleTextChange = (event) => {
        setText(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (text.trim() === '') {
            setError("Text is required!");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            setResponseData(null);
            const response = await axios.post(`${API_BASE_URL}/journal/journal-entry/`, { text });
            setResponseData(response.data);
            setText('');  // Reset the text area
        } catch (err) {
            setError("Failed to submit the journal entry. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="journal-entry-container">
            <div>
                <Link to="/journal-dashboard" className="journal-dashboard-link">
                    <h4>Your Entries Stats</h4>
                </Link>
            </div>

            <div className="journal-entry-card">
                <h1>Write Your Journal Entry</h1>
                <p style={{ color: '#6b7280', marginBottom: '20px' }}>
                    Take a moment to capture what’s on your mind — every thought and feeling matters... <br /> Your thoughts are safe here 💭
                </p>

                <form onSubmit={handleSubmit}>
                    <textarea
                        className="journal-textarea"
                        value={text}
                        onChange={handleTextChange}
                        placeholder="Write your thoughts here..."
                        rows="8"
                    ></textarea>
                    {error && <div className="error-message">{error}</div>}
                    <button type="submit" className="submit-btn" disabled={loading}>
                        {loading ? "Submitting..." : "Submit Entry"}
                    </button>
                </form>

                {responseData && (
                    <div className="feedback-section">
                        <h2 className="reflection-title">
                            Your Reflection Summary
                            <span className="info-icon">ℹ️
                                <span className="tooltip-text">
                                <strong>Sentiment</strong> — Measures the overall tone of your entry (e.g., Positive, Neutral, Negative).  
                                <br /><br />
                                <strong>Score</strong> — Confidence of that sentiment, ranging from 0 to 1 (closer to 1 = higher confidence).  
                                <br /><br />
                                <strong>Emotion</strong> — The dominant emotional tone (e.g., Joy, Sadness, Anger, Calm).  
                                <br /><br />
                                <strong>Emotion Score</strong> — How strongly that emotion was detected (also from 0 to 1).
                                </span>
                            </span>
                        </h2>

                        <div className="feedback-card">
                            <div className="feedback-block sentiment-block">
                                <div className='sub_block_feedback'>
                                    <div className='line_flex_feedback'>
                                        <h3>Sentiment: </h3> <p>{responseData.sentiment}</p>
                                    </div>
                                    <div className='line_flex_feedback'>
                                        <h3>Score: </h3> <p>{responseData.sentiment_score}</p>
                                    </div>
                                </div>

                                <hr />

                                <div className='sub_block_feedback'>
                                    <div className='line_flex_feedback'>
                                        <h3>Emotion: </h3> <p>{responseData.emotion}</p>
                                    </div>
                                    <div className='line_flex_feedback'>
                                        <h3>Score: </h3> <p>{responseData.emotion_score}</p>
                                    </div>
                                </div>
                            </div>

                            <div className="feedback-block emotion-block">
                                {responseData.model_result_justification && (
                                    <p className="justification">
                                        <p style={{fontSize: "11px", fontWeight: "bold"}}>Feedback justification:</p>
                                        <pre>{responseData.model_result_justification}</pre>
                                    </p>
                                )}
                            </div>

                            <div className="feedback-block ai-block">
                                <h3>AI Reflection</h3>
                                <p>{responseData.ai_feedback}</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default JournalEntryPage;
