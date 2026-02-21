// ── Theme Toggle ─────────────────────────────────────────
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

function setTheme(theme) {
  html.setAttribute('data-theme', theme);
  localStorage.setItem('luxe-theme', theme);
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    setTheme(current === 'dark' ? 'light' : 'dark');
  });
}

// ── Mobile Menu ──────────────────────────────────────────
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenuClose = document.getElementById('mobileMenuClose');
const mobileMenu = document.getElementById('mobileMenu');

function openMenu() {
  mobileMenu.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeMenu() {
  mobileMenu.classList.remove('open');
  document.body.style.overflow = '';
}

if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', openMenu);
if (mobileMenuClose) mobileMenuClose.addEventListener('click', closeMenu);
if (mobileMenu) {
  mobileMenu.addEventListener('click', (e) => {
    if (e.target === mobileMenu) closeMenu();
  });
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeMenu();
});

// ── Auto-dismiss flash messages ──────────────────────────
document.querySelectorAll('.flash-message').forEach(msg => {
  setTimeout(() => {
    msg.style.opacity = '0';
    msg.style.transform = 'translateX(20px)';
    msg.style.transition = 'all 0.3s ease';
    setTimeout(() => msg.remove(), 300);
  }, 4000);
});

// ── Quantity selectors ───────────────────────────────────
document.querySelectorAll('.qty-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = btn.parentElement.querySelector('.qty-input');
    let val = parseInt(input.value) || 1;
    if (btn.dataset.action === 'minus') val = Math.max(1, val - 1);
    if (btn.dataset.action === 'plus') val = Math.min(99, val + 1);
    input.value = val;
  });
});

// ── Product image gallery ────────────────────────────────
const mainImg = document.querySelector('.product-main-image img');
document.querySelectorAll('.product-thumb').forEach(thumb => {
  thumb.addEventListener('click', () => {
    if (mainImg && thumb.querySelector('img')) {
      mainImg.src = thumb.querySelector('img').src;
    }
    document.querySelectorAll('.product-thumb').forEach(t => t.classList.remove('active'));
    thumb.classList.add('active');
  });
});

// ── Scroll-triggered animations ──────────────────────────
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.product-card, .category-card, .feature-item').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(18px)';
    el.style.transition = `opacity 0.45s ease ${i * 0.04}s, transform 0.45s ease ${i * 0.04}s`;
    observer.observe(el);
  });
}

// ── Cart update form on qty change ───────────────────────
document.querySelectorAll('[data-cart-form]').forEach(form => {
  form.querySelector('.qty-input')?.addEventListener('change', () => form.submit());
});
