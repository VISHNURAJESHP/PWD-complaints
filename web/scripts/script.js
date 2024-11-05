document.addEventListener("DOMContentLoaded", function() {
    // Fetch News Content from Backend API
    fetchNewsContent();
});

// Fetch news content from backend and update news ticker
async function fetchNewsContent() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/news/');  // Update URL if needed
        const data = await response.json();

        if (response.ok) {
            document.getElementById('news-content').innerText = data.news;
        } else {
            console.error("Failed to fetch news:", data);
            document.getElementById('news-content').innerText = "Failed to load news.";
        }
    } catch (error) {
        console.error("Error fetching news:", error);
        document.getElementById('news-content').innerText = "Failed to load news.";
    }
}

// Register a new user and handle OTP flow
async function registerUser(email, name, password) {
    try {
        const response = await fetch("http://127.0.0.1:8000/userregister", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                name: name,
                password: password,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            // Redirect to OTP entry page if registration was successful
            window.location.href = `/otp-verification.html?email=${encodeURIComponent(email)}`;
        } else {
            alert(data.message || "Registration failed.");
        }
    } catch (error) {
        console.error("Registration error:", error);
        alert("An error occurred during registration.");
    }
}

// Log in a user and handle JWT storage
async function loginUser(email, password) {
    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                password: password,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            alert("Login successful");
            // Store JWT in cookies with secure attributes
            document.cookie = `jwt=${data.jwt}; path=/; samesite=None; secure`;
            // Redirect to dashboard or home page
            window.location.href = "/dashboard.html";
        } else {
            alert(data.detail || "Login failed.");
        }
    } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred during login.");
    }
}
