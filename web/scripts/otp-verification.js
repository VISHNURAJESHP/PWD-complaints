// Select all OTP input boxes
const otpInputs = document.querySelectorAll(".otp-input");

// Automatically focus on the next box when a digit is entered
otpInputs.forEach((input, index) => {
    input.addEventListener("input", () => {
        // Move to the next input if a single character is entered
        if (input.value.length === 1 && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }
    });

    input.addEventListener("keydown", (event) => {
        if (event.key === "ArrowRight" || event.key === "Enter") {
            // Move to the next input on right arrow or Enter
            if (index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        } else if (event.key === "ArrowLeft") {
            // Move to the previous input on left arrow
            if (index > 0) {
                otpInputs[index - 1].focus();
            }
        } else if (event.key === "Backspace" && input.value === "") {
            // Move to the previous input on Backspace if current box is empty
            if (index > 0) {
                otpInputs[index - 1].focus();
            }
        }
    });
});

// Function to verify OTP
async function verifyOTP() {
    // Get the OTP value by concatenating each input box's value
    const otp = Array.from(otpInputs).map(input => input.value).join("");

    if (otp.length < otpInputs.length) { // Check if all boxes are filled
        alert("Please enter the complete OTP.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/verify-email", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ otp }), // Sending the combined OTP
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            window.location.href = "/login.html"; // Redirect on successful OTP verification
        } else {
            alert(data.error || "OTP verification failed");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred during OTP verification.");
    }
}

// Event listener for OTP verification button
document.getElementById("verify-otp-button").addEventListener("click", verifyOTP);
