import { useState } from "react";
import { registerUser } from "../services/authService";
import { validateRegisterForm } from "../utils/validation";

function Register() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "member",
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
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validateRegisterForm(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setMessage("");

    try {
      const response = await registerUser(formData);

      setMessage(response.message);

      setFormData({
        name: "",
        email: "",
        password: "",
        role: "member",
      });
    } catch (error) {
      setMessage(error.detail || "Registration Failed");
    }
  };

  return (
    <div className="container">
      <h2>User Registration</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Enter Name"
          value={formData.name}
          onChange={handleChange}
        />
        {errors.name && (
          <p style={{ color: "red", marginTop: "5px" }}>{errors.name}</p>
        )}

        <br />

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

        <select name="role" value={formData.role} onChange={handleChange}>
          <option value="member">Member</option>
          <option value="admin">Admin</option>
          <option value="viewer">Viewer</option>
        </select>

        {errors.role && (
          <p style={{ color: "red", marginTop: "5px" }}>{errors.role}</p>
        )}

        <br />

        <button type="submit">Register</button>
      </form>

      {message && (
        <p
          style={{
            marginTop: "20px",
            color: message.includes("successfully") ? "green" : "red",
          }}
        >
          {message}
        </p>
      )}
    </div>
  );
}

export default Register;
