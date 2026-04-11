document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('import-listing');
  if (button) {
    button.addEventListener('click', () => {
      chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'import_listing' });
      });
    });
  }
});
