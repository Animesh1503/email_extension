document.addEventListener("DOMContentLoaded", async () => {

    const privacyMode =
        document.getElementById("privacyMode");

    const analyzeBtn =
        document.getElementById("analyzeBtn");

    const loading =
        document.getElementById("loading");

    const result =
        document.getElementById("result");

    const explanation =
        document.getElementById("explanation");

    const riskValue =
        document.getElementById("riskValue");

    const riskLevel =
        document.getElementById("riskLevel");

    const bottomRisk =
        document.getElementById("bottomRisk");

    const bottomThreat =
        document.getElementById("bottomThreat");

    const progressFill =
        document.getElementById("progressFill");

    const progressPercent =
        document.getElementById("progressPercent");

    const closeBtn =
        document.querySelector(".close-btn");

    let progressInterval;

    // Close popup

    if (closeBtn) {
        closeBtn.addEventListener(
            "click",
            () => window.close()
        );
    }

    // Load privacy mode

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

    function updateRiskDisplay(
        score,
        threat
    ) {

        const riskText =
            `${score}/100`;

        riskValue.textContent =
            riskText;

        bottomRisk.textContent =
            riskText;

        riskLevel.textContent =
            threat;

        bottomThreat.textContent =
            threat;

        // SAFE

        if (score <= 30) {

            riskLevel.style.color =
                "#3EE089";

            bottomThreat.style.color =
                "#3EE089";

            bottomThreat.style.background =
                "rgba(62,224,137,.12)";
        }

        // SUSPICIOUS

        else if (score <= 70) {

            riskLevel.style.color =
                "#FFD166";

            bottomThreat.style.color =
                "#FFD166";

            bottomThreat.style.background =
                "rgba(255,209,102,.12)";
        }

        // HIGH RISK

        else {

            riskLevel.style.color =
                "#FF624D";

            bottomThreat.style.color =
                "#FF624D";

            bottomThreat.style.background =
                "rgba(255,98,77,.12)";
        }
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

                    async (
                        emailData
                    ) => {

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

                            const score =
                                Number(
                                    data.risk_score
                                ) || 0;

                            const threat =
                                data.threat_type ||
                                "Unknown";

                            updateRiskDisplay(
                                score,
                                threat
                            );

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

                console.error(
                    error
                );
            }
        }
    );
});