export default function HomePage() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '20%' }}>
      <h1>Hello, welcome to GlobiFYE's chatbot!</h1>
      <p>How may I help you today?</p>
      <Link href="/chat">
        <a
          style={{
            display: 'inline-block',
            padding: '10px 20px',
            fontSize: '16px',
            marginTop: '20px',
            backgroundColor: '#0070f3',
            color: 'white',
            textAlign: 'center',
            borderRadius: '5px',
            textDecoration: 'none',
            cursor: 'pointer',
          }}
        >
          Prepare me for an interview
        </a>
      </Link>
    </div>
  );
}