// Toast utility function for showing notifications
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        console.error('Toast container not found!');
        return;
    }
    
    toastContainer.appendChild(toast);
    
    // Animate the toast
    setTimeout(() => {
        toast.classList.add('visible');
    }, 10);
    
    // Remove the toast after 5 seconds
    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 5000);
}

// Make the function globally available
window.showToast = showToast;
