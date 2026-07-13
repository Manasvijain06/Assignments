import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import authImage from "../assets/auth-image.png";
import Notification from "../components/Notification";
import { registerUser } from "../services/auth-Service";
import { validateRegisterForm } from "../utils/validation";

function Register() {
  const navigate = useNavigate();

  const initialFormData = {
    name: "",
    email: "",
    password: "",
    role: "",
  };

  const [formData, setFormData] = useState(initialFormData);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [notification, setNotification] = useState({
    message: "",
    type: "",
  });

  const showNotification = (message, type = "success") => {
    setNotification({ message, type });

    setTimeout(() => {
      setNotification({ message: "", type: "" });
    }, 3000);
  };

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
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validateRegisterForm(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    try {
      const encryptedFormData = {
        ...formData,
        password: btoa(formData.password),
      };
      const response = await registerUser(encryptedFormData);

      showNotification("Registration successful!","success");
      setFormData(initialFormData);

      setTimeout(() => {
        navigate("/login");
      }, 1000);
    } catch (error) {
      showNotification(error.detail || "Registration Failed","error");
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
            <img src={authImage} alt="Authentication" />
          </div>

          <p>
            Track issues, manage sprints and collaborate with your team in one
            place.
          </p>
        </div>

        <div className="auth-right">
          <h2>Create Account</h2>
          <p className="auth-subtitle">Register to get started</p>
          <form onSubmit={handleSubmit}>
            <label>Full Name</label>
            <input
              type="text"
              name="name"
              placeholder="Enter your name"
              value={formData.name}
              onChange={handleChange}
            />
            {errors.name && <p className="error">{errors.name}</p>}

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
                placeholder="Enter strong password"
                value={formData.password}
                onChange={handleChange}
              />
              {errors.password && <p className="error">{errors.password}</p>}
              <button
                type="button"
                className="toggle-password"
                aria-label={showPassword ? "Hide password" : "Show password"}
                onClick={() => setShowPassword((prev) => !prev)}
              >
                {showPassword ? "Hide" : "Show"}
              </button>

            </div>

            <label>Role</label>
            <select name="role" value={formData.role} onChange={handleChange}>
              <option value="">Select Role</option>
              <option value="member">Member</option>
              <option value="viewer">Viewer</option>
            </select>
            {errors.role && <p className="error">{errors.role}</p>}

            <button className="auth-btn" type="submit" disabled={loading}>
              {loading ? "Registering..." : "Register"}
            </button>
          </form>
          <p className="auth-link">
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </div>
      </section>
      <Notification
        message={notification.message}
        type={notification.type}
        onClose={() => setNotification({ message: "", type: "" })}
      />
    </main>
  );
}

export default Register;
