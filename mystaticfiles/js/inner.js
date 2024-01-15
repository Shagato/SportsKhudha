document.addEventListener('DOMContentLoaded', function() {
    // Wait for the DOM content to be fully loaded
  
    // Function to check and set innerHTML for an element
    function setInnerHTML(selector, content) {
      const element = document.querySelector(selector);
      if (element) {
        element.innerHTML = content;
      } else {
        console.error(`Element with selector '${selector}' not found!`);
      }
    }
  
    // Call the setInnerHTML function with your element selectors and content
    setInnerHTML('.your-element-class', 'New HTML content');
  });
  