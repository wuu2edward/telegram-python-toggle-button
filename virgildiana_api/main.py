from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Workflow questions and steps
STEPS = [
    [
        "What is the idea?",
        "What problem is it solving?",
        "What desire is it meeting?",
        "Does this project represent the way you naturally organise things before you learned too much?"
    ],
    [
        "How long do you want to take to build it?",
        "Apply Parkinson’s Law and set a strict one-week deadline.",
        "What is the simplest version that can exist in that time?"
    ],
    [
        "What?",
        "Where?",
        "Why?",
        "Who?",
        "When?",
        "How?",
        "Also ask for a simple 'three-frame cartoon' story from a single user’s point of view."
    ],
    [
        "What economically valuable skills are being learned?",
        "What is the Minimum Viable Offer?",
        "What is the smallest bundle of benefits that proves the concept?"
    ],
    [
        "What existing thing is being adjusted by 3%?",
        "What materials or systems will be used?",
        "What readymade form is being edited?",
        "What precedents or existing products are being used as a platform?"
    ],
    [
        "What near rocks could kill the project?",
        "What urgent and important tasks must not fail?",
        "What 20% will drive 80% of the performance?"
    ],
    [
        "Conditions",
        "Constraints",
        "Considerations"
    ]
]

sessions = {}

class StartRequest(BaseModel):
    session_id: str

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

class ReportResponse(BaseModel):
    report: str

@app.post('/start')
def start(req: StartRequest):
    sessions[req.session_id] = {
        'step': 0,
        'question': 0,
        'answers': [[] for _ in STEPS],
        'cancelled': False
    }
    first_question = STEPS[0][0]
    return {'message': f'Workflow started. Step 1: Name the Idea\nQuestion 1: {first_question}'}

@app.post('/answer')
def answer(req: AnswerRequest):
    if req.session_id not in sessions or sessions[req.session_id]['cancelled']:
        raise HTTPException(status_code=404, detail='Session not found or cancelled')
    session = sessions[req.session_id]
    step = session['step']
    question = session['question']
    session['answers'][step].append(req.answer)
    session['question'] += 1
    if session['question'] >= len(STEPS[step]):
        session['step'] += 1
        session['question'] = 0
        if session['step'] >= len(STEPS):
            return {'message': 'All steps complete! Use /report to get final report.'}
        else:
            next_question = STEPS[session['step']][session['question']]
            return {'message': f'Step {session["step"] + 1} started.\nQuestion 1: {next_question}'}
    else:
        next_question = STEPS[session['step']][session['question']]
        return {'message': f'Question {session["question"] + 1}: {next_question}'}

@app.post('/report', response_model=ReportResponse)
def report(req: StartRequest):
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail='Session not found')
    session = sessions[req.session_id]
    if session['step'] < len(STEPS):
        return {'report': 'Workflow not complete yet. Please finish all steps.'}
    parts = []
    for i, step in enumerate(STEPS):
        parts.append(f'<b>Step {i + 1}:</b>')
        for q, a in zip(step, session['answers'][i]):
            parts.append(f'<b>{q}</b><br>{a}<br>')
    report_html = '<br><br>'.join(parts)
    return {'report': report_html}

@app.post('/restart')
def restart(req: StartRequest):
    if req.session_id in sessions:
        del sessions[req.session_id]
    return {'message': 'Workflow restarted. Use /start to begin.'}

@app.post('/cancel')
def cancel(req: StartRequest):
    if req.session_id in sessions:
        sessions[req.session_id]['cancelled'] = True
    return {'message': 'Workflow cancelled.'}

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
