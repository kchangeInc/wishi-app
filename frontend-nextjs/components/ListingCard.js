export default function ListingCard({ listing }) {
  return (
    <article style={{ border: '1px solid #ddd', borderRadius: '12px', padding: '1rem', background: '#fff' }}>
      <h3>{listing.title}</h3>
      <p>{listing.location}</p>
      <p><strong>{listing.price}</strong></p>
      <a href={`/listing/${listing.id}`}>View listing</a>
    </article>
  );
}
