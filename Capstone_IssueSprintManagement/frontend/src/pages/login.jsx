import { useState } from "react";
import { loginUser } from "../services/auth-Service";
import { validateLoginForm } from "../utils/validation";
import { Link } from "react-router-dom";

function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    setErrors((prev) => ({
      ...prev,
      [name]: "",
    }));

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
      const encodedFormData = {
        ...formData,
        password: btoa(formData.password),
      };

      const response = await loginUser(encodedFormData);

      setMessage(response.message);

      localStorage.setItem("user", JSON.stringify(response));

      setFormData({
        email: "",
        password: "",
      });
    } catch (error) {
      setMessage(error.detail || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>User Login</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
          />
          {errors.email && <p className="error">{errors.email}</p>}
        </div>

        <div>
          <label>Password</label>
          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
          />
          {errors.password && <p className="error">{errors.password}</p>}
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>

      {message && (
        <p className={message.includes("successful") ? "success" : "error"}>
          {message}
        </p>
      )}
    </div>
  );
}

export default Login;
