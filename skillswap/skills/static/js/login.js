document.addEventListener("DOMContentLoaded", function() {

    const form = document.getElementById("loginForm");

    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();

            fetch("/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: document.getElementById("loginUsername").value,
                    password: document.getElementById("loginPassword").value
                })
            })
            .then(response => response.json())
            .then(data => {

                const message = document.getElementById("loginMessage");

                if (data.access) {

                    localStorage.setItem("access_token", data.access);

                    fetch("/save-session/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            username: document.getElementById("loginUsername").value
                        })
                    }).then(() => {
                        window.location.href = "/";
                    });

                } else {
                    message.style.color = "red";
                    message.innerText = "Invalid credentials.";
                }

            })
            .catch(error => {
                document.getElementById("loginMessage").innerText = "Something went wrong.";
            });
        });
    }

});