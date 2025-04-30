"use client";

import { use, useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const CustomDatePicker = ({ selectedDate, setSelectedDate, handle }) => {
  const [dates, setDates] = useState([]);
  useEffect(() => {
    // Set the date to the current date
    fetch(`http://localhost:5000/api/get_dates`, {
      method: "GET",
      credentials: "include", // Ensures cookies are sent
    })
      .then((response) => response.json())
      .then((data) => {
        setDates(data.map((date) => new Date(date)));
        console.log("dates: ", data[data.length - 1]);
        setSelectedDate(data[data.length - 1]);

        // console.log("ANALATICS :: ", data.analytics.analytics);
        // console.log("main ANALATICS :: ", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, []);

  return (
    <div className="relative max-w-sm">
      {/* Icon */}
      <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
        <svg
          className="w-4 h-4 text-gray-500 dark:text-gray-400"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z" />
        </svg>
      </div>

      {/* Date Picker Input */}
      <DatePicker
        selected={selectedDate}
        onChange={(date) => {
          // handle();
          setSelectedDate(date);
          console.log("date: ", date);

          handle(date);
        }} // Updating the parent state
        dateFormat="MM-dd-yyyy"
        placeholderText="Select date"
        includeDates={dates} // Only these dates will be selectable
        maxDate={new Date()} // Disable future dates
        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      />
    </div>
  );
};

export default CustomDatePicker;
