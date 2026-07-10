function Notification({ message, type, onClose }) {
  if (!message) {
    return null;
  }

  return (
    <div className={`custom-toast ${type}`} role="alert">
      <span>{message}</span>

      <button type="button" onClick={onClose} aria-label="Close notification">
        ×
      </button>
    </div>
  );
}

export default Notification;
