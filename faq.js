document.addEventListener("DOMContentLoaded", () => {
    const questions = document.querySelectorAll(".faq-question");
  
    questions.forEach(button => {
      button.addEventListener("click", () => {
        const answer = button.nextElementSibling;
  
        // Close all other answers
        document.querySelectorAll(".faq-answer").forEach(ans => {
          if (ans !== answer) {
            ans.classList.remove("open");
          }
        });
  
        // Toggle this one
        answer.classList.toggle("open");
      });
    });
  });
  