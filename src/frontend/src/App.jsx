import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import LandingPage from "./LandingPage";
import PatientDetails from "./PatientDetails";
import SearchPatient from "./SearchPage"; 

function App() {
  return (
    <Router>
      <header className="fixed top-0 left-0 w-full bg-white drop-shadow-lg z-10">
        <div className="mx-auto flex justify-between items-center p-4 px-6">
          <div className="text-2xl font-bold">Readmission Prediction Tool</div>
          <div className="flex gap-4">
            <button
              className="border-2 border-teal px-6 py-2 rounded-full font-medium hover:bg-teal hover:opacity-95 transition"
              onClick={() => window.location.href = './#prediction'}
            >
              Get Started
            </button>
            <Link to="/search">
              <button className="border-2 border-teal px-6 py-2 rounded-full font-medium bg-teal hover:bg-white transition">
                View Patient Details
              </button>
            </Link>
          </div>
        </div>
      </header>

      <main className="pt-16">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/search" element={<SearchPatient />} />
          <Route path="/patient-details" element={<PatientDetails />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;