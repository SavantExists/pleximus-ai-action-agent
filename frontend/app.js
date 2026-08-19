const messages = document.getElementById("messages");

const activity = document.getElementById("activity");

const activityContent =
    document.getElementById("activityContent");

const input =
    document.getElementById("userInput");


function suggest(text) {

    input.value = text;

    input.focus();

}


function addMessage(text, type) {

    const message =
        document.createElement("div");

    message.className =
        `message ${type}`;

    message.innerHTML = `
        <div class="message-bubble">
            ${text}
        </div>
    `;

    messages.appendChild(message);

    document.querySelector(".chat-area").scrollTop =
        document.querySelector(".chat-area").scrollHeight;
}


function showActivity(tool, details) {

    activity.classList.remove("hidden");

    activityContent.innerHTML += `

        <div class="tool-call">

            <div class="tool-call-icon">
                ${getIcon(tool)}
            </div>

            <div>

                <strong>${tool}</strong>

                <small>
                    ${details}
                </small>

            </div>

        </div>

    `;

}


function getIcon(tool) {

    if (tool.includes("weather"))
        return "🌤️";

    if (tool.includes("currency"))
        return "💱";

    if (tool.includes("text"))
        return "🔤";

    if (tool.includes("calculate"))
        return "🧮";

    return "⚡";

}


async function sendMessage() {

    const text = input.value.trim();

    if (!text)
        return;

    addMessage(text, "user");

    input.value = "";

    /*
       DEMO MODE

       Later this function will call
       your Python backend.
    */

    activity.classList.remove("hidden");

    activityContent.innerHTML = "";

    showActivity(
        "AI Agent",
        "Analyzing request and selecting tools..."
    );

    setTimeout(() => {

        let response =
            "Your request has been received by the AI action agent.";

        if (
            text.toLowerCase().includes("weather")
        ) {

            showActivity(
                "get_weather",
                "Fetching live weather data..."
            );

            response =
                "The weather tool would now retrieve the latest weather information and return the result to the agent.";

        }

        else if (
            text.toLowerCase().includes("currency") ||
            text.toLowerCase().includes("usd") ||
            text.toLowerCase().includes("inr")
        ) {

            showActivity(
                "convert_currency",
                "Fetching current exchange rate..."
            );

            response =
                "The currency tool would retrieve the latest exchange rate and calculate the conversion.";

        }

        else if (
            text.toLowerCase().includes("word") ||
            text.toLowerCase().includes("uppercase")
        ) {

            showActivity(
                "text_utility",
                "Processing text..."
            );

            response =
                "The text utility would analyze or transform the supplied text.";

        }

        else {

            showActivity(
                "calculate",
                "Executing mathematical operation..."
            );

            response =
                "The calculator tool would evaluate the requested expression.";

        }

        setTimeout(() => {

            document.getElementById(
                "activityStatus"
            ).textContent = "COMPLETED";

            addMessage(
                response,
                "agent"
            );

        }, 600);

    }, 500);

}


input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);