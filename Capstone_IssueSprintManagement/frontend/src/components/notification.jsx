function Notification({ message, type, onClose }) {
    if (!message) return null;

    return (
        <div className={`custom-toast ${type}`}>
            <span>{message}</span>
            <button type="button" onClick={onClose}>
                ×
            </button>
        </div>
    );
}

export default Notification;
