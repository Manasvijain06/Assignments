import { useState } from "react";

import Sidebar from "../components/Sidebar";
import { updateProfile, changePassword } from "../services/auth-service";
import Notification from "../components/Notification";

const initialPasswordData = {
  current_password: "",
  new_password: "",
};

function Profile() {
    const storedUser = JSON.parse(localStorage.getItem("user") || "{}");

    const [user, setUser] = useState(storedUser);
    const [isEditing, setIsEditing] = useState(false);
    const [name, setName] = useState(storedUser?.name || "");

    const [passwordData, setPasswordData] = useState(initialPasswordData);
    const [showCurrentPassword, setShowCurrentPassword] = useState(false);
    const [showNewPassword, setShowNewPassword] = useState(false);

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

    const handlePasswordChange = (fieldName, value) => {
      setPasswordData((prev) => ({
        ...prev,
        [fieldName]: value,
      }));
    };

     const handleUpdateProfile = async () => {
       if (!name.trim()) {
         showNotification("Name is required.", "error");
         return;
       }

       if (name.trim().length < 2) {
         showNotification("Name must be at least 2 characters long.", "error");
         return;
       }

       try {
         const response = await updateProfile(user.user_id, {
           name: name.trim(),
         });

         localStorage.setItem("user", JSON.stringify(response.user));
         setUser(response.user);
         setName(response.user.name);
         setIsEditing(false);

         showNotification("Profile updated successfully.", "success");
       } catch (error) {
         showNotification(error.detail || "Profile update failed.", "error");
       }
     };

    const handleChangePassword = async () => {
      if (!passwordData.current_password) {
        showNotification("Current password is required.", "error");
        return;
      }

      if (!passwordData.new_password) {
        showNotification("New password is required.", "error");
        return;
      }

      if (passwordData.new_password.length < 6) {
        showNotification(
          "New password must be at least 6 characters long.",
          "error",
        );
        return;
      }
       if (passwordData.current_password === passwordData.new_password) {
         showNotification(
           "New password must be different from current password.",
           "error",
         );
         return;
       }

      try {
        await changePassword(user.user_id, {
          current_password: btoa(passwordData.current_password),
          new_password: btoa(passwordData.new_password),
        });
        setPasswordData(initialPasswordData);
        setShowCurrentPassword(false);
        setShowNewPassword(false);

        showNotification("Password changed successfully.", "success");
      } catch (error) {
        showNotification(error.detail || "Password change failed.", "error");
      }
    };

    const handleCancelEdit = () => {
      setName(user?.name || "");
      setIsEditing(false);
    };

    return (
      <div className="dashboard-layout">
        <Sidebar />

        <main className="dashboard-main">
          <div className="project-detail-header">
            <div className="project-title-box">
              <div className="project-logo">
                {user?.name?.charAt(0).toUpperCase()}
              </div>

              <div>
                <h1>My Profile</h1>
                <p>View and update your account information</p>
              </div>
            </div>
          </div>

          {!isEditing ? (
            <div className="profile-card-grid">
              <section className="overview-card">
                <h3>Profile Details</h3>

                <button
                  className="edit-project-btn"
                  onClick={() => setIsEditing(true)}
                >
                  Edit Profile
                </button>

                <p className="label">Name</p>
                <p>{user?.name || "-"}</p>

                <p className="label">Email</p>
                <p>{user?.email || "-"}</p>

                <p className="label">Role</p>
                <p>{user?.role || "-"}</p>
              </section>
            </div>
          ) : (
            <div className="project-overview-grid">
              <div className="overview-card">
                <h3>Edit Profile</h3>

                <p className="label">Name</p>
                <input value={name} onChange={(e) => setName(e.target.value)} />

                <p className="label">Email</p>
                <p>{user?.email || "-"}</p>

                <p className="label">Role</p>
                <p>{user?.role || "-"}</p>

                <div className="profile-action-row">
                  <button
                    className="modal-create-btn"
                    onClick={handleUpdateProfile}
                  >
                    Save
                  </button>

                  <button
                    type="button"
                    className="modal-cancel-btn"
                    onClick={() => setIsEditing(false)}
                  >
                    Cancel
                  </button>
                </div>
              </div>

              <div className="overview-card">
                <h3>Change Password</h3>

                <p className="label">Current Password</p>
                <div className="profile-password-field">
                  <input
                    type={showCurrentPassword ? "text" : "password"}
                    value={passwordData.current_password}
                    onChange={(e) =>
                      handlePasswordChange(
                        "current_password",
                        e.target.value,
                      )
                    }
                  />
                  <button
                    type="button"
                    onClick={() => setShowCurrentPassword((prev) => !prev)}
                  >
                    {showCurrentPassword ? "Hide" : "Show"}
                  </button>
                </div>

                <p className="label">New Password</p>
                <div className="profile-password-field">
                  <input
                    type={showNewPassword ? "text" : "password"}
                    value={passwordData.new_password}
                    onChange={(e) =>
                      handlePasswordChange("new_password", e.target.value)
                    }
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPassword((prev) => !prev)}
                  >
                    {showNewPassword ? "Hide" : "Show"}
                  </button>
                </div>

                <button
                  className="modal-create-btn"
                  onClick={handleChangePassword}
                >
                  Change Password
                </button>
              </div>
            </div>
          )}
        </main>
        <Notification
          message={notification.message}
          type={notification.type}
          onClose={() => setNotification({ message: "", type: "" })}
        />
      </div>
    );
}

export default Profile;
