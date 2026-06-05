function extractEmailData() {
    try {

        // Gmail Subject
        const subjectElement = document.querySelector("h2");

        // Gmail Sender
        const senderElement = document.querySelector(
            "span[email]"
        );

        // Gmail Email Body
        const bodyElement = document.querySelector(
            "div.a3s"
        );

        const subject =
            subjectElement?.innerText?.trim() || "";

        const sender =
            senderElement?.getAttribute("email") || "";

        const body =
            bodyElement?.innerText?.trim() || "";

        // Extract Links
        const links = [];

        if (bodyElement) {

            const anchorTags =
                bodyElement.querySelectorAll("a");

            anchorTags.forEach((link) => {

                const href = link.href;

                if (href) {
                    links.push(href);
                }
            });
        }

        return {
            sender,
            subject,
            body,
            links
        };

    } catch (error) {

        console.error(
            "MailShield extraction error:",
            error
        );

        return null;
    }
}

chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {

        if (
            request.action === "GET_EMAIL_DATA"
        ) {

            const emailData =
                extractEmailData();

            sendResponse(emailData);
        }

        return true;
    }
);