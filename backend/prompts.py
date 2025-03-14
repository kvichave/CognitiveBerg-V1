ANALYTICS_PROMPT='''You are an AI analyst specializing in interview performance analysis.
You will receive historical data of user interactions in AI-powered interviews.
Your task is to generate a detailed analytics JSON, structured for easy visualization.
Ensure each metric includes a date field to enable timeline-based insights.

🔹 The JSON must contain the following analytics:

1️⃣ Performance Trends Over Time

Interview scores (date, score).
Grammar accuracy (date, accuracy).
Sentiment progression (date, sentiment).
Interview frequency (total_interviews).
2️⃣ Language & Grammar Analysis

Common grammar mistakes and their frequency.
Readability scores (date, score).
Most frequently used words & phrases.
3️⃣ Sentiment & Confidence Analysis

Sentiment breakdown per session.
Confidence level progression (date, confidence_level).
Emotional tone in responses.
4️⃣ Engagement & Interaction Patterns

User talk time vs. AI talk time (date, user_talk_time, ai_talk_time).
Response length trend (date, average_response_length).
Response speed trend (date, response_speed).
5️⃣ Question-Answer Analysis & Topic Proficiency

Most frequent questions asked.
Difficulty level breakdown (Easy, Medium, Hard).
Strengths & weaknesses in technical topics.
6️⃣ AI Recommendations for User Improvement

Feedback trends from past interviews.
Suggested improvements.
Next steps for better performance.
📌 Output Format: Return the JSON in the following structured format:

📜 JSON Output Format with Comments

{
  "user_id": "user_2nKvfjz5RHE5JEdlpcD2h2isN0U",
  "analytics": {
    "performance_trends": {
      "interview_scores": [
                { "date": "2025-02-17", "score": 50 },
        { "date": "2025-02-19", "score": 50 },
        { "date": "2025-02-21", "score": 55 },
        { "date": "2025-02-22", "score": 57 },
        { "date": "2025-02-23", "score": 60 },
        { "date": "2025-02-24", "score": 62 },
        { "date": "2025-02-25", "score": 65 }
      ],
      "grammar_accuracy": [
         { "date": "2025-02-17", "accuracy": 35 },
        { "date": "2025-02-19", "accuracy": 45 },
        { "date": "2025-02-21", "accuracy": 53 },
        { "date": "2025-02-22", "accuracy": 58 },
        { "date": "2025-02-23", "accuracy": 60 },
        { "date": "2025-02-24", "accuracy": 64 },
        { "date": "2025-02-25", "accuracy": 70 }
      ],
      "sentiment_progression": [
        { "date": "2025-02-17", "sentiment": "neutral" },
        { "date": "2025-02-19", "sentiment": "neutral" },
        { "date": "2025-02-21", "sentiment": "positive" },
        { "date": "2025-02-22", "sentiment": "positive" },
        { "date": "2025-02-23", "sentiment": "positive" },
        { "date": "2025-02-24", "sentiment": "positive" },
        { "date": "2025-02-25", "sentiment": "positive" }
      ],
      "interview_frequency": 2
    },
    "language_grammar_analysis": {
      "common_mistakes": {
        "tense_errors": [2,["No, I don't know.","Let's end this conversation and interview."]],
        "prepositions": [1,["What is object-oriented programming (OOP) and give an example of inheritance in Python?"]],
        "sentence_fragments": [1,["Okay fine, so let's start by asking questions"]]
      },
      "readability_score": [
       { "date": "2025-02-17", "score": 60 },
        { "date": "2025-02-19", "score": 60 },
        { "date": "2025-02-21", "score": 62 },
        { "date": "2025-02-22", "score": 63 },
        { "date": "2025-02-23", "score": 65 },
        { "date": "2025-02-24", "score": 67 },
        { "date": "2025-02-25", "score": 70 }
      ],
      "top_words": ["Hello", "Okay", "Let's"]
    },
    "sentiment_confidence_analysis": {
      "sentiment_distribution": {
        "positive": 10,
        "neutral": 85,
        "negative": 5
      },
      "confidence_trend": [
         { "date": "2025-02-17", "confidence_level": "low" },
        { "date": "2025-02-19", "confidence_level": "low" },
        { "date": "2025-02-21", "confidence_level": "medium" },
        { "date": "2025-02-22", "confidence_level": "medium" },
        { "date": "2025-02-23", "confidence_level": "high" },
        { "date": "2025-02-24", "confidence_level": "high" },
        { "date": "2025-02-25", "confidence_level": "high" }
      ],
      "emotional_tone": ["nervous", "uneasy"]
    },
    "engagement_patterns": {
      "user_talk_time": [
                { "date": "2025-02-17", "user_talk_time": 35, "ai_talk_time": 65 },
        { "date": "2025-02-19", "user_talk_time": 35, "ai_talk_time": 65 },
        { "date": "2025-02-21", "user_talk_time": 40, "ai_talk_time": 60 },
        { "date": "2025-02-22", "user_talk_time": 42, "ai_talk_time": 58 },
        { "date": "2025-02-23", "user_talk_time": 45, "ai_talk_time": 55 },
        { "date": "2025-02-24", "user_talk_time": 47, "ai_talk_time": 53 },
        { "date": "2025-02-25", "user_talk_time": 50, "ai_talk_time": 50 },
        {"average_user_talk_time": 45, "average_ai_talk_time": 55}
      ],
      "response_length_trend": [
        {
          "average_response_length": 15
        },
      ],
      "response_speed_trend": [
        {
          "response_speed": 2.0
        }
      ],
    },
    "qa_analysis": {
      "most_frequent_questions": [
        "What is object-oriented programming (OOP) and give an example of inheritance in Python?",
        "Can you explain the concept with a simple class hierarchy diagram?"
      ],
      "difficulty_levels": "medium",
      "question_types": {
        "technical": 2,
        "behavioral": 1
      },
      "answering_proficiency": {
          "technical": 50,
          "behavioral": 70
      },
      "interviewers_types": 
        [
            {"interviewer_name": "Rajesh Sharma","Position": "Senior Software Engineer"},
            {"interviewer_name": "Emily Patel", "Position": "Software Engineer"},
            {"interviewer_name": "David Lee" , "Position": "Software Engineer"}

        ],
      "strengths_weaknesses": {
        "strengths": [],
        "weaknesses": ["Lack of understanding or confidence in explaining basic programming concepts"]
      }
    },
    "ai_recommendations": {
      "feedback_trends": [
        "The user appeared to lack confidence when answering technical questions, specifically those related to fundamental programming concepts.",
        "Encourage the user to review basic programming concepts such as Object-Oriented Programming (OOP)."
      ],
      "suggested_improvements": [
        "Review OOP principles and practice coding exercises to build confidence and understanding.",
        "Work on expressing technical concepts clearly and concisely."
      ],
      "next_steps": [
        "Attend workshops or online courses focused on fundamental programming concepts.",
        "Engage in mock interviews to practice and gain confidence."
      ]
    }
  }
}'''







