import React, { useState } from "react";

const UserCard = ({ userName, isSpeaking, toggleSpeaking }) => {
  return (
    <div
      className={`relative p-4 w-60 h-40 rounded-lg shadow-lg border-2 ${
        isSpeaking ? "border-green-500 animate-pulse" : "border-gray-300"
      } bg-white transition`}
    >
      <div className="absolute top-2 left-2 flex items-center space-x-2">
        {isSpeaking && (
          <div className="w-3 h-3 rounded-full bg-green-500 animate-ping"></div>
        )}
        <p
          className={`text-sm font-medium ${
            isSpeaking ? "text-green-600" : "text-gray-600"
          }`}
        >
          {isSpeaking ? "Speaking" : "Idle"}
        </p>
      </div>
      <div className="flex flex-col items-center justify-center h-full">
        <div
          className={`w-16 h-16 rounded-full bg-gray-200 border-4 ${
            isSpeaking ? "border-green-500" : "border-gray-300"
          }`}
        ></div>
        <h3 className="text-lg font-semibold text-gray-800 mt-4">{userName}</h3>
      </div>
    </div>
  );
};

// const SpeakingIndicator = () => {
//   const [users, setUsers] = useState([
//     xz,
//     { id: 1, name: "John Doe", isSpeaking: false },
//     { id: 2, name: "Jane Smith", isSpeaking: false },
//   ]);

//   const toggleSpeaking = (id) => {
//     setUsers((prevUsers) =>
//       prevUsers.map(
//         (user) =>
//           user.id === id
//             ? { ...user, isSpeaking: !user.isSpeaking }
//             : { ...user, isSpeaking: false } // Ensure only one speaks at a time
//       )
//     );
//   };

//   return (
//     <div className="flex justify-center gap-4 p-6 bg-gray-100 min-h-screen">
//       {users.map((user) => (
//         <UserCard
//           key={user.id}
//           userName={user.name}
//           isSpeaking={user.isSpeaking}
//           toggleSpeaking={() => toggleSpeaking(user.id)}
//         />
//       ))}
//     </div>
//   );
// };

export default UserCard;
