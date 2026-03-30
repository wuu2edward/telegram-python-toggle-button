"""
V.I.R.G.I.L / D.I.A.N.A_002 Telegram Workflow Mini-App

Guides user through 7-step idea development process.

Commands:
 - /virgil: start workflow
 - /virgil_report: show current report
 - /virgil_restart: restart workflow
 - /virgil_cancel: cancel workflow

Designed for safe integration into existing OpenClaw Telegram bot command handlers.
"""

import json

# Session state storage (in-memory)
_sessions = {}

# Workflow steps definition
_STEPS = [
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


class VirgilDiana002:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = _sessions.get(user_id, {
            "step_index": 0,
            "answers": [[] for _ in _STEPS],
            "cancelled": False
        })

    def save_state(self):
        _sessions[self.user_id] = self.state

    def current_step(self):
        return _STEPS[self.state["step_index"]]

    def is_complete(self):
        return self.state["step_index"] >= len(_STEPS)

    def reset(self):
        self.state = {
            "step_index": 0,
            "answers": [[] for _ in _STEPS],
            "cancelled": False
        }
        self.save_state()

    def cancel(self):
        self.state["cancelled"] = True
        self.save_state()

    def handle_text(self, text):
        if self.state["cancelled"]:
            return "Workflow is cancelled. Use /virgil to start again."

        if self.is_complete():
            return "Workflow complete. Use /virgil_report to see the report or /virgil_restart to start a new session."

        # Add the text answer to current step answers
        current_index = self.state["step_index"]
        self.state["answers"][current_index].append(text.strip())
        self.save_state()

        # Check if all questions in current step are answered
        if len(self.state["answers"][current_index]) >= len(_STEPS[current_index]["questions"]):
            self.state["step_index"] += 1
            self.save_state()
            if self.is_complete():
                return "All steps complete! Use /virgil_report to see your final report."
            return f"Step {self.state['step_index']} complete. Next step: {self.current_step()['name']}\n" + self.get_current_step_questions()
        else:
            return self.get_next_question()

    def get_current_step_questions(self):
        idx = self.state["step_index"]
        return "\n".join([f"{i+1}. {q}" for i, q in enumerate(_STEPS[idx]["questions"])] )

    def get_next_question(self):
        idx = self.state["step_index"]
        ans_len = len(self.state["answers"][idx])
        return f"Question {ans_len+1}: {_STEPS[idx]['questions'][ans_len]}"

    def generate_report(self):
        if not self.is_complete():
            return "Workflow not complete yet. Use /virgil to continue."

        parts = [f"<b>{_STEPS[i]['name']}</b>:<br>" + "<br>".join(ans) for i, ans in enumerate(self.state["answers"]) ]
        report_html = "<br><br>".join(parts)
        return report_html


# Integration hooks for OpenClaw command handling

# Simple in-memory user session handlers
_workflows = {}

def start_virgil_session(user_id):
    w = VirgilDiana002(user_id)
    w.reset()
    _workflows[user_id] = w
    first_step = w.current_step()
    return f"Started V.I.R.G.I.L workflow! First step: {first_step['name']}\n" + w.get_current_step_questions()

def handle_virgil_text(user_id, text):
    if user_id not in _workflows:
        _workflows[user_id] = VirgilDiana002(user_id)
    w = _workflows[user_id]
    return w.handle_text(text)

def show_virgil_report(user_id):
    if user_id not in _workflows:
        return "No active V.I.R.G.I.L session. Use /virgil to start."
    w = _workflows[user_id]
    return w.generate_report()

def restart_virgil_session(user_id):
    w = VirgilDiana002(user_id)
    w.reset()
    _workflows[user_id] = w
    return "V.I.R.G.I.L workflow restarted. Use /virgil to start again."

def cancel_virgil_session(user_id):
    if user_id not in _workflows:
        return "No active V.I.R.G.I.L session to cancel."
    w = _workflows[user_id]
    w.cancel()
    return "V.I.R.G.I.L workflow cancelled. Use /virgil to start a new session."

# Note: Registration with OpenClaw Telegram commands will be handled separately.
