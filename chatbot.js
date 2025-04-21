function toggleChatbot() {
    const bot = document.getElementById('chatbot');
    bot.style.display = bot.style.display === 'flex' ? 'none' : 'flex';
    bot.style.flexDirection = 'column';
  }
  
  function handleChatKey(event) {
    if (event.key === 'Enter') {
      const input = document.getElementById('chat-input');
      const message = input.value.trim();
      if (message !== "") {
        addMessage("You", message);
        botReply(message);
        input.value = "";
      }
    }
  }
  
  function addMessage(sender, text) {
    const container = document.getElementById('chat-messages');
    const message = document.createElement('div');
    message.innerHTML = `<strong>${sender}:</strong> ${text}`;
    container.appendChild(message);
    container.scrollTop = container.scrollHeight;
  }
  
  function botReply(userMsg) {
    let reply = "Sorry, I didn't understand. Try asking about canceling or loyalty points.";
    const msg = userMsg.toLowerCase();
  
    if (["hi", "hello", "hey", "heyy", "hiya", "good morning", "good afternoon", "good evening"].some(greet => msg.includes(greet))) {
      reply = "Hi there! 👋 How can I assist you today?";
    } else if (msg.includes("how are you")) {
      reply = "I'm just a bot, but I'm here and ready to help you! 😊";
    } else if (msg.includes("cancel")) {
      reply = "To cancel your trip, go to 'My Bookings' and click 'Cancel'.";
    } else if (msg.includes("loyalty")) {
      reply = "You earn loyalty points with each trip! Use them at checkout.";
    } else if (msg.includes("refund")) {
      reply = "Refunds are processed in 3–5 business days.";
    } else if (msg.includes("agent") || msg.includes("talk to someone")) {
      reply = "A support agent will reach out to you within 24 hours or you can try calling them using the phone shown on our website.";
    } else if (msg.includes("book") && msg.includes("trip")) {
      reply = "You can book a new trip through the 'Explore' section. Let me know if you need help!";
    } else if (msg.includes("thank")) {
      reply = "You're welcome! 😊 Let me know if there's anything else I can do for you.";
    }
  
    setTimeout(() => addMessage("Bot", reply), 500);
  }
  
  