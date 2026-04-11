console.log('Deal Platform extension content script loaded');

window.addEventListener('message', event => {
  if (event.data?.source === 'deal-platform-extension') {
    console.log('Received event from page:', event.data);
  }
});
