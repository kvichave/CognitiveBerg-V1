"use client";

import { useState, useEffect } from "react";
import { Line, Bar, Pie } from "react-chartjs-2";
// import { Card, CardContent, CardTitle } from "@/components/ui/card";
import { bannercard } from "./components/card.jsx";
import CircularProgress from "./components/C_progress.jsx";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import Image from "next/image";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  ChartDataLabels
);

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/api/dashboard_data_fetch`, {
      method: "GET",
      credentials: "include", // Ensures cookies are sent
    })
      .then((response) => response.json())
      .then((data) => {
        setAnalytics(data.analytics.analytics);
        // console.log("ANALATICS :: ", data.analytics.analytics);
        // console.log("main ANALATICS :: ", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    // fetch("http://localhost:5000/api/dashboard_data_fetch") // Replace with actual backend API
    //   .then((res) => res.json())
    //   .then((data) => setAnalytics(data.analytics));
  }, []);

  if (!analytics)
    return <div className="text-white text-center">Loading...</div>;
  const proficiencyArray = Object.entries(
    analytics.qa_analysis.answering_proficiency
  );

  return (
    <div className="min-h-screen bg-black text-white p-6">
      <h1 className="flex font-mono item-center justify-center text-5xl font-bold mb-6">
        Interview Analytics Dashboard
      </h1>

      {/* Cards for Key Metrics */}
      <div className="flex flex-wrap my-20 items-center justify-center gap-y-2 bg-black">
        <div className="px-10 py-4 sm:px-20 ">
          <p className="mb-0 whitespace-nowrap bg-gradient-to-b from-white to-gray-400 bg-clip-text text-4xl font-black text-transparent sm:text-6xl">
            {analytics.performance_trends.interview_scores.slice(-1)[0].score}{" "}
          </p>
          <p className="mt-2 text-center text-lg leading-relaxed tracking-wide text-gray-400">
            Interview Score
          </p>
        </div>

        <div className="px-10 py-4 sm:px-20 ">
          <p className="mb-0 whitespace-nowrap bg-gradient-to-b from-white to-gray-400 bg-clip-text text-4xl font-black text-transparent sm:text-6xl">
            {
              analytics.performance_trends.grammar_accuracy.slice(-1)[0]
                .accuracy
            }
          </p>
          <p className="mt-2 text-center text-lg leading-relaxed tracking-wide text-gray-400">
            Grammar Accuracy
          </p>
        </div>
        <div className="px-10 py-4 sm:px-20 ">
          <p className="mb-0 whitespace-nowrap bg-gradient-to-b from-white to-gray-400 bg-clip-text text-4xl font-black text-transparent sm:text-6xl">
            {analytics.performance_trends.interview_frequency}
          </p>
          <p className="mt-2 text-center text-lg leading-relaxed tracking-wide text-gray-400">
            Interview Frequency
          </p>
        </div>
      </div>
      {/* <Card>
          <CardContent>
            <CardTitle>Interview Score</CardTitle>
            <p className="text-2xl">
              {analytics.performance_trends.interview_scores.slice(-1)[0].score}{" "}
              / 100
            </p>
          </CardContent>
        </Card>



        <Card>
          <CardContent>
            <CardTitle>Grammar Accuracy</CardTitle>
            <p className="text-2xl">
              {
                analytics.performance_trends.grammar_accuracy.slice(-1)[0]
                  .accuracy
              }
              %
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <CardTitle>Interview Frequency</CardTitle>
            <p className="text-2xl">
              {analytics.performance_trends.interview_frequency} Sessions
            </p>
          </CardContent>
        </Card> */}

      {/* Charts */}
      <div
        className="bg-gray-800 p-4  rounded-xl"
        style={{ width: "100%", height: "500px" }}
      >
        <h2 className="text-xl font-semibold mb-2">
          Interview Scores Over Time
        </h2>
        <Line
          data={{
            labels: analytics.performance_trends.interview_scores.map(
              (item) => item.date
            ),
            datasets: [
              {
                label: "Score",
                data: analytics.performance_trends.interview_scores.map(
                  (item) => item.score
                ),
                borderColor: "#4CAF50",
                fill: false,
              },
              {
                label: "Grammar Accuracy",
                data: analytics.performance_trends.grammar_accuracy.map(
                  (item) => item.accuracy
                ),
                borderColor: "#F44336",
                fill: false,
              },
            ],
          }}
          options={{
            responsive: true,
            maintainAspectRatio: false, // Allows height customization
            scales: {
              x: {
                title: {
                  display: true,
                  align: "center",
                  color: "#fff",
                },
              },
            },
          }}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        {/* Questions */}
        <div className="flex flex-col mb-8 md:mb-auto gap-3.5 flex-1 p-4 mt-16">
          <h2 className="flex gap-3 items-center m-auto text-4xl mb-4 font-bold md:flex-col md:gap-2">
            Most Frequent Questions
          </h2>
          <ul className="flex flex-col gap-4 w-full sm:max-w-md m-auto">
            {analytics.qa_analysis.most_frequent_questions.map(
              (question, index) => (
                <li
                  className="w-full bg-gray-900 p-3 text-xl  rounded-md"
                  key={index}
                >
                  {question}
                </li>
              )
            )}
            <div className="flex items-center mt-12">
              <div className="relative">
                {/* <img className="h-16 w-16 rounded-full object-cover" src="https://randomuser.me/api/portraits/women/87.jpg" alt="Avatar"> */}
                {analytics.qa_analysis.difficulty_levels === "easy" ? (
                  <Image
                    src="/green_speedometer.png"
                    alt="Avatar"
                    width={64}
                    height={64}
                    className="rounded-full"
                  />
                ) : analytics.qa_analysis.difficulty_levels === "hard" ? (
                  <Image
                    src="/red_speedometer.png"
                    alt="Avatar"
                    width={64}
                    height={64}
                    className="rounded-full"
                  />
                ) : (
                  <Image
                    src="/yellow_speedometer.png"
                    alt="Avatar"
                    width={64}
                    height={64}
                    className="rounded-full"
                  />
                )}

                <div className="absolute inset-0 rounded-full shadow-inner"></div>
              </div>
              <div className="ml-4 ">
                <h2 className="font-bold text-gray-400 text-3xl">
                  Difficulty Level
                </h2>
                <p className="text-gray-600">
                  {analytics.qa_analysis.difficulty_levels}
                </p>
              </div>
            </div>
          </ul>

          {/* {analytics.qa_analysis.answering_proficiency.map((item, index) => (
            <>
              <CircularProgress
                percent={item}
                color="green"
                label="Answering Proficiency"
                value={item}
              />
            </>
          ))} */}
        </div>
        {/* difficulty level */}
        <div>
          {proficiencyArray.map(([category, score]) => (
            <div className=" flex justify-center mt-16">
              <CircularProgress
                percent={score}
                color="yellow"
                label={category}
                value={score}
              />
            </div>
          ))}{" "}
        </div>
        <div
          className="bg-gray-800 p-8  rounded-xl"
          style={{ width: "100%", height: "90%" }}
        >
          {/* <h2 className="text-xl font-semibold mb-2"></h2> */}
          <h2 className="flex gap-3 items-center m-auto text-4xl mb-4 font-bold md:flex-col md:gap-2">
            Sentiment Distribution
          </h2>
          <Bar
            data={{
              labels: ["Positive", "Neutral", "Negative"],
              datasets: [
                {
                  label: "Sentiment",
                  data: Object.values(
                    analytics.sentiment_confidence_analysis
                      .sentiment_distribution
                  ),
                  backgroundColor: ["#4CAF50", "#FFC107", "#F44336"],
                },
              ],
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false, // Allows height customization
              scales: {
                x: {
                  title: {
                    display: true,
                    align: "center",
                    color: "#fff",
                  },
                },
              },
            }}
          />
        </div>
        <div className="bg-gray-800 p-4 rounded-xl">
          <div className="flex flex-col mb-8 md:mb-auto gap-3.5 flex-1 p-4 mt-4">
            <h2 className="flex gap-3 items-center m-auto text-4xl mb-4 font-bold md:flex-col md:gap-2">
              Feedback Trends
            </h2>
            <ul className="flex flex-col gap-4 w-full sm:max-w-md m-auto">
              {analytics.ai_recommendations.feedback_trends.map(
                (question, index) => (
                  <li
                    className="w-full bg-gray-900 p-3 text-xl  rounded-md"
                    key={index}
                  >
                    {question}
                  </li>
                )
              )}
            </ul>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-xl">
          <div className="flex flex-col mb-8 md:mb-auto gap-3.5 flex-1 p-4 mt-4">
            <h2 className="flex gap-3 items-center m-auto text-4xl mb-4 font-bold md:flex-col md:gap-2">
              Feedback Trends
            </h2>
            <ul className="flex flex-col gap-4 w-full sm:max-w-md m-auto">
              {analytics.ai_recommendations.suggested_improvements.map(
                (question, index) => (
                  <li
                    className="w-full bg-gray-900 p-3 text-xl  rounded-md"
                    key={index}
                  >
                    {question}
                  </li>
                )
              )}
            </ul>
          </div>
        </div>
        <div
          className="bg-gray-800 p-4 h-full  rounded-xl"
          style={{ width: "100%", height: "90%" }}
        >
          <h2 className="flex gap-3 items-center m-auto text-4xl mb-4 font-bold md:flex-col md:gap-2">
            User vs AI Talk Time
          </h2>
          <Pie
            className="ml-44"
            data={{
              labels: ["User", "AI"],
              datasets: [
                {
                  data: [
                    analytics.engagement_patterns.user_talk_time.slice(-1)[0]
                      .average_user_talk_time,
                    analytics.engagement_patterns.user_talk_time.slice(-1)[0]
                      .average_ai_talk_time,
                  ],
                  backgroundColor: ["#03A9F4", "#9C27B0"],
                },
              ],
            }}
            options={{
              responsive: true,
              maintainAspectRatio: true,
              plugins: {
                datalabels: {
                  color: "#fff", // Label color
                  font: { weight: "bold", size: 22 },
                  formatter: (value, ctx) => {
                    let sum = ctx.chart.data.datasets[0].data.reduce(
                      (a, b) => a + b,
                      0
                    );
                    let percentage = ((value / sum) * 100).toFixed(1) + "%";
                    return percentage;
                  },
                },
              },
            }}
          />
        </div>
      </div>

      {/* AI Suggestions & Improvements */}
      <div className="mt-6 bg-gray-800 p-6 rounded-xl">
        <h2 className="text-2xl font-bold">AI Feedback & Next Steps</h2>
        <div className="mt-3">
          <h3 className="text-lg font-semibold">Feedback Trends:</h3>
          <ul className="list-disc pl-6">
            {analytics.ai_recommendations.feedback_trends.map(
              (feedback, index) => (
                <li key={index} className="text-gray-300">
                  {feedback}
                </li>
              )
            )}
          </ul>
        </div>
        <div className="mt-3">
          <h3 className="text-lg font-semibold">Suggested Improvements:</h3>
          <ul className="list-disc pl-6">
            {analytics.ai_recommendations.suggested_improvements.map(
              (improvement, index) => (
                <li key={index} className="text-gray-300">
                  {improvement}
                </li>
              )
            )}
          </ul>
        </div>
        <div className="mt-3">
          <h3 className="text-lg font-semibold">Next Steps:</h3>
          <ul className="list-disc pl-6">
            {analytics.ai_recommendations.next_steps.map((step, index) => (
              <li key={index} className="text-gray-300">
                {step}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
