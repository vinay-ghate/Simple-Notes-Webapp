// Enhanced note deletion with better UX
function deleteNote(noteId) {
  if (confirm('Are you sure you want to delete this note?')) {
    const button = event.target.closest('button');
    const originalContent = button.innerHTML;
    
    // Show loading state
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Deleting...';
    button.disabled = true;
    
    fetch("/delete-note", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ noteId: noteId }),
    })
    .then(response => {
      if (response.ok) {
        // Smooth fade out animation
        const noteItem = button.closest('.note-item');
        noteItem.style.transition = 'all 0.3s ease';
        noteItem.style.opacity = '0';
        noteItem.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
          window.location.href = "/";
        }, 300);
      } else {
        throw new Error('Failed to delete note');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      button.innerHTML = originalContent;
      button.disabled = false;
      
      // Show error message
      const alert = document.createElement('div');
      alert.className = 'alert alert-danger alert-dismissible fade show mt-3';
      alert.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        Failed to delete note. Please try again.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      button.closest('.note-item').appendChild(alert);
      
      // Auto-hide error after 5 seconds
      setTimeout(() => {
        if (alert.parentNode) {
          alert.remove();
        }
      }, 5000);
    });
  }
}

// Form enhancements
document.addEventListener('DOMContentLoaded', function() {
  // Auto-resize textarea
  const textarea = document.getElementById('note');
  if (textarea) {
    textarea.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.max(120, this.scrollHeight) + 'px';
    });
    
    // Focus on textarea when page loads
    textarea.focus();
  }
  
  // Form validation feedback
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(event) {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        const originalContent = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="loading me-2"></span>Processing...';
        submitBtn.disabled = true;
        
        // Re-enable button after 3 seconds if form doesn't submit
        setTimeout(() => {
          if (submitBtn.disabled) {
            submitBtn.innerHTML = originalContent;
            submitBtn.disabled = false;
          }
        }, 3000);
      }
    });
  });
  
  // Auto-hide alerts
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      if (alert.parentNode && bootstrap.Alert) {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }
    }, 5000);
  });
  
  // Smooth scroll for navigation
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});