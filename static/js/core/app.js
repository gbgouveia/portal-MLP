/**
 * Ministério Luz da Palavra — Core Application Scripts
 * Acessibilidade, navegação responsiva e comportamento global.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggle
  const toggleBtn = document.querySelector('.mobile-toggle');
  const siteNav = document.querySelector('.site-nav');

  if (toggleBtn && siteNav) {
    toggleBtn.addEventListener('click', () => {
      const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
      toggleBtn.setAttribute('aria-expanded', !isExpanded);
      siteNav.classList.toggle('open');
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!toggleBtn.contains(e.target) && !siteNav.contains(e.target) && siteNav.classList.contains('open')) {
        siteNav.classList.remove('open');
        toggleBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 2. Smooth Scroll for internal hash links with keyboard focus
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.length > 1) {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
          targetElement.setAttribute('tabindex', '-1');
          targetElement.focus({ preventScroll: true });
        }
      }
    });
  });

  // 3. Prefers-reduced-motion check logger
  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  window.MLP_REDUCED_MOTION = mediaQuery.matches;
  mediaQuery.addEventListener('change', () => {
    window.MLP_REDUCED_MOTION = mediaQuery.matches;
  });
});
