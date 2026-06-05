chrome.runtime.onInstalled.addListener(() => {
    console.log("MailShield AI Extension Installed");
});

// Listen for messages from popup/content scripts
chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {

        if (request.action === "PING") {

            sendResponse({
                status: "MailShield Active"
            });
        }

        return true;
    }
);