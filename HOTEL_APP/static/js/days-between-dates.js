function daysBetween(start, end) {
    // Convert the start and end dates to milliseconds
    const startTime = start.getTime();
    const endTime = end.getTime();
  
    // Calculate the difference between the start and end dates in milliseconds
    const difference = endTime - startTime;
  
    // Divide the difference by the number of milliseconds in a day
    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
  
    // Return the number of days
    return days;
  }
  
  // Create two input elements for the start and end dates
  const startInput = document.getElementById("start-date");
  const endInput = document.getElementById("end-date");
  
  // Create a text input element to display the number of days
  const daysInput = document.getElementById("days");
  
  // When the start and end dates are changed, update the number of days
  startInput.addEventListener("change", () => {
    const start = new Date(startInput.value);
    const end = new Date(endInput.value);
    const days = daysBetween(start, end);
    daysInput.value = days;
  });
  
  endInput.addEventListener("change", () => {
    const start = new Date(startInput.value);
    const end = new Date(endInput.value);
    const days = daysBetween(start, end);
    daysInput.value = days;
  });