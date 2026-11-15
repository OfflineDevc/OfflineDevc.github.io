// Filter buttons on index page
const filterBtns = document.querySelectorAll('.filter-btn');
const cards      = document.querySelectorAll('.writeup-card');

if (filterBtns.length > 0) {
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;
      cards.forEach(card => {
        const tags = card.dataset.tags || '';
        if (filter === 'all' || tags.includes(filter)) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
}

// Fade-in on scroll (index cards)
if (cards.length > 0) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.08 });

  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = `opacity .4s ${i * 0.06}s ease, transform .4s ${i * 0.06}s ease`;
    observer.observe(card);
  });
}

// Writeup Page Interactive Features
document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Sidebar Toggle
  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  if (sidebar && sidebarToggle && sidebarOverlay) {
    const toggleSidebar = () => {
      const isOpen = sidebar.classList.toggle('open');
      sidebarOverlay.classList.toggle('open', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    };

    sidebarToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleSidebar();
    });

    sidebarOverlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      sidebarOverlay.classList.remove('open');
      document.body.style.overflow = '';
    });
  }

  // 2. Code Block Copy Buttons
  const preBlocks = document.querySelectorAll('.writeup-content pre');
  preBlocks.forEach(pre => {
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.type = 'button';
    copyBtn.innerText = 'Copy';

    copyBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const code = pre.querySelector('code');
      const textToCopy = code ? code.innerText : pre.innerText;

      navigator.clipboard.writeText(textToCopy).then(() => {
        copyBtn.innerText = 'Copied!';
        copyBtn.style.color = '#9fef00';
        copyBtn.style.borderColor = '#9fef00';
        setTimeout(() => {
          copyBtn.innerText = 'Copy';
          copyBtn.style.color = '';
          copyBtn.style.borderColor = '';
        }, 2000);
      }).catch(() => {
        copyBtn.innerText = 'Error';
      });
    });

    pre.appendChild(copyBtn);
  });

  // 3. Screenshot Lightbox Modal
  const images = document.querySelectorAll('.writeup-content img');
  if (images.length > 0) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-modal';
    lightbox.innerHTML = `
      <span class="lightbox-close">&times;</span>
      <img src="" alt="Zoomed Screenshot" />
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('img');
    const closeBtn = lightbox.querySelector('.lightbox-close');

    images.forEach(img => {
      img.addEventListener('click', (e) => {
        e.stopPropagation();
        lightboxImg.src = img.src;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    const closeLightbox = () => {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    };

    lightbox.addEventListener('click', closeLightbox);
    closeBtn.addEventListener('click', closeLightbox);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (lightbox.classList.contains('active')) {
          closeLightbox();
        }
        if (sidebar && sidebar.classList.contains('open')) {
          sidebar.classList.remove('open');
          sidebarOverlay.classList.remove('open');
          document.body.style.overflow = '';
        }
      }
    });
  }
});
