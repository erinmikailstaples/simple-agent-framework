import { useState } from 'react';
import Head from 'next/head';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [location, setLocation] = useState('');
  const [agentResponse, setAgentResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!location.trim()) {
      setError('Please enter a location');
      return;
    }

    setLoading(true);
    setError('');
    setAgentResponse('');

    try {
      // This is where we would make an API call to the backend
      // For now, we'll use a placeholder response
      // TODO: Implement actual API call to the weather vibes agent
      const response = await fetch('/api/weather-vibes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ location }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from agent');
      }

      const data = await response.json();
      setAgentResponse(data.response || 'No response received from agent');
    } catch (err) {
      setError('Failed to get a response from the agent. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Weather Vibes</title>
        <meta name="description" content="Get your weather vibes based on your location" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <span className={styles.highlight}>Weather Vibes</span>
        </h1>

        <p className={styles.description}>
          Enter your location to get weather information and music recommendations!
        </p>

        <div className={styles.formContainer}>
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.inputGroup}>
              <label htmlFor="location" className={styles.label}>
                Location:
              </label>
              <input
                id="location"
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="Enter city name or zip code"
                className={styles.input}
                required
              />
            </div>
            <button type="submit" className={styles.button} disabled={loading}>
              {loading ? 'Getting Vibes...' : 'Get Weather Vibes'}
            </button>
          </form>

          {error && <p className={styles.error}>{error}</p>}

          {loading && <p className={styles.loading}>Loading your weather vibes...</p>}

          {agentResponse && (
            <div className={styles.results}>
              <h2>Weather Information</h2>
              <div className={styles.responseText}>
                {agentResponse.split('\n').map((line, index) => (
                  <p key={index}>{line}</p>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className={styles.footer}>
        <p>Powered by Weather Vibes Agent</p>
      </footer>
    </div>
  );
}

