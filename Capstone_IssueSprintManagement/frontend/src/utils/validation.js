export const validateRegisterForm = (formData) => {
    const errors = {};

    // Name Validation
    if (!formData.name.trim()) {
        errors.name = "Name is required.";
    } else if (formData.name.trim().length < 3) {
        errors.name = "Name must be at least 3 characters long.";
    }

    // Email Validation
    if (!formData.email.trim()) {
        errors.email = "Email is required.";
    } else if (
        !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(formData.email)
    ) {
        errors.email = "Please enter a valid email address.";
    }

    // Password Validation
    if (!formData.password) {
        errors.password = "Password is required.";
    } else if (formData.password.length < 6) {
        errors.password = "Password must be at least 6 characters long.";
    } else if (!/[A-Z]/.test(formData.password)) {
        errors.password = "Password must contain one uppercase letter.";
    } else if (!/[a-z]/.test(formData.password)) {
        errors.password = "Password must contain one lowercase letter.";
    } else if (!/\d/.test(formData.password)) {
        errors.password = "Password must contain one digit.";
    } else if (!/[!@#$%^&*()_,.?":{}|<>]/.test(formData.password)) {
        errors.password = "Password must contain one special character.";
    }

    // Role Validation
    if (!formData.role) {
        errors.role = "Role is required.";
    }

    return errors;
};


export const validateLoginForm = (formData) => {
    const errors = {};

    // Email
    if (!formData.email.trim()) {
    errors.email = "Email is required.";
    } else if (
    !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(formData.email)
    ) {
    errors.email = "Enter a valid email address.";
    }

    // Password
    if (!formData.password) {
    errors.password = "Password is required.";
    } else if (formData.password.length < 6) {
    errors.password = "Password must be at least 6 characters long.";
    }

    return errors;
};