import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import authImage from "../assets/auth-image.png";
import { loginUser } from "../services/auth-Service";
import { validateLoginForm } from "../utils/validation";

function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const clearFieldError = (fieldName) => {
    setErrors((prev) => ({
      ...prev,
      [fieldName]: "",
    }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    clearFieldError(name);
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validateLoginForm(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setMessage("");
    setLoading(true);

    try {
      const encryptedFormData = {
        ...formData,
        password: btoa(formData.password),
      };

      const response = await loginUser(encryptedFormData);

      localStorage.setItem("user", JSON.stringify(response));
      navigate("/projects");
    } catch (error) {
      setMessage(error.detail || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div className="auth-left">
          <h1>
            Issue & Sprint
            <br />
            Management
          </h1>
          <div className="auth-image">
            <img src={authImage} alt="Issue ans sprint illustration" />
          </div>

          <p>
            Track issues, manage sprints and collaborate with your team in one
            place.
          </p>
        </div>

        <div className="auth-right">
          <h2>Welcome Back!</h2>
          <p className="auth-subtitle">Login to continue</p>

          <form onSubmit={handleSubmit}>
            <label>Email</label>
            <input
              type="text"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
            />
            {errors.email && <p className="error">{errors.email}</p>}

            <div className="password-container">
              <label>Password</label>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
              />
              {errors.password && <p className="error">{errors.password}</p>}
              <button
                type="button"
                className="toggle-password"
                aria-label={showPassword ? "Hide password" : "Show password"}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
              {errors.password && <p className="error">{errors.password}</p>}
            </div>

            <button className="auth-btn" type="submit" disabled={loading}>
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          {message && <p className="error">{message}</p>}

          <p className="auth-link">
            Don't have an account? <Link to="/register">Register</Link>
          </p>
        </div>
      </section>
    </main>
  );
}

export default Login;
