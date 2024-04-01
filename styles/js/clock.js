// Function to update the countdown timer
function updateCountdown() {
    // Set the release date and time 
    const releaseDate = new Date('2025-02-25T00:00:00');
    const currentDate = new Date();
  
    // Calculate the time difference between the current date and release date
    const difference = releaseDate - currentDate;
  
    // Calculate days, hours, minutes, and seconds
    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);
  
    // Display the countdown timer
    document.getElementById('days').textContent = days;
    document.getElementById('hours').textContent = hours;
    document.getElementById('minutes').textContent = minutes;
    document.getElementById('seconds').textContent = seconds;

    setTimeout(updateCountdown, 1000);
  }

  updateCountdown();