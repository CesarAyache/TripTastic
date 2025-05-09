function validateForm(event) {
    localStorage.setItem("loggedInUserEmail", email);
    event.preventDefault();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.message === "Login successful") {
            window.location.href = "homepage.html";
        }
    });
}

function validateSignUp(event) {
    localStorage.setItem("loggedInUserEmail", email);
    event.preventDefault();
    let name = document.getElementById("nameSign").value.trim();
    let email = document.getElementById("emailSign").value.trim();
    let age = document.getElementById("ageSign").value.trim();
    let password = document.getElementById("passSign").value.trim();

    fetch('http://127.0.0.1:5000/signup', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name, email, age, password })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.message === "User created successfully") {
            window.location.href = "homepage.html";
        }
    });
    // function adminLogin(event) {
    //     event.preventDefault();
    //     const email = document.getElementById("adminEmail").value;
    //     const password = document.getElementById("adminPass").value;
      
    //     fetch("http://127.0.0.1:5000/admin-login", {
    //       method: "POST",
    //       headers: { "Content-Type": "application/json" },
    //       body: JSON.stringify({ email, password }),
    //     })
    //       .then((res) => res.json())
    //       .then((data) => {
    //         alert(data.message);
    //         if (data.message === "Admin login successful") {
    //           window.location.href = "admin_dashboard.html";
    //         }
    //       });
    //   }
      
}
