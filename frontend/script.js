const API_URL = "http://127.0.0.1:5000/predict";

const form = document.getElementById("predictionForm");
const button = document.getElementById("predictButton");

const emptyResult = document.getElementById("emptyResult");
const successResult = document.getElementById("successResult");

const predictedPrice = document.getElementById("predictedPrice");

const resultCarName = document.getElementById("resultCarName");
const resultYear = document.getElementById("resultYear");
const resultKms = document.getElementById("resultKms");
const resultTransmission = document.getElementById("resultTransmission");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Get input values
    const carName = document.getElementById("carName").value.trim();
    const year = document.getElementById("year").value;
    const presentPrice = document.getElementById("presentPrice").value;
    const kmsDriven = document.getElementById("kmsDriven").value;
    const fuelType = document.getElementById("fuelType").value;
    const sellerType = document.getElementById("sellerType").value;
    const transmission = document.getElementById("transmission").value;
    const owner = document.getElementById("owner").value;


    // Basic validation
    if (
        !carName ||
        !year ||
        !presentPrice ||
        !kmsDriven ||
        !fuelType ||
        !sellerType ||
        !transmission ||
        owner === ""
    ) {
        alert("Please complete all vehicle details.");
        return;
    }


    // Loading state
    button.classList.add("loading");
    button.querySelector(".button-text").textContent = "Calculating...";
    button.querySelector(".button-arrow").textContent = "•••";


    // Data sent to Flask
    const carData = {
        Car_Name: carName,
        Year: Number(year),
        Present_Price: Number(presentPrice),
        Kms_Driven: Number(kmsDriven),
        Fuel_Type: fuelType,
        Seller_Type: sellerType,
        Transmission: transmission,
        Owner: Number(owner)
    };


    try {

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(carData)
        });


        if (!response.ok) {
            throw new Error("Prediction request failed.");
        }


        const result = await response.json();

        const price = Number(result.predicted_price);
        const aiAdvice = document.getElementById("aiAdvice");

aiAdvice.textContent = "Generating personalized advice...";

try {
    const aiResponse = await fetch("http://127.0.0.1:5000/ai-advice", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            ...carData,
            predicted_price: price
        })
    });

    const aiResult = await aiResponse.json();

    if (aiResponse.ok) {
        aiAdvice.textContent = aiResult.advice;
    } else {
        aiAdvice.textContent = "AI advice could not be generated.";
    }

} catch (error) {
    console.error("AI advice error:", error);
    aiAdvice.textContent = "AI advice could not be generated.";
}

        // Display result
        predictedPrice.textContent = price.toFixed(2);

        resultCarName.textContent = carName;
        resultYear.textContent = year;
        resultKms.textContent = Number(kmsDriven).toLocaleString("en-IN") + " km";
        resultTransmission.textContent = transmission;


        // Switch result card
        emptyResult.style.display = "none";
        successResult.classList.add("visible");


        // Scroll result into view on mobile
        if (window.innerWidth <= 900) {
            document.getElementById("resultCard").scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        }

    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to the prediction server. " +
            "Please make sure the Flask API is running."
        );

    } finally {

        // Restore button
        button.classList.remove("loading");
        button.querySelector(".button-text").textContent = "Estimate car value";
        button.querySelector(".button-arrow").textContent = "→";
    }

});