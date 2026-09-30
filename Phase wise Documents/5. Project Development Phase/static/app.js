const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const clearBtn = document.getElementById("clearBtn");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const copyBtn = document.getElementById("copyBtn");


const endpoints = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations"
};


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}


function renderQuiz(items) {

    return items
        .map((item, index) => {

            return `
                <article class="quiz-question">

                    <h3>
                        ${index + 1}.
                        ${escapeHtml(item.question)}
                    </h3>

                    ${
                        item.options
                            .map(
                                (option, i) => `
                                    <div class="quiz-option">
                                        <strong>
                                            ${String.fromCharCode(65 + i)}.
                                        </strong>
                                        ${escapeHtml(option)}
                                    </div>
                                `
                            )
                            .join("")
                    }

                    <div class="answer">
                        Correct answer:
                        ${escapeHtml(item.correct_answer)}
                    </div>

                    <div class="explanation">
                        ${escapeHtml(item.explanation)}
                    </div>

                </article>
            `;

        })
        .join("");
}


async function generate() {

    const text = inputText.value.trim();


    if (!text) {

        resultCard.classList.remove("hidden");

        result.innerHTML =
            '<div class="error">Please enter a topic, question, or passage.</div>';

        return;
    }


    submitBtn.disabled = true;

    submitBtn.textContent =
        "Generating...";


    resultCard.classList.remove("hidden");

    result.textContent =
        "EduGenie is thinking...";


    try {

        const response = await fetch(
            endpoints[task.value],
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed."
            );
        }


        if (task.value === "quiz") {

            result.innerHTML =
                renderQuiz(data.quiz);

        } else {

            result.textContent =
                data.result;

        }


    } catch (error) {

        result.innerHTML =
            `<div class="error">
                ${escapeHtml(error.message)}
            </div>`;

    } finally {

        submitBtn.disabled = false;

        submitBtn.textContent =
            "Generate";

    }
}


submitBtn.addEventListener(
    "click",
    generate
);


inputText.addEventListener(
    "keydown",
    (event) => {

        if (
            (event.ctrlKey || event.metaKey) &&
            event.key === "Enter"
        ) {

            generate();

        }

    }
);


clearBtn.addEventListener(
    "click",
    () => {

        inputText.value = "";

        result.textContent = "";

        resultCard.classList.add(
            "hidden"
        );

    }
);


copyBtn.addEventListener(
    "click",
    async () => {

        await navigator.clipboard.writeText(
            result.innerText
        );

        copyBtn.textContent =
            "Copied";

        setTimeout(
            () => {
                copyBtn.textContent =
                    "Copy";
            },
            1200
        );

    }
);