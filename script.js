// ==========================================================================
// OFFLINEDEVC — INTERACTIVE JAVASCRIPT
// Minimalist, Clean UX/UI for Cybersecurity Technical Documentation
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {

  // 1. Filter Buttons on Homepage Bento Grid
  const filterBtns = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.writeup-card');

  if (filterBtns.length > 0 && cards.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.dataset.filter;
        cards.forEach(card => {
          const tags = card.dataset.tags || '';
          if (filter === 'all' || tags.includes(filter)) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // 2. Mobile Sidebar Drawer Toggle
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

  // 3. Code Block Copy Buttons
  const preBlocks = document.querySelectorAll('.writeup-content pre');
  preBlocks.forEach(pre => {
    // Avoid duplicate buttons
    if (pre.querySelector('.copy-btn')) return;

    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.type = 'button';
    copyBtn.innerText = 'Copy';

    copyBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const code = pre.querySelector('code');
      const textToCopy = code ? code.innerText : pre.innerText;

      navigator.clipboard.writeText(textToCopy).then(() => {
        const originalText = copyBtn.innerText;
        copyBtn.innerText = 'Copied!';
        copyBtn.style.color = '#10B981';
        copyBtn.style.borderColor = '#10B981';
        setTimeout(() => {
          copyBtn.innerText = originalText;
          copyBtn.style.color = '';
          copyBtn.style.borderColor = '';
        }, 2000);
      }).catch(() => {
        copyBtn.innerText = 'Error';
      });
    });

    pre.appendChild(copyBtn);
  });

  // 4. Sticky Table of Contents ScrollSpy & Smooth Scrolling
  const tocLinks = document.querySelectorAll('.toc-menu a, .toc-link');
  const headings = document.querySelectorAll('.writeup-content h2[id], .writeup-content h3[id]');

  if (tocLinks.length > 0 && headings.length > 0) {
    // ScrollSpy observer
    const onScroll = () => {
      let activeHeadingId = '';
      const scrollPosition = window.scrollY + 100;

      headings.forEach(heading => {
        const top = heading.offsetTop;
        if (scrollPosition >= top) {
          activeHeadingId = heading.getAttribute('id');
        }
      });

      if (!activeHeadingId && headings.length > 0) {
        activeHeadingId = headings[0].getAttribute('id');
      }

      tocLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${activeHeadingId}`) {
          link.classList.add('active');
        }
      });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // Run once on init
  }

  // 5. Image Lightbox Zoom Modal
  const images = document.querySelectorAll('.writeup-content img');
  if (images.length > 0) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-modal';
    lightbox.style.cssText = `
      position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 2000;
      display: none; align-items: center; justify-content: center; cursor: zoom-out;
      backdrop-filter: blur(4px);
    `;
    lightbox.innerHTML = `
      <img src="" alt="Enlarged screenshot" style="max-width: 90vw; max-height: 90vh; border-radius: 6px; box-shadow: 0 10px 40px rgba(0,0,0,0.5); object-fit: contain;" />
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('img');

    images.forEach(img => {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', (e) => {
        e.stopPropagation();
        lightboxImg.src = img.src;
        lightbox.style.display = 'flex';
        document.body.style.overflow = 'hidden';
      });
    });

    const closeLightbox = () => {
      lightbox.style.display = 'none';
      document.body.style.overflow = '';
    };

    lightbox.addEventListener('click', closeLightbox);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeLightbox();
        if (sidebar && sidebar.classList.contains('open')) {
          sidebar.classList.remove('open');
          sidebarOverlay.classList.remove('open');
          document.body.style.overflow = '';
        }
      }
    });
  }

});
