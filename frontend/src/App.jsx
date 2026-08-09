import { useState } from "react";

import {
  BrainCircuit,
  User,
  Sparkles,
  Send,
  CheckCircle2,
  Clock3,
  Target,
  MessageSquare,
  ChevronRight,
  Award,
  Code2,
  TrendingUp,
  AlertCircle,
  BookOpen
} from "lucide-react";

import "./App.css";


const API = "http://localhost:8000";


function App() {

  const [candidateId, setCandidateId] = useState("CAND-001");

  const [candidate, setCandidate] = useState(null);

  const [session, setSession] = useState(null);

  const [answer, setAnswer] = useState("");

  const [loading, setLoading] = useState(false);

  const [started, setStarted] = useState(false);

  const [error, setError] = useState("");


  // ==========================================================
  // LOAD CANDIDATE
  // ==========================================================

  const loadCandidate = async () => {

    try {

      setError("");

      const response = await fetch(
        `${API}/candidates/${candidateId}`
      );

      if (!response.ok) {
        throw new Error("Candidate not found");
      }

      const data = await response.json();

      setCandidate(data);

    } catch (err) {

      setError(err.message);
    }
  };


  // ==========================================================
  // START INTERVIEW
  // ==========================================================

  const startInterview = async () => {

    try {

      setLoading(true);
      setError("");

      const response = await fetch(
        `${API}/interview/start/${candidateId}`,
        {
          method: "POST"
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to start interview"
        );
      }

      setSession(data);

      setStarted(true);

      if (!candidate) {
        await loadCandidate();
      }

    } catch (err) {

      setError(err.message);

    } finally {

      setLoading(false);
    }
  };


  // ==========================================================
  // SUBMIT ANSWER
  // ==========================================================

  const submitAnswer = async () => {

    if (
      !answer.trim() ||
      !session?.session_id ||
      session?.completed
    ) {
      return;
    }

    try {

      setLoading(true);
      setError("");

      const response = await fetch(
        `${API}/interview/${session.session_id}/answer`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            answer: answer.trim()
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail || "Unable to submit answer"
        );
      }

      // ------------------------------------------------------
      // Store complete response
      // ------------------------------------------------------

      setSession(data);

      setAnswer("");

    } catch (err) {

      setError(err.message);

    } finally {

      setLoading(false);
    }
  };


  // ==========================================================
  // CURRENT QUESTION
  // ==========================================================

  const question = session?.question;


  // ==========================================================
  // FEEDBACK
  // ==========================================================

  const feedback = session?.feedback;


  // ==========================================================
  // RENDER
  // ==========================================================

  return (

    <div className="app">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="topbar">

        <div className="brand">

          <div className="brand-icon">
            <BrainCircuit size={34} />
          </div>

          <div>

            <h1>InterviewAI</h1>

            <span>
              AI Engineering Interview Agent
            </span>

          </div>

        </div>


        <div className="top-status">

          <span className="status-dot"></span>

          System Ready

        </div>

      </header>


      {/* =====================================================
          MAIN
      ===================================================== */}

      <main className="container">

        {/* ===================================================
            WELCOME
        =================================================== */}

        {!started ? (

          <section className="welcome">

            <div className="hero-icon">
              <Sparkles size={42} />
            </div>

            <p className="eyebrow">
              AI COHORT TECHNICAL INTERVIEW
            </p>

            <h2>

              Build confidence.
              <br />

              <span>
                Explain what you built.
              </span>

            </h2>

            <p className="hero-description">

              A personalized technical interview that adapts
              to your learning journey, challenges your
              reasoning, and gives actionable feedback.

            </p>


            {/* Candidate */}

            <div className="candidate-card">

              <div className="candidate-avatar">
                <User size={30} />
              </div>

              <div className="candidate-info">

                <label>
                  Candidate ID
                </label>

                <input
                  value={candidateId}
                  onChange={(e) =>
                    setCandidateId(e.target.value)
                  }
                  placeholder="CAND-001"
                />

              </div>

              <button
                className="secondary-btn"
                onClick={loadCandidate}
              >
                Load Candidate
              </button>

            </div>


            {/* Candidate Preview */}

            {candidate && (

              <div className="candidate-preview">

                <div>

                  <strong>

                    {candidate.member?.name ||
                      candidate.name ||
                      "Candidate"}

                  </strong>

                  <span>

                    {candidate.member?.jobRole ||
                      candidate.jobRole ||
                      "AI Engineer"}

                  </span>

                </div>


                <div className="preview-stat">

                  <Target size={18} />

                  <span>

                    {candidate.signals?.missionsCompleted ||
                      0}{" "}
                    missions

                  </span>

                </div>

              </div>

            )}


            {/* Error */}

            {error && (

              <div className="error">
                {error}
              </div>

            )}


            {/* Start */}

            <button
              className="primary-btn start-btn"
              onClick={startInterview}
              disabled={loading}
            >

              {loading
                ? "Preparing Interview..."
                : "Start Technical Interview"}

              <ChevronRight size={20} />

            </button>


            {/* Features */}

            <div className="interview-features">

              <div>

                <BrainCircuit size={20} />

                <span>
                  Adaptive Questions
                </span>

              </div>


              <div>

                <MessageSquare size={20} />

                <span>
                  Natural Follow-ups
                </span>

              </div>


              <div>

                <Award size={20} />

                <span>
                  Actionable Feedback
                </span>

              </div>

            </div>

          </section>

        ) : (

          /* =================================================
             INTERVIEW
          ================================================= */

          <section className="interview-layout">


            {/* =================================================
                SIDEBAR
            ================================================= */}

            <aside className="sidebar">

              <div className="profile">

                <div className="profile-avatar">
                  <User size={25} />
                </div>

                <div>

                  <strong>

                    {candidate?.member?.name ||
                      candidate?.name ||
                      "Candidate"}

                  </strong>

                  <span>

                    {candidate?.member?.jobRole ||
                      candidate?.jobRole ||
                      "AI Engineer"}

                  </span>

                </div>

              </div>


              {/* Progress */}

              <div className="progress-card">

                <div className="progress-heading">

                  <span>
                    Interview Progress
                  </span>

                  <strong>

                    {session?.question_number || 1}/8

                  </strong>

                </div>


                <div className="progress-bar">

                  <div

                    style={{
                      width: `${Math.min(
                        ((session?.question_number || 1) / 8) *
                          100,
                        100
                      )}%`
                    }}

                  ></div>

                </div>


                <p>

                  Minimum 8 questions across multiple
                  curriculum areas.

                </p>

              </div>


              {/* Signals */}

              <div className="sidebar-section">

                <span className="sidebar-label">
                  INTERVIEW SIGNALS
                </span>


                <div className="signal">

                  <Target size={17} />

                  <span>
                    Technical Depth
                  </span>

                </div>


                <div className="signal">

                  <Code2 size={17} />

                  <span>
                    Engineering Thinking
                  </span>

                </div>


                <div className="signal">

                  <MessageSquare size={17} />

                  <span>
                    Communication
                  </span>

                </div>

              </div>


              <div className="sidebar-bottom">

                <Clock3 size={17} />

                <span>
                  Take your time. Think clearly.
                </span>

              </div>

            </aside>


            {/* =================================================
                MAIN INTERVIEW AREA
            ================================================= */}

            <div className="interview-main">


              <div className="interview-header">

                <div>

                  <span className="eyebrow">
                    TECHNICAL INTERVIEW
                  </span>

                  <h2>
                    Let's explore your engineering thinking.
                  </h2>

                </div>


                <div className="live-badge">

                  <span></span>

                  LIVE

                </div>

              </div>


              {/* Error */}

              {error && (

                <div className="error">
                  {error}
                </div>

              )}


              {/* =================================================
                  QUESTION
              ================================================= */}

              {question && !session?.completed && (

                <div className="question-card">


                  <div className="question-meta">

                    <span className="question-number">

                      Question{" "}
                      {session?.question_number || 1}

                    </span>


                    <span className="difficulty">

                      {question.difficulty || "medium"}

                    </span>


                    <span className="topic">

                      Day {question.curriculum_day}{" "}
                      {question.topic}

                    </span>

                  </div>


                  <div className="question-body">

                    <div className="ai-icon">

                      <BrainCircuit size={23} />

                    </div>


                    <div>

                      <p className="question-label">
                        INTERVIEWER
                      </p>

                      <h3>
                        {question.question}
                      </h3>

                    </div>

                  </div>


                  <div className="answer-area">

                    <textarea

                      value={answer}

                      onChange={(e) =>
                        setAnswer(e.target.value)
                      }

                      onKeyDown={(e) => {

                        if (
                          e.key === "Enter" &&
                          e.ctrlKey
                        ) {

                          submitAnswer();

                        }

                      }}

                      placeholder="Explain your approach, reasoning, and engineering decisions..."

                    />


                    <div className="answer-footer">

                      <span>
                        Ctrl + Enter to submit
                      </span>


                      <button

                        className="primary-btn"

                        onClick={submitAnswer}

                        disabled={
                          loading ||
                          !answer.trim()
                        }

                      >

                        {loading
                          ? "Thinking..."
                          : "Submit Answer"}

                        <Send size={17} />

                      </button>

                    </div>

                  </div>

                </div>

              )}


              {/* =================================================
                  COMPLETED + FEEDBACK
              ================================================= */}

              {session?.completed && feedback && (

                <div className="feedback-container">


                  {/* Completion */}

                  <div className="completed-card">

                    <CheckCircle2 size={32} />

                    <div>

                      <h3>
                        Interview Complete!
                      </h3>

                      <p>
                        Your technical interview has been
                        evaluated successfully.
                      </p>

                    </div>

                  </div>


                  {/* Overall Score */}

                  <div className="feedback-score-card">

                    <div className="score-icon">
                      <TrendingUp size={28} />
                    </div>

                    <div>

                      <span className="feedback-label">
                        OVERALL SCORE
                      </span>

                      <div className="overall-score">

                        {feedback.overall_score}

                        <span>
                          /100
                        </span>

                      </div>

                    </div>

                  </div>


                  {/* Score Breakdown */}

                  <div className="score-grid">


                    <div className="score-box">

                      <span>
                        Technical
                      </span>

                      <strong>
                        {feedback.technical_score}
                      </strong>

                      <small>
                        /100
                      </small>

                    </div>


                    <div className="score-box">

                      <span>
                        Reasoning
                      </span>

                      <strong>
                        {feedback.reasoning_score}
                      </strong>

                      <small>
                        /100
                      </small>

                    </div>


                    <div className="score-box">

                      <span>
                        Communication
                      </span>

                      <strong>
                        {feedback.communication_score}
                      </strong>

                      <small>
                        /100
                      </small>

                    </div>

                  </div>


                  {/* Strengths */}

                  <div className="feedback-section">

                    <div className="feedback-section-title">

                      <CheckCircle2 size={21} />

                      <h3>
                        Strengths
                      </h3>

                    </div>


                    <div className="feedback-list">

                      {feedback.strengths?.map(
                        (item, index) => (

                          <div
                            className="feedback-item"
                            key={index}
                          >

                            <CheckCircle2 size={17} />

                            <span>
                              {item}
                            </span>

                          </div>

                        )
                      )}

                    </div>

                  </div>


                  {/* Weaknesses */}

                  <div className="feedback-section">

                    <div className="feedback-section-title">

                      <AlertCircle size={21} />

                      <h3>
                        Areas to Improve
                      </h3>

                    </div>


                    <div className="feedback-list">

                      {feedback.weaknesses?.map(
                        (item, index) => (

                          <div
                            className="feedback-item"
                            key={index}
                          >

                            <AlertCircle size={17} />

                            <span>
                              {item}
                            </span>

                          </div>

                        )
                      )}

                    </div>

                  </div>


                  {/* Recommended Topics */}

                  <div className="feedback-section">

                    <div className="feedback-section-title">

                      <BookOpen size={21} />

                      <h3>
                        Recommended Topics
                      </h3>

                    </div>


                    <div className="feedback-list">

                      {feedback.recommended_topics?.map(
                        (item, index) => (

                          <div
                            className="feedback-item"
                            key={index}
                          >

                            <BookOpen size={17} />

                            <span>
                              {item}
                            </span>

                          </div>

                        )
                      )}

                    </div>

                  </div>


                  {/* Final Feedback */}

                  <div className="final-feedback">

                    <div className="feedback-section-title">

                      <MessageSquare size={21} />

                      <h3>
                        Interviewer Feedback
                      </h3>

                    </div>

                    <p>
                      {feedback.final_feedback}
                    </p>

                  </div>


                </div>

              )}


              {/* =================================================
                  COMPLETED WITHOUT FEEDBACK
              ================================================= */}

              {session?.completed && !feedback && (

                <div className="completed-card">

                  <CheckCircle2 size={32} />

                  <div>

                    <h3>
                      Interview Complete!
                    </h3>

                    <p>
                      The interview is complete, but feedback
                      could not be loaded.
                    </p>

                  </div>

                </div>

              )}

            </div>

          </section>

        )}

      </main>

    </div>
  );
}


export default App;