import React from "react";
import { Link } from "react-router-dom";
import PredictionForm from "./PredictionForm";


const HeroSection = () => {
  return (
    <section className="flex flex-col items-center justify-center text-center py-20 px-8 mt-10">
      <h2 className="text-2xl font-bold mb-3">
        Welcome to the Readmission Prediction Tool
      </h2>
      <p className="text-sm opacity-90 mb-6 max-w-xl">
        Use our predictive tool to analyze readmission risk for patients with hyperglycemia. Just fill in patient details and see the prediction in real-time.
      </p>
    </section>
  );
};

const Footer = () => {
  return (
    <footer className="bg-white py-4 mt-10">
      <div className="container mx-auto text-center">
        <p className="text-xs opacity-75">
          © 2025 Readmission Prediction Tool. All Rights Reserved.
        </p>
      </div>
    </footer>
  );
};

const LandingPage = () => {
  return (
    <>
      <HeroSection />
      <section id="prediction" className="scroll-mt-10">
        <PredictionForm />
      </section>
      <Footer />
    </>
  );
};

export default LandingPage;
