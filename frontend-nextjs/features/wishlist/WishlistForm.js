export default function WishlistForm() {
  return (
    <form style={{ display: 'grid', gap: '0.75rem', maxWidth: '420px' }}>
      <label>
        Wishlist title
        <input type="text" name="title" placeholder="i20 under ₹6L in Chennai" />
      </label>
      <label>
        Location
        <input type="text" name="location" placeholder="Chennai" />
      </label>
      <label>
        Max price
        <input type="number" name="price" placeholder="600000" />
      </label>
      <button type="submit">Save wishlist</button>
    </form>
  );
}
