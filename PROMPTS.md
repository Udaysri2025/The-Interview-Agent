# AI Development Log - The Interview Agent

## About This File

This file documents how AI-assisted development was used while building
The Interview Agent.

We used AI as a development partner for brainstorming, implementation,
debugging, refinement, and documentation. The team made the project
decisions, reviewed the generated code, tested the application, and
iterated on the implementation.

---

## Project

**Project:** The Interview Agent

**Repository:** https://github.com/Udaysri2025/The-Interview-Agent

**Live Application:** https://the-interview-agent-seven.vercel.app/

**Team:** Kojinkia Innovation

---

# How We Built It

The project followed an iterative vibe-coding workflow:

1. We defined the feature or problem we wanted to solve.
2. We discussed the implementation approach with AI.
3. AI helped us generate or modify parts of the implementation.
4. We tested the changes locally.
5. We identified errors or improvements.
6. We used AI to help debug and refine the implementation.
7. We reviewed the resulting code and integrated the changes.
8. We committed the working changes to GitHub.
9. We deployed the application and tested the live version.
10. We continued iterating until the feature worked as expected.

AI was therefore used throughout the development loop rather than only for
generating isolated pieces of code.

---

# What We Used AI For

## Project Planning

AI helped us think through:

- Application architecture
- Backend and frontend separation
- API structure
- Interview workflow
- Candidate analysis workflow
- AI agent responsibilities
- Deployment approach

The final architecture and feature decisions were made by the team.

---

## Backend Development

AI assisted with implementing and refining the FastAPI backend.

The backend includes functionality for:

- Health checks
- Candidate information
- Candidate analysis
- Curriculum information
- Interview session creation
- Interview question generation
- Answer submission
- Interview progress tracking
- Final interview feedback

We tested the API endpoints and fixed implementation issues during
development.

---

## AI Interview System

AI assistance was used to develop the interview agent responsible for:

- Generating interview questions
- Using candidate information
- Considering previous answers
- Continuing the interview dynamically
- Generating final interview feedback

The interview flow was designed and refined by the team.

---

## Candidate Analysis

AI helped us implement the candidate analysis workflow.

Candidate information is analyzed before the interview so that the
interview experience can be more relevant to the candidate.

---

## Frontend Development

AI was used as a coding partner while developing the frontend.

It helped with:

- React components
- Interview screens
- API integration
- State handling
- User interaction
- UI refinements
- Connecting the frontend to the deployed backend

The frontend was tested against the live backend before deployment.

---

## API Integration

The project uses a Groq-powered AI backend through an
OpenAI-compatible API interface.

AI helped us configure the integration and troubleshoot API-related issues.

API credentials are stored using environment variables and are not included
in the public repository.

---

# Debugging and Iteration

A major part of the development process involved debugging real issues.

For example, during deployment we encountered an incorrect Render build
command caused by the root-directory configuration.

The deployment initially failed with:

    bash: line 1: backend/: Is a directory

We investigated the issue, corrected the Render configuration, and
successfully deployed the backend.

The final backend deployment was verified through the health endpoint and
live API requests.

---

# Deployment

The project uses separate deployments for the frontend and backend.

## Backend

The FastAPI backend was deployed as a web service.

Build command:

    pip install -r requirements.txt

Start command:

    uvicorn main:app --host 0.0.0.0 --port $PORT

The deployed backend was tested after deployment.

## Frontend

The React/Vite frontend was deployed separately and configured to communicate
with the live backend API.

---

# Vibe-Coding Workflow

The development process was conversational and iterative.

Typical development cycle:

    Idea
      ↓
    Discuss with AI
      ↓
    Generate / modify implementation
      ↓
    Run and test
      ↓
    Find an issue
      ↓
    Debug with AI
      ↓
    Review changes
      ↓
    Test again
      ↓
    Commit to GitHub
      ↓
    Deploy
      ↓
    Validate

This allowed us to move quickly while still testing and reviewing the
implementation at every important stage.

---

# Examples of AI-Assisted Tasks

Some examples of tasks where AI acted as our coding partner:

- Designing the initial project structure
- Creating FastAPI routes
- Implementing interview session handling
- Building candidate analysis logic
- Developing question generation logic
- Developing feedback generation logic
- Connecting frontend API calls
- Debugging environment variable configuration
- Troubleshooting deployment errors
- Fixing frontend/backend connectivity
- Preparing deployment commands
- Improving project documentation

---

# Human Contribution

AI assistance was part of our development workflow, but the project was
actively directed and validated by the team.

We were responsible for:

- Defining the project idea
- Choosing the features
- Making architecture decisions
- Deciding what to implement
- Reviewing generated code
- Testing the application
- Identifying bugs
- Validating AI-generated changes
- Managing GitHub
- Deploying the application
- Checking the final live system

AI helped us accelerate implementation and problem-solving, while the team
remained responsible for the final product.

---

# Team

## Uday Sri Yaramati
**Role:** Project Lead & AI/Backend Developer

Worked on:

- Project architecture
- AI interview system
- Backend development
- API integration
- AI integration
- Deployment
- Overall project coordination

## K Hemasree Krishna
**Role:** Frontend & UI Developer

Worked on:

- Frontend development
- Interview interface
- User interaction flow
- Frontend/backend integration
- UI improvements

## Hitesh Laahiri Kodamala
**Role:** AI/Backend & Testing Developer

Worked on:

- AI/backend implementation
- Testing
- Debugging
- Feature validation
- Integration support

**Institution:** Amrita Vishwa Vidyapeetham University

---

# Final Note

This project demonstrates a practical AI-assisted development workflow.

Instead of treating AI as a one-time code generator, we used it as a
development partner throughout the build-test-debug-refine cycle.

The final application was reviewed, tested, integrated, and deployed by the
team.
