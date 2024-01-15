document.addEventListener('DOMContentLoaded', function() {
    let slideIndex = 0;
    const slides = document.querySelectorAll('.slide');
    
    function showSlides() {
        slides.forEach(slide => {
            slide.style.display = 'none';
        });
    
        if (slideIndex === slides.length) {
            slideIndex = 0;
        } else if (slideIndex < 0) {
            slideIndex = slides.length - 1;
        }
    
        slides[slideIndex].style.display = 'block';
    }
    
    function nextSlide() {
        slideIndex++;
        showSlides();
    }
    
    function prevSlide() {
        slideIndex--;
        showSlides();
    }
    
    // Show the first slide initially
    showSlides();

    // Adding event listeners for Previous and Next buttons
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');

    prevButton.addEventListener('click', prevSlide);
    nextButton.addEventListener('click', nextSlide);
});
