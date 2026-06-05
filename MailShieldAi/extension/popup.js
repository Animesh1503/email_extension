document.addEventListener("DOMContentLoaded", async () => {

    const privacyMode =
        document.getElementById("privacyMode");

    const analyzeBtn =
        document.getElementById("analyzeBtn");

    const loading =
        document.getElementById("loading");

    const result =
        document.getElementById("result");

    const riskScore =
        document.getElementById("riskScore");

    const threatType =
        document.getElementById("threatType");

    const explanation =
        document.getElementById("explanation");

    const progressFill =
        document.getElementById("progressFill");

    const progressPercent =
        document.getElementById("progressPercent");

    let progressInterval;

    // Load saved privacy mode
    chrome.storage.local.get(
        ["privacyMode"],
        (data) => {
            privacyMode.checked =
                data.privacyMode || false;
        }
    );

    // Save privacy mode
    privacyMode.addEventListener(
        "change",
        () => {
            chrome.storage.local.set({
                privacyMode:
                    privacyMode.checked
            });
        }
    );

    function startProgress() {

        let progress = 0;

        progressFill.style.width = "0%";
        progressPercent.textContent = "0%";

        clearInterval(progressInterval);

        progressInterval = setInterval(() => {

            if (progress < 90) {

                progress +=
                    Math.random() * 4 + 1;

                if (progress > 90) {
                    progress = 90;
                }

                progressFill.style.width =
                    `${progress}%`;

                progressPercent.textContent =
                    `${Math.floor(progress)}%`;
            }

        }, 250);
    }

    function finishProgress() {

        clearInterval(progressInterval);

        progressFill.style.width = "100%";

        progressPercent.textContent =
            "100%";
    }

    analyzeBtn.addEventListener(
        "click",
        async () => {

            try {

                loading.classList.remove(
                    "hidden"
                );

                result.classList.add(
                    "hidden"
                );

                startProgress();

                const [tab] =
                    await chrome.tabs.query({
                        active: true,
                        currentWindow: true
                    });

                chrome.tabs.sendMessage(
                    tab.id,
                    {
                        action:
                            "GET_EMAIL_DATA"
                    },
                    async (emailData) => {

                        if (
                            chrome.runtime
                                .lastError
                        ) {

                            clearInterval(
                                progressInterval
                            );

                            loading.classList.add(
                                "hidden"
                            );

                            alert(
                                "Open a Gmail email before analyzing."
                            );

                            return;
                        }

                        if (
                            !emailData
                        ) {

                            clearInterval(
                                progressInterval
                            );

                            loading.classList.add(
                                "hidden"
                            );

                            alert(
                                "Could not read email content."
                            );

                            return;
                        }

                        const payload = {
                            privacyMode:
                                privacyMode.checked,

                            sender:
                                emailData.sender,

                            subject:
                                emailData.subject,

                            body:
                                emailData.body,

                            links:
                                emailData.links
                        };

                        try {

                            const response =
                                await fetch(
                                    "http://localhost:8000/analyze",
                                    {
                                        method:
                                            "POST",

                                        headers: {
                                            "Content-Type":
                                                "application/json"
                                        },

                                        body:
                                            JSON.stringify(
                                                payload
                                            )
                                    }
                                );

                            const data =
                                await response.json();

                            finishProgress();

                            await new Promise(
                                resolve =>
                                    setTimeout(
                                        resolve,
                                        300
                                    )
                            );

                            riskScore.textContent =
                                data.risk_score ||
                                "N/A";

                            threatType.textContent =
                                data.threat_type ||
                                "Unknown";

                            explanation.textContent =
                                data.explanation ||
                                "No explanation available.";

                            loading.classList.add(
                                "hidden"
                            );

                            result.classList.remove(
                                "hidden"
                            );

                        } catch (
                            error
                        ) {

                            clearInterval(
                                progressInterval
                            );

                            loading.classList.add(
                                "hidden"
                            );

                            alert(
                                "Backend server not running."
                            );

                            console.error(
                                error
                            );
                        }
                    }
                );

            } catch (error) {

                clearInterval(
                    progressInterval
                );

                loading.classList.add(
                    "hidden"
                );

                console.error(error);
            }
        }
    );
});