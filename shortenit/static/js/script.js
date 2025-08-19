document.addEventListener('DOMContentLoaded', () => {
  // Copy to clipboard for result page
  const copyBtn   = document.getElementById('copyBtn');
  const shortUrlEl = document.getElementById('shortUrl');

  if (copyBtn && shortUrlEl) {
    copyBtn.addEventListener('click', e => {
      const text = shortUrlEl.textContent.trim();
      const btn  = e.currentTarget;
      const orig = btn.textContent;

      navigator.clipboard.writeText(text)
        .then(() => {
          btn.textContent = '✅ Copied!';
          btn.style.background = '#28a745';

          setTimeout(() => {
            btn.textContent = orig;
            btn.style.background = '';
          }, 2000);
        })
        .catch(err => {
          console.error('Clipboard error:', err);
          alert('Failed to copy URL. Please copy it manually.');
        });
    });
  }
  
    const urlForm = document.getElementById('urlForm');
    const urlInput = document.getElementById('original_url');
    const submitBtn = document.getElementById('submitBtn');
    
    if (urlForm) {
        urlForm.addEventListener('submit', function(e) {
            const btnText = submitBtn.querySelector('.btn-text');
            const btnLoading = submitBtn.querySelector('.btn-loading');
            const errorMessage = document.getElementById('errorMessage');
            const successMessage = document.getElementById('successMessage');
            
            // Clear previous messages
            if (errorMessage) errorMessage.style.display = 'none';
            if (successMessage) successMessage.style.display = 'none';
            
            // Validate URL
            const url = urlInput.value.trim();
            if (!url) {
                showError('Please enter a URL');
                e.preventDefault();
                return;
            }
            
            if (!isValidUrl(url)) {
                showError('Please enter a valid URL starting with http:// or https://');
                e.preventDefault();
                return;
            }
            
            // Show loading state
            submitBtn.disabled = true;
            btnText.style.display = 'none';
            btnLoading.style.display = 'inline';
            
            // Form will submit normally
        });
    }
    
    // Real-time URL validation
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            const url = this.value.trim();
            if (url && !isValidUrl(url)) {
                this.style.borderColor = '#e74c3c';
            } else {
                this.style.borderColor = '#e1e5e9';
            }
        });
        
        // Auto-resize input on focus
        urlInput.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
        });
        
        urlInput.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
    }
});

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
}

function showSuccess(message) {
    const successMessage = document.getElementById('successMessage');
    if (successMessage) {
        successMessage.textContent = message;
        successMessage.style.display = 'block';
    }
}


// Inline slug-editing, deletion, and copy/share feedback
document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = '{{ csrf_token }}';
  
    // Helpers
    function fetchJSON(url, opts) {
      return fetch(url, opts).then(r => r.json());
    }
  
    // 1) Edit Slug
    document.querySelectorAll('.edit-slug-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const item = btn.closest('.url-item');
        item.querySelector('.slug-text').classList.add('hidden');
        item.querySelector('.inline-slug-form').style.display = 'inline-block';
        item.querySelector('.inline-slug-input').focus();
      });
    });
  
    // 2) Cancel Slug Edit
    document.querySelectorAll('.cancel-slug-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const item = btn.closest('.url-item');
        item.querySelector('.slug-text').classList.remove('hidden');
        item.querySelector('.inline-slug-form').style.display = 'none';
      });
    });
  
    // 3) Save New Slug
    document.querySelectorAll('.save-slug-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const item = btn.closest('.url-item');
        const id = item.dataset.id;
        const input = item.querySelector('.inline-slug-input');
        const newSlug = input.value.trim();
        if (!newSlug) return alert('Slug cannot be empty.');
  
        fetchJSON(
          `{% url 'api_rename_url' 0 %}`.replace('/0/', `/${id}/`),
          {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ short_url: newSlug })
          }
        ).then(data => {
          if (data.error) return alert(data.error);
          // Success: update UI
          item.querySelector('.slug-text').textContent = data.short_url;
          item.querySelector('.slug-text').classList.remove('hidden');
          item.querySelector('.inline-slug-form').style.display = 'none';
        });
      });
    });
  
    // 4) Delete URL
    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        if (!confirm('Really delete this link?')) return;
        const item = btn.closest('.url-item');
        const id = item.dataset.id;
  
        fetchJSON(
          `{% url 'api_delete_url' 0 %}`.replace('/0/', `/${id}/`),
          {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken }
          }
        ).then(data => {
          if (data.deleted) {
            item.remove();
          } else {
            alert('Failed to delete.');
          }
        });
      });
    });
  });
  