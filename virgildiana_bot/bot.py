import logging
import os
import textwrap
from telegram import Update, ParseMode
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackContext)
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Steps definition with detailed questions
STEPS = [
    {
        "name": "Name the Idea",
        "questions": [
            "What is the idea?",
            "What problem is it solving?",
            "What desire is it meeting?",
            "Does this project represent the way you naturally organise things before you learned too much?"
        ]
    },
    {
        "name": "Frame",
        "questions": [
            "How long do you want to take to build it?",
            "Apply Parkinson’s Law and set a strict one-week deadline.",
            "What is the simplest version that can exist in that time?"
        ]
    },
    {
        "name": "5Ws and a H",
        "questions": [
            "What?",
            "Where?",
            "Why?",
            "Who?",
            "When?",
            "How?",
            "Also ask for a simple “three-frame cartoon” story from a single user’s point of view."
        ]
    },
    {
        "name": "Learning Objectives & MVO",
        "questions": [
            "What economically valuable skills are being learned?",
            "What is the Minimum Viable Offer?",
            "What is the smallest bundle of benefits that proves the concept?"
        ]
    },
    {
        "name": "Evaluate — The 3% Rule",
        "questions": [
            "What existing thing is being adjusted by 3%?",
            "What materials or systems will be used?",
            "What readymade form is being edited?",
            "What precedents or existing products are being used as a platform?"
        ]
    },
    {
        "name": "Near Rocks & Power Laws",
        "questions": [
            "What near rocks could kill the project?",
            "What urgent and important tasks must not fail?",
            "What 20% will drive 80% of the performance?"
        ]
    },
    {
        "name": "OU Design Limits",
        "questions": [
            "Conditions",
            "Constraints",
            "Considerations"
        ]
    }
]

# Telegram conversation states for each step's question index
(STEP, QUESTION) = range(2)

# Session data key prefixes
SESSION_STEP = 'step'
SESSION_QUESTION = 'question'
SESSION_ANSWERS_PREFIX = 'answers'

# Report file max lines threshold
MAX_REPORT_LINES = 70


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the V.I.R.G.I.L / D.I.A.N.A_002 idea development workflow bot."
        "\nUse /virgildiana to start the idea workflow."
    )


def start_virgildiana(update: Update, context: CallbackContext):
    context.user_data.clear()
    context.user_data[SESSION_STEP] = 0
    context.user_data[SESSION_QUESTION] = 0
    context.user_data[SESSION_ANSWERS_PREFIX] = [[] for _ in STEPS]

    step_name = STEPS[0]["name"]
    first_question = STEPS[0]["questions"][0]
    update.message.reply_text(f"Step 1: {step_name}\nQuestion 1: {first_question}")
    return (0, 0)


def handle_message(update: Update, context: CallbackContext):
    step = context.user_data.get(SESSION_STEP)
    question = context.user_data.get(SESSION_QUESTION)
    answers = context.user_data.get(SESSION_ANSWERS_PREFIX)

    if step is None or question is None or answers is None:
        update.message.reply_text(
            "Session expired or not started. Use /virgildiana to start a new session."
        )
        return ConversationHandler.END

    # Save current answer
    answers[step].append(update.message.text.strip())
    context.user_data[SESSION_ANSWERS_PREFIX] = answers

    question += 1

    # Check if questions remain in this step
    if question < len(STEPS[step]["questions"]):
        context.user_data[SESSION_QUESTION] = question
        update.message.reply_text(f"Question {question + 1}: {STEPS[step]['questions'][question]}")
        return (step, question)

    # Step complete, move to next step
    step += 1
    if step >= len(STEPS):
        update.message.reply_text(
            "\nAll steps complete! Use /virgildiana_report to generate the final report."
        )
        return ConversationHandler.END

    context.user_data[SESSION_STEP] = step
    context.user_data[SESSION_QUESTION] = 0
    next_step_name = STEPS[step]["name"]
    next_question = STEPS[step]["questions"][0]
    update.message.reply_text(f"Step {step + 1}: {next_step_name}\nQuestion 1: {next_question}")
    return (step, 0)


def virgildiana_report(update: Update, context: CallbackContext):
    answers = context.user_data.get(SESSION_ANSWERS_PREFIX, [])

    if not answers or len(answers) < len(STEPS):
        update.message.reply_text(
            "Workflow not complete yet. Use /virgildiana to start or continue the workflow."
        )
        return

    report_lines = []
    for i, step in enumerate(STEPS):
        report_lines.append(f"<b>Step {i + 1}: {step['name']}</b>")
        for question, answer in zip(step['questions'], answers[i]):
            report_lines.append(f"<b>{question}</b>\n{answer}")
        report_lines.append("")

    report_text = "\n".join(report_lines)

    # If too long, save to file and send path instead
    if len(report_lines) > MAX_REPORT_LINES:
        filename = f"virgildiana_report_{update.effective_chat.id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_text)
        update.message.reply_text(
            f"Report too long to display here, saved as file: {filename}"
        )
        with open(filename, "rb") as f:
            update.message.reply_document(f)
        return

    update.message.reply_text(report_text, parse_mode=ParseMode.HTML)


def virgildiana_restart(update: Update, context: CallbackContext):
    context.user_data.clear()
    update.message.reply_text("Workflow restarted. Use /virgildiana to start again.")


def virgildiana_cancel(update: Update, context: CallbackContext):
    context.user_data.clear()
    update.message.reply_text("Workflow cancelled.")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("virgildiana", start_virgildiana)],
        states={
            STEP: [MessageHandler(Filters.text & ~Filters.command, handle_message)],
        },
        fallbacks=[
            CommandHandler("virgildiana_cancel", virgildiana_cancel),
            CommandHandler("virgildiana_restart", virgildiana_restart),
        ],
        allow_reentry=True,
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("virgildiana_report", virgildiana_report))
    dispatcher.add_handler(CommandHandler("virgildiana_restart", virgildiana_restart))
    dispatcher.add_handler(CommandHandler("virgildiana_cancel", virgildiana_cancel))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
