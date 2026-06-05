document.addEventListener("DOMContentLoaded", async () => {
    const privacyMode = document.getElementById("privacyMode");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    const riskScore = document.getElementById("riskScore");
    const threatType = document.getElementById("threatType");
    const explanation = document.getElementById("explanation");

    // Load saved privacy mode setting
    chrome.storage.local.get(["privacyMode"], (data) => {
        privacyMode.checked = data.privacyMode || false;
    });

    // Save privacy mode setting
    privacyMode.addEventListener("change", () => {
        chrome.storage.local.set({
            privacyMode: privacyMode.checked
        });
    });

    analyzeBtn.addEventListener("click", async () => {
        try {
            loading.classList.remove("hidden");
            result.classList.add("hidden");

            // Get current active Gmail tab
            const [tab] = await chrome.tabs.query({
                active: true,
                currentWindow: true
            });

            // Ask content.js for email data
            chrome.tabs.sendMessage(
                tab.id,
                { action: "GET_EMAIL_DATA" },
                async (emailData) => {

                    if (chrome.runtime.lastError) {
                        loading.classList.add("hidden");

                        alert(
                            "Open a Gmail email before analyzing."
                        );
                        return;
                    }

                    if (!emailData) {
                        loading.classList.add("hidden");

                        alert(
                            "Could not read email content."
                        );
                        return;
                    }

                    const payload = {
                        privacyMode: privacyMode.checked,
                        sender: emailData.sender,
                        subject: emailData.subject,
                        body: emailData.body,
                        links: emailData.links
                    };

                    try {

                        const response = await fetch(
                            "http://localhost:8000/analyze",
                            {
                                method: "POST",
                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },
                                body: JSON.stringify(payload)
                            }
                        );

                        const data =
                            await response.json();

                        riskScore.textContent =
                            data.risk_score || "N/A";

                        threatType.textContent =
                            data.threat_type || "Unknown";

                        explanation.textContent =
                            data.explanation ||
                            "No explanation available.";

                        loading.classList.add("hidden");
                        result.classList.remove("hidden");

                    } catch (error) {

                        loading.classList.add("hidden");

                        alert(
                            "Backend server not running."
                        );

                        console.error(error);
                    }
                }
            );

        } catch (error) {
            loading.classList.add("hidden");
            console.error(error);
        }
    });
});