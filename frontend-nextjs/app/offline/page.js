'use client'

export default function OfflinePage() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      padding: '2rem',
      textAlign: 'center',
      fontFamily: 'Inter, system-ui, sans-serif',
    }}>
      <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>
        📡
      </div>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>
        You're Offline
      </h1>
      <p style={{ color: '#666', maxWidth: '400px', lineHeight: 1.6 }}>
        It looks like you've lost your internet connection.
        WISHI will be back as soon as you're online again.
      </p>
      <button
        onClick={() => window.location.reload()}
        style={{
          marginTop: '1.5rem',
          padding: '0.75rem 2rem',
          backgroundColor: '#E60023',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          fontSize: '1rem',
          fontWeight: 600,
          cursor: 'pointer',
        }}
      >
        Try Again
      </button>
    </div>
  )
}
