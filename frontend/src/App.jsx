import { useState } from "react";
import "./index.css";

function App() {
  const [formData, setFormData] = useState({
    cement: 540,
    slag: 0,
    fly_ash: 0,
    water: 162,
    superplasticizer: 2.5,
    coarse_aggregate: 1040,
    fine_aggregate: 676,
    age: 28,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: Number(e.target.value),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:9000/api/concrete/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed");
      }

      setResult(data.predicted_strength_mpa);
    } catch (err) {
      setError(
        "Could not connect to the prediction server. Make sure the FastAPI backend is running on port 9000."
      );
    } finally {
      setLoading(false);
    }
  };

  const fields = [
    { name: "cement", label: "Cement", unit: "kg/m³" },
    { name: "slag", label: "Blast Furnace Slag", unit: "kg/m³" },
    { name: "fly_ash", label: "Fly Ash", unit: "kg/m³" },
    { name: "water", label: "Water", unit: "kg/m³" },
    { name: "superplasticizer", label: "Superplasticizer", unit: "kg/m³" },
    { name: "coarse_aggregate", label: "Coarse Aggregate", unit: "kg/m³" },
    { name: "fine_aggregate", label: "Fine Aggregate", unit: "kg/m³" },
    { name: "age", label: "Concrete Age", unit: "days" },
  ];

  return (
    <div className="app">
      <header>
        <div>
          <h1>🏗️ SeismoBuild AI</h1>
          <p>ML-Based Concrete Strength Assessment</p>
        </div>
        <span className="badge">AI Powered</span>
      </header>

      <main>
        <section className="hero">
          <h2>Predict Concrete Strength</h2>
          <p>
            Enter your concrete mixture details and let our machine learning
            model estimate its compressive strength.
          </p>
        </section>

        <div className="content-grid">
          <form className="prediction-form" onSubmit={handleSubmit}>
            <h3>Material Details</h3>

            <div className="form-grid">
              {fields.map((field) => (
                <div className="input-group" key={field.name}>
                  <label>
                    {field.label} <span>({field.unit})</span>
                  </label>
                  <input
                    type="number"
                    name={field.name}
                    value={formData[field.name]}
                    onChange={handleChange}
                    step="any"
                    required
                  />
                </div>
              ))}
            </div>

            <button type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Predict Strength"}
            </button>
          </form>

          <aside className="result-card">
            <h3>Prediction Result</h3>

            {result !== null ? (
              <>
                <div className="strength-value">{result}</div>
                <div className="unit">MPa</div>
                <p>
                  Estimated concrete compressive strength based on the trained
                  machine learning model.
                </p>
              </>
            ) : (
              <div className="empty-result">
                <div className="icon">📊</div>
                <p>Your prediction will appear here.</p>
              </div>
            )}
          </aside>
        </div>

        {error && <div className="error-message">{error}</div>}

        <section className="info">
          <h3>How does it work?</h3>
          <div className="steps">
            <div>
              <strong>1. Enter Materials</strong>
              <p>Provide quantities of the concrete mixture components.</p>
            </div>
            <div>
              <strong>2. AI Analysis</strong>
              <p>Our trained Random Forest model analyzes the mixture.</p>
            </div>
            <div>
              <strong>3. Get Prediction</strong>
              <p>Receive an estimated compressive strength in MPa.</p>
            </div>
          </div>
        </section>

        <p className="disclaimer">
          Educational ML project only. Results are estimates and should not be
          used as a substitute for professional structural engineering analysis.
        </p>
      </main>
    </div>
  );
}

export default App;