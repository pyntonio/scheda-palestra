document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const userData = {
        username: username,
        email: email,
        password: password
    };

    try {
        const response = await fetch("http://localhost:8000/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById("message").innerHTML = `
                <p>${result.message}</p>
                <p>Un'email di conferma è stata inviata a ${email}.</p>
            `;
        } else {
            throw new Error(result.detail || "Errore nella registrazione.");
        }
    } catch (error) {
        document.getElementById("message").innerHTML = `
            <p style="color: red;">${error.message}</p>
        `;
    }
});
