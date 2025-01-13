import React from "react";
import { loadStripe } from "@stripe/stripe-js";

const stripePromise = loadStripe("pk_test_51QU51aEb1r0toAUQRzJWvaYMHOaa0G88WxsVV1KoWUnTR5wS9YNnC6XHBxVQTk8uwapmSiM1RDYn8cHwTEjNoVCG00l6UqosbM"); // Chiave pubblica di Stripe

function App() {
  const handlePayment = async (plan) => {
    try {
      const response = await fetch("http://localhost:8000/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan }),
      });

      const data = await response.json();
      if (data.sessionId) {
        const stripe = await stripePromise;
        await stripe.redirectToCheckout({ sessionId: data.sessionId });
      } else {
        alert("Errore durante la creazione della sessione");
      }
    } catch (error) {
      console.error(error);
      alert("Errore durante il pagamento");
    }
  };

  return (
    <div>
      <button onClick={() => handlePayment("monthly")}>Abbonamento Mensile</button>
      <button onClick={() => handlePayment("yearly")}>Abbonamento Annuale</button>
    </div>
  );
}

export default App;
