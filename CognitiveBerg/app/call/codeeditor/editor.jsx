"use client";

import React, { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";

const CodeEditor = ({
  code,
  setCode,
  language,
  setLanguage,
  output,
  setOutput,
  setCodeSubmitted,
  codeSubmitted,
}) => {
  const languages = [
    { name: "Python", value: "python" },
    { name: "JavaScript", value: "javascript" },
    { name: "C", value: "c" },
    { name: "C++", value: "cpp" },
    { name: "Java", value: "java" },
  ];
  const [sbutton, setsButton] = useState(false);

  const handleEditorChange = (value) => {
    setCode(value);
    setsButton(false);
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const runCode = async () => {
    console.log("inrun");
    const url = "https://onecompiler-apis.p.rapidapi.com/api/v1/run";
    const options = {
      method: "POST",
      headers: {
        "x-rapidapi-key": "e392557994msh90bcd2a109f84e4p1b52e9jsn63ee20608b85",
        "x-rapidapi-host": "onecompiler-apis.p.rapidapi.com",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        language,
        stdin: "",
        files: [{ name: `main.${language}`, content: code }],
      }),
    };

    try {
      const response = await fetch(url, options);
      const result = await response.json();
      setOutput(result.stdout || result.stderr);
      console.log(result);
    } catch (error) {
      console.error(error);
      setOutput("Error running code");
    }
  };
  //   useEffect(() => {
  const submitCode = async () => {
    try {
      const response = await fetch("http://localhost:5000/getcode", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code, language }),
        credentials: "include",
      });

      const data = await response.json();
      console.log(data);
      if (data.submitted == true) {
        setsButton(true);
        console.log(sbutton);

        setCodeSubmitted(true);
      }
      //   setCodeSubmitted(false);
    } catch (error) {
      console.error("Request failed:", error);
    }
  };

  //   }, [codeSubmitted]);

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-900 text-white p-4">
      {/* Language Selector */}
      <div className="mb-4 flex gap-4">
        <select
          className="p-2 bg-gray-800 text-white border rounded-lg"
          value={language}
          onChange={handleLanguageChange}
        >
          {languages.map((lang) => (
            <option key={lang.value} value={lang.value}>
              {lang.name}
            </option>
          ))}
        </select>
        <button
          onClick={runCode}
          className="bg-blue-500 px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Run Code
        </button>
        <button
          onClick={submitCode}
          type="button"
          disabled={sbutton}
          class={
            sbutton
              ? "bg-gray-600 px-4 py-2 fixed right-4 rounded-lg"
              : "bg-green-600 px-4 py-2 fixed right-4 rounded-lg hover:bg-green-800"
          }
        >
          Submit
        </button>
      </div>

      {/* Code Editor */}
      <div className="w-full h-[60vh] border rounded-lg shadow-lg">
        <Editor
          height="100%"
          width="100%"
          theme="vs-dark"
          language={language}
          value={code}
          onChange={handleEditorChange}
        />
      </div>

      {/* Output Section */}
      <div className="w-full mt-4 p-4 bg-gray-800 rounded-md border">
        <h3 className="text-lg font-bold">Output:</h3>
        <pre className="text-green-400 whitespace-pre-wrap">{output}</pre>
      </div>
    </div>
  );
};

export default CodeEditor;
