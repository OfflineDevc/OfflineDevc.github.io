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

// Fade-in on scroll
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

// Writeup Features (Mobile Sidebar & Image Lightbox)
document.addEventListener('DOMContentLoaded', () => {
  // Mobile Sidebar Toggle
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

  // Screenshot Lightbox Modal
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
