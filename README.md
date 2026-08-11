# The Interview Agent

> An AI-powered technical interview platform that evaluates a candidate's engineering knowledge, reasoning, and communication through an adaptive 8-question interview.

[![Live Frontend](https://img.shields.io/badge/Live%20Frontend-Vercel-black?logo=vercel)](https://the-interview-agent.vercel.app/)
[![Backend API](https://img.shields.io/badge/Backend-Render-46E3B7?logo=render)](https://the-interview-agent-1-d3h6.onrender.com/)
[![Framework](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react)](https://react.dev/)

---

## Overview

The Interview Agent is a full-stack AI interview system designed to simulate a structured technical interview.

Instead of presenting a fixed list of questions, the system uses the candidate's profile, curriculum information, previous questions, and submitted answers to drive the interview flow. After the interview, the system generates a structured evaluation covering:

- Technical depth
- Engineering reasoning
- Communication
- Strengths
- Areas for improvement
- Recommended learning topics
- Overall interviewer feedback

The application is split into a React/Vite frontend and a FastAPI backend, with Groq used as the LLM provider.

---

## Why We Built It

Traditional technical interviews can be difficult to standardize. Different interviewers may ask different questions, provide inconsistent feedback, or spend limited time evaluating a candidate's reasoning.

The Interview Agent aims to make the process:

**Structured** → Every candidate follows a consistent interview framework.

**Adaptive** → Questions are generated using candidate context and interview history.

**Evaluative** → The final response includes multiple evaluation dimensions rather than a single score.

**Actionable** → Candidates receive strengths, improvement areas, and recommended topics.

---

## Core Workflow

```text
                    ┌──────────────────────┐
                    │      Candidate       │
                    │      enters ID       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Candidate Service    │
                    │ Load candidate data  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Candidate Analyzer   │
                    │ Build candidate      │
                    │ understanding        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Interview Agent      │
                    │ Generate Question    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Candidate Answer     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Interview History    │
                    │ Question + Answer    │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
               Questions 1-7          Question 8
                    │                      │
                    ▼                      ▼
             Generate next          Generate final
               question               feedback
                                           │
                                           ▼
                              ┌──────────────────────┐
                              │ Interview Evaluation │
                              │ Technical            │
                              │ Reasoning            │
                              │ Communication        │
                              │ Strengths            │
                              │ Improvements         │
                              │ Recommended Topics   │
                              └──────────────────────┘
```

---

## Key Features

### Candidate-Aware Interviewing

The system first loads the candidate profile and analyzes available candidate information before starting the interview.

### AI-Generated Technical Questions

Questions are generated dynamically instead of relying only on a hard-coded question list.

The question generation process considers:

- Candidate information
- Curriculum
- Candidate analysis
- Previous interview questions
- Previous answers
- Current question number

### Structured 8-Question Interview

The current interview consists of eight questions.

The system maintains interview state throughout the session and records each question and answer.

### AI-Based Final Evaluation

After the eighth answer, the system generates a final evaluation containing:

- Overall score
- Technical score
- Reasoning score
- Communication score
- Strengths
- Areas to improve
- Recommended topics
- Final interviewer feedback

### Candidate Progress Interface

The frontend displays:

- Current question number
- Interview progress
- Question difficulty
- Curriculum day/topic
- Candidate information
- Interview signals
- Answer submission interface

### Production Deployment

The application is deployed as two services:

```text
React + Vite
     │
     │ HTTPS
     ▼
Vercel
     │
     │ REST API
     ▼
FastAPI
     │
     ▼
Render
     │
     ▼
Groq LLM
```

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS
- Lucide React

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- python-dotenv

### AI Layer

- Groq API
- OpenAI-compatible Python SDK
- Prompt-based candidate analysis
- Prompt-based question generation
- Prompt-based interview evaluation

### Deployment

- Vercel — frontend
- Render — backend
- GitHub — source control

---

## Project Structure

```text
The-Interview-Agent/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── candidate_analyzer.py
│   │   └── interview_agent.py
│   │
│   ├── api/
│   │
│   ├── data/
│   │
│   ├── models/
│   │
│   ├── prompts/
│   │
│   ├── services/
│   │   ├── candidate_service.py
│   │   ├── curriculum_service.py
│   │   └── interview_service.py
│   │
│   ├── tests/
│   ├── utils/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Backend Architecture

The backend is organized around separate responsibilities.

### `candidate_service`

Responsible for retrieving candidate information.

### `curriculum_service`

Provides curriculum days and topics used during question generation.

### `candidate_analyzer`

Analyzes candidate information using the LLM and produces structured candidate context for the interview.

### `interview_agent`

Handles the AI intelligence of the interview:

- Question generation
- Interview evaluation
- Feedback generation
- Handling model responses and API errors

### `interview_service`

Maintains interview sessions and their state, including:

- Session ID
- Candidate ID
- Candidate data
- Candidate analysis
- Question number
- Interview history
- Completion status
- Final feedback

### `main.py`

Exposes the FastAPI application and REST endpoints that connect the frontend to the backend.

---

## Interview Lifecycle

### 1. Candidate Loading

The frontend sends:

```http
GET /candidates/{candidate_id}
```

The backend retrieves the candidate profile.

### 2. Interview Initialization

The frontend sends:

```http
POST /interview/start/{candidate_id}
```

The backend:

1. Loads the candidate.
2. Analyzes the candidate.
3. Creates an interview session.
4. Loads the curriculum.
5. Generates the first question.
6. Stores the question in interview history.

### 3. Answer Submission

The frontend sends:

```http
POST /interview/{session_id}/answer
```

with:

```json
{
  "answer": "Candidate's response..."
}
```

The backend stores the answer and determines whether another question should be generated.

### 4. Next Question

For questions 1–7, the AI generates the next question using the accumulated interview context.

### 5. Final Evaluation

After question 8 is answered, the backend generates the final evaluation instead of another question.

---

## API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| GET | `/candidates` | Get all candidates |
| GET | `/candidates/{candidate_id}` | Get a specific candidate |
| POST | `/candidates/{candidate_id}/analyze` | Analyze a candidate |
| GET | `/curriculum` | Get curriculum |
| GET | `/curriculum/day/{day_number}` | Get a curriculum day |
| POST | `/interview/start/{candidate_id}` | Start an interview |
| POST | `/interview/{session_id}/answer` | Submit an answer |
| GET | `/interview/{session_id}` | Get interview status |

---

## Local Development

### Prerequisites

Install:

- Python 3.10+
- Node.js
- npm
- Git

### Clone the repository

```bash
git clone https://github.com/Udaysri2025/The-Interview-Agent.git
cd The-Interview-Agent
```

---

### Backend Setup

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
backend/.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key
```

Start the backend:

```bash
uvicorn main:app --reload
```

Backend will run locally on:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

### Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server will provide the frontend URL shown in the terminal.

The frontend communicates with the deployed backend through the API URL configured in `src/App.jsx`.

---

## Environment Variables

The Groq API key is required only by the backend.

```env
GROQ_API_KEY=your_groq_api_key
```

### Security

Never commit:

```text
backend/.env
```

Never place the real API key inside:

- `App.jsx`
- GitHub
- README files
- frontend environment variables
- screenshots

The repository contains only the example configuration:

```env
GROQ_API_KEY=
```

---

## Live Deployment

### Frontend

The React/Vite application is deployed on Vercel.

Live application:

https://the-interview-agent-seven.vercel.app/

### Backend

The FastAPI service is deployed on Render.

Backend:

https://the-interview-agent-1-d3h6.onrender.com/

Health check:

https://the-interview-agent-1-d3h6.onrender.com/health

API documentation:

https://the-interview-agent-1-d3h6.onrender.com/docs

---

## Example Interview Result

The final evaluation provides a structured result similar to:

```text
Interview Complete!

Overall Score: 60/100

Technical:       55/100
Reasoning:       50/100
Communication:   65/100

Strengths:
- Understanding of embeddings
- Awareness of vector databases
- Ability to discuss engineering trade-offs

Areas to Improve:
- Technical depth
- Reasoning structure
- Detailed implementation explanation

Recommended Topics:
- Advanced retrieval techniques
- Embedding optimization
- RAG evaluation
```

The actual evaluation is generated dynamically from the candidate's interview responses.

---

## Engineering Design Decisions

### Why FastAPI?

FastAPI provides:

- Lightweight REST API development
- Automatic API documentation
- Pydantic-based validation
- Easy integration with Python AI tooling
- Straightforward deployment with Uvicorn

### Why React + Vite?

The interview interface requires frequent state updates for:

- Current questions
- Answers
- Loading states
- Interview progress
- Final evaluation

React provides a clean component-based approach while Vite keeps frontend development and builds fast.

### Why an OpenAI-Compatible Client?

The backend uses the OpenAI Python SDK interface while configuring the Groq-compatible API endpoint. This provides a familiar client interface while using Groq's inference infrastructure.

### Why Separate Frontend and Backend?

Separating the frontend and backend allows:

- Independent deployment
- Better security for API credentials
- Clear API boundaries
- Easier maintenance
- Independent scaling

---

## Current Limitations

The current implementation is intentionally focused on the core interview experience.

Potential future improvements include:

- Persistent database-backed interview sessions
- Authentication and user accounts
- Interview history dashboard
- More sophisticated adaptive difficulty
- Voice-based interviewing
- Speech-to-text answers
- Real-time interviewer interaction
- Detailed per-question scoring
- Analytics dashboard
- Multiple interview modes
- Resume-based question generation
- Automated evaluation benchmarking

---

## Future Vision

The long-term goal is to evolve The Interview Agent from a technical interview simulator into a complete AI-powered interview and learning platform.

The system could eventually connect:

```text
Candidate Profile
       +
Resume / Projects
       +
Learning History
       +
Interview Performance
       ↓
Adaptive Interview Engine
       ↓
Personalized Evaluation
       ↓
Personalized Learning Roadmap
```

This would allow the platform not only to evaluate candidates, but also to identify knowledge gaps and guide them toward targeted improvement.

---

# Team

## Kojinkia Innovation

### Uday Sri Yaramati
**Team Lead & AI/Full-Stack Developer**

Responsible for overall system architecture, AI interview workflow, backend/frontend integration, deployment, and project coordination.

### K Hemasree Krishna
**AI Developer**

Responsible for AI-focused components, candidate analysis and evaluation logic, prompt design, model interaction, and improving the quality of generated interview content.

### Hitesh Laahiri Kodamala
**Full-Stack Developer**

Responsible for frontend experience, API integration, interview interaction flow, UI implementation, testing, and supporting backend integration.


---

## Repository

Source code:

https://github.com/Udaysri2025/The-Interview-Agent

---

## Team

**Uday Sri Yaramati · K Hemasree Krishna · Hitesh Laahiri Kodamala**

**Amrita Vishwa Vidyapeetham University**

---

## License

This project is developed as an academic/engineering project by the team above.

Copyright © 2026 The Interview Agent Team.
