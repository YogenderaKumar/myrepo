document.addEventListener("DOMContentLoaded", () => {
  const currentYear = document.getElementById("year");
  if (currentYear) {
    currentYear.textContent = new Date().getFullYear();
  }
});
