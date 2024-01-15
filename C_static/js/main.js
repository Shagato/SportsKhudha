// JavaScript logic for sliding the images
const slider = document.querySelector('.slider');
const slides = document.querySelectorAll('.slide');
const indicatorsContainer = document.querySelector('.indicators');

let slideIndex = 0;

function showSlides() {
  if (slider && slides) {
    slides.forEach((slide, index) => {
      slide.style.transform = `translateX(${(index - slideIndex) * 100}%)`;
    });
  }

  if (indicatorsContainer) {
    // Update active indicator
    const indicators = document.querySelectorAll('.indicator');
    if (indicators) {
      indicators.forEach((indicator, index) => {
        indicator.classList.remove('active-indicator');
        if (index === slideIndex) {
          indicator.classList.add('active-indicator');
        }
      });
    }
  }
}

function nextSlide() {
  if (slides) {
    slideIndex = (slideIndex + 1) % slides.length;
    showSlides();
  }
}

function prevSlide() {
  if (slides) {
    slideIndex = (slideIndex - 1 + slides.length) % slides.length;
    showSlides();
  }
}

if (indicatorsContainer && slides) {
  // Create indicators
  for (let i = 0; i < slides.length; i++) {
    const indicator = document.createElement('span');
    indicator.classList.add('indicator');
    if (i === 0) {
      indicator.classList.add('active-indicator');
    }
    indicator.addEventListener('click', () => {
      slideIndex = i;
      showSlides();
    });
    indicatorsContainer.appendChild(indicator);
  }

  setInterval(nextSlide, 3000); // Auto slide change every 3 seconds
}
