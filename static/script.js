$(document).ready(function () {
  let selectedMode = "a"; // Default mode
  // appendMessage("Don't worry, I will suggest something creative & best!", "chatgpt");

  let chatHistory = {
    a: [],
    b: [],
    c: [],
  };

  $(".mode-button").click(function () {
    selectedMode = $(this).data("mode");
    console.log(selectedMode);
    $(".mode-button").removeClass("active");
    $(this).addClass("active");

    $(".chat-box").empty(); // Clear existing chat
    showChatHistory(selectedMode); // Show chat history for the selected mode

    // Smoothly change background color of chat-container
    $(".chat-container").css("background-color", getBackgroundColor(selectedMode));
    $("#send-button").css("background-color", getBackgroundColorButton(selectedMode));

    $("#chat-box").attr("data-mode", selectedMode);

    // Check if selectedMode is 2 and show terms and conditions pop-up
    if (selectedMode === "a") {
      // appendMessage("Don't worry, I will suggest something creative & best!", "chatgpt");
    }

    if (selectedMode === "c") {
      // appendMessage("Latest fashion trends will be blended & tailored with respect to your request", "chatgpt");
    }

    if (selectedMode === "b") {
      // Show your terms and conditions pop-up code here
      // Once the user accepts, display a text box, loading screen, and handle its disappearance
      // You can use jQuery dialogs, modal pop-ups, or any preferred UI library
      // Here's a basic example:

        const termsAccepted = confirm(`Terms and Conditions:
        Our Terms and Conditions outline the agreement between users and our company regarding the utilization of their shopping cart and purchase history data to enhance their shopping experience. Users' consent is obtained to collect and process this data for tailored shopping recommendations. No sensitive personal information is collected, only cart items and purchase history from our platform. Data security is ensured through protective measures, and third-party sharing is not allowed without explicit consent. Users retain control over their data and can opt-out of personalized suggestions. Account deletion results in data removal. We reserve the right to update these terms, and any changes are effective upon posting on our website. Users who continue to use our services accept these terms.
        By continuing, you acknowledge that you have read, understood, and agreed to these Terms and Conditions.
        Do you accept? (Ok/Cancel)`);
        // if (termsAccepted) {
        //   // Show the input text box
        //   const inputTextBox =  prompt("Enter any of your Social Media URL");
        // }
        // isAccepted = true;
      
        
        // Show loading screen
        showLoadingIndicator();

        // Simulate loading by delaying the disappearance of the loading screen
        setTimeout(function () {
          hideLoadingIndicator();
          // appendMessage("Hi! I will suggest, something especially tailored for you!", "chatgpt");
          // RevertChange
          // const fs = require('fs');
          // const path ='user_other_data.csv'
          // if(fs.existsSync(path)){
            // appendMessage("Personal Data Loaded", "chatgpt");
          // }else{
            // appendMessage("Personal Data Not Loaded, Kindly Update  your Profile", "chatgpt");
          // }
          // RevertChange
        }, 200); // 2000 milliseconds (2 seconds) delay
       
        
        // loadingDiv.classList.add("chat-message", "chatgpt");
        // loadingDiv.innerHTML = `Instagram Account Connected`;

      }
    

  });

  $("#send-button").click(function () {
    var userMessage = $("#user-input").val();
    if (userMessage.trim() === "") return;

    // Store the user message in the chat history for the selected mode
    chatHistory[selectedMode].push({ sender: "user", message: userMessage });

    appendMessage(userMessage, "user");
    showLoadingIndicator();

    $.post("/", { user_message: userMessage, mode: selectedMode }, function (data) {
      hideLoadingIndicator();

      // Store the bot reply in the chat history for the selected mode
      chatHistory[selectedMode].push({ sender: "bot", message: data.bot_reply });

      appendImg(data.bot_reply, "chatgpt");
    });

    $("#user-input").val("");
  });

  function showChatHistory(mode) {
    const chatBox = $("#chat-box");
    chatBox.empty(); // Clear chat box
    const modeHistory = chatHistory[mode];
    for (const entry of modeHistory) {
      appendMessage(entry.message, entry.sender);
    }
  }





  $(".mode-button").click(function () {
    const newMode = $(this).data("mode");
    if (newMode === selectedMode) return;

    $(".mode-button").removeClass("active");
    $(this).addClass("active");
    selectedMode = newMode;

    $("#chat-box").fadeOut(200, function () {
      $(this).attr("data-mode", selectedMode).fadeIn(200);
    });
  });

  $(".mode-button").click(function () {
    selectedMode = $(this).data("mode");
    $(".mode-button").removeClass("active");
    $(this).addClass("active");
    
    // Smoothly change background color of chat-container
    $(".chat-container").css("background-color", getBackgroundColor(selectedMode));
    
    $("#chat-box").attr("data-mode", selectedMode);
  });

  $("#send-button").click(function () {
    var userMessage = $("#user-input").val();
    if (userMessage.trim() === "") return;

    appendMessage(userMessage, "user");
    showLoadingIndicator();

    $.post("/", { user_message: userMessage, mode: selectedMode }, function (data) {
      hideLoadingIndicator();
      appendImg(data.bot_reply, "chatgpt");
      appendLink();
    });

    $("#user-input").val("");
  });

  function appendLink(){
    const messageDiv = document.createElement("div");
    const aTag = document.createElement("a");
    aTag.href = "/listproducts"
    aTag.textContent = "Buy"
    messageDiv.appendChild(aTag);
    $("#chat-box").append(messageDiv);
  }

  function appendImg(message, sender) {
    const messageDiv = document.createElement("div");
    const imgTag = document.createElement("img");
    const brTag = document.createElement("br");
    const brTag2 = document.createElement("br");
    imgTag.src = message;
    imgTag.width = 400;
    messageDiv.appendChild(imgTag);
    const aTag = document.createElement("a");
    aTag.href = "/buy"
    aTag.classList.add("buy-link");
    aTag.textContent = " Buy now "
    messageDiv.appendChild(brTag);
    messageDiv.appendChild(brTag2);
    messageDiv.appendChild(aTag);
    $("#chat-box").append(messageDiv);
  }

  function appendMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message", sender);
    messageDiv.textContent = message;
    $("#chat-box").append(messageDiv);
    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
  }

  function showLoadingIndicator() {
    const loadingDiv = document.createElement("div");
    loadingDiv.classList.add("chat-message", "chatgpt");
    loadingDiv.innerHTML = `<div class="loading-indicator"><img src="/static/loading.gif" width="30" /></div>`;
    $("#chat-box").append(loadingDiv);
    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
  }

  function hideLoadingIndicator() {
    const loadingIndicator = document.querySelector(".loading-indicator");
    if (loadingIndicator) {
      loadingIndicator.parentNode.remove();
    }
  }

  function getBackgroundColorButton(mode) {
    // Adjust these colors based on your Neumorphism style
    if (mode === "a") return "rgb(242, 61, 126)"; // Example background color for Mode A
    if (mode === "b") return "rgba(0, 123, 255)"; // Example background color for Mode B
    if (mode === "c") return "rgba(1, 184, 149)"; // Example background color for Mode C
  }

  function getBackgroundColor(mode) {
    // Adjust these colors based on your Neumorphism style
    if (mode === "a") return "rgba(252, 120, 168, 0.2)"; // Example background color for Mode A
    if (mode === "b") return "rgba(0, 123, 255,0.2)"; // Example background color for Mode B
    if (mode === "c") return "rgba(1, 184, 149, 0.2)"; // Example background color for Mode C
  }

});
