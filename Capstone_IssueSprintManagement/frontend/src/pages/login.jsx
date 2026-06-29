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

    try {
      const response = await loginUser(formData);

      setMessage(response.message || "Login Successful");
      setFormData({
        email: "",
        password: "",
      });
    } catch (error) {
      setMessage(error.detail || "Invalid Email or Password");
    }
  };

  return (
    <div className="container">
      <h2>User Login</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Enter Email"
          value={formData.email}
          onChange={handleChange}
        />

        {errors.email && (
          <p style={{ color: "red", marginTop: "5px" }}>{errors.email}</p>
        )}
        <br />

        <input
          type="password"
          name="password"
          placeholder="Enter Password"
          value={formData.password}
          onChange={handleChange}
        />

        {errors.password && (
          <p style={{ color: "red", marginTop: "5px" }}>{errors.password}</p>
        )}

        <br />

        <button type="submit">Login</button>
      </form>

      <p style={{ marginTop: "15px" }}>
        Don't have an account? <Link to="/register">Register</Link>
      </p>

      {message && (
        <p
          style={{
            marginTop: "20px",
            color: message.toLowerCase().includes("success") ? "green" : "red",
          }}
        >
          {message}
        </p>
      )}
    </div>
  );
}

export default Login;
