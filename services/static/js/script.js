const serviceList = document.getElementById('service-list');
const popup = document.getElementById('popup');
const closePopupButton = document.getElementById('close-popup');

// Variables for handling the timeout
let popupTimeout;

// Fetch data from the API
async function fetchServices() {
  try {
    const response = await fetch('http://127.0.0.1:8000/services/api/service/');  // Replace with actual API endpoint
    const services = await response.json();

    if (Array.isArray(services)) {
      renderFlashcards(services);
    }
  } catch (error) {
    console.error('Error fetching services:', error);
  }
}

// 2. Render the flashcards
function renderFlashcards(services) {
  services.forEach(service => {
    const flashcard = document.createElement('div');
    flashcard.className = 'flashcard';
    flashcard.innerText = service.name;
    flashcard.onclick = () => openPopup(service);
    
    serviceList.appendChild(flashcard);
  });
}

// 3. Open popup with service details
function openPopup(service) {
  // Set the service details in the popup
  document.getElementById('popup-title').innerText = service.name;
  document.getElementById('popup-docs').innerText = service.required_docs || 'Not available';
  document.getElementById('popup-fee').innerText = service.serv_fee2 || 'Not available';
  document.getElementById('popup-time').innerText = service.serv_time || 'Not available';

  const sampleDocsElement = document.getElementById('popup-sample-docs');

  // Clear previous iframe (if any)
  const existingIframe = document.getElementById('sample-doc-iframe');
  if (existingIframe) {
    existingIframe.remove();
  }

  // if (service.file_url) {
  //   // Add a clickable label and embed the PDF in an iframe
  //   sampleDocsElement.innerHTML = `<span>Sample Document:</span>`;
  //   const iframe = document.createElement('iframe');
  //   iframe.id = 'sample-doc-iframe';
  //   iframe.src = service.file_url;
  //   iframe.width = '100%';
  //   iframe.height = '400px';
  //   iframe.style.border = '1px solid #ccc';
  //   sampleDocsElement.appendChild(iframe);
  // } else {
  //   sampleDocsElement.innerText = 'Not available';
  // }

  // Show the popup
  popup.style.display = 'flex';

  // Reset and start the inactivity timer
  resetPopupTimeout();
  document.addEventListener('mousemove', resetPopupTimeout);
    document.addEventListener('keypress', resetPopupTimeout);
    document.addEventListener('click', resetPopupTimeout);
    document.addEventListener('scroll', resetPopupTimeout);  // To detect scroll activity
    document.addEventListener('touchstart', resetPopupTimeout);

  // Close popup on clicking outside
  popup.onclick = (event) => {
    if (event.target === popup) {
      closePopup();
    }
  };
}

// 4. Reset the inactivity timer
function resetPopupTimeout() {
  clearTimeout(popupTimeout);

  // Set the timeout to close the popup after 30 seconds of inactivity
  popupTimeout = setTimeout(closePopup, 10000);
}

// 5. Close the popup
function closePopup() {
  popup.style.display = 'none';
  clearTimeout(popupTimeout);
}

// Event listener for the close button
closePopupButton.addEventListener('click', closePopup);

// 6. Initialize the app
fetchServices();