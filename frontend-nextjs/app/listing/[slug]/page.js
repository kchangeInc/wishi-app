import { notFound } from 'next/navigation';

const mockListings = {
  'hyundai-i20-chennai': {
    title: 'Hyundai i20 under ₹6L in Chennai',
    price: '₹5.5L',
    location: 'Chennai',
    description: 'Matched listing for your wishlist.'
  }
};

export default function ListingPage({ params }) {
  const listing = mockListings[params.slug];
  if (!listing) {
    notFound();
  }

  return (
    <main style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      <h1>{listing.title}</h1>
      <p>{listing.description}</p>
      <p><strong>Price:</strong> {listing.price}</p>
      <p><strong>Location:</strong> {listing.location}</p>
    </main>
  );
}
