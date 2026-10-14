/**
 * Ministério Luz da Palavra — Core Application Scripts
 * Cabeçalho institucional dinâmico, acessibilidade, menu móvel com focus trap,
 * sincronização de seção ativa por IntersectionObserver e controles globais.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Controle de Rolagem do Cabeçalho (data-scrolled)
  const header = document.querySelector('.site-header');
  let lastScrollY = window.scrollY;

  const handleScroll = () => {
    const currentScrollY = window.scrollY;

    if (header) {
      if (currentScrollY > 40) {
        header.setAttribute('data-scrolled', 'true');
        header.classList.add('scrolled');
      } else {
        header.setAttribute('data-scrolled', 'false');
        header.classList.remove('scrolled');
      }
    }
    lastScrollY = currentScrollY;
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // Checagem inicial

  // 2. Menu Móvel (< 1024px) com Acessibilidade e Focus Trap
  const toggleBtn = document.getElementById('site-header-toggle');
  const mobilePanel = document.getElementById('site-mobile-panel');
  const closeBtn = document.getElementById('site-mobile-close');
  const backdrop = document.getElementById('site-mobile-backdrop');
  const mobileLinks = document.querySelectorAll('.site-header__mobile-link, .site-header__mobile-cta, .site-header__mobile-user-links a');

  if (toggleBtn && mobilePanel) {
    const focusableSelectors = 'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])';

    const openMobileMenu = () => {
      toggleBtn.setAttribute('aria-expanded', 'true');
      mobilePanel.setAttribute('aria-hidden', 'false');
      mobilePanel.classList.add('is-open');
      document.body.style.overflow = 'hidden';

      // Focus no primeiro item interativo dentro do painel
      const firstFocusable = mobilePanel.querySelector(focusableSelectors);
      if (firstFocusable) {
        setTimeout(() => firstFocusable.focus(), 50);
      }
    };

    const closeMobileMenu = () => {
      toggleBtn.setAttribute('aria-expanded', 'false');
      mobilePanel.setAttribute('aria-hidden', 'true');
      mobilePanel.classList.remove('is-open');
      document.body.style.overflow = '';
      toggleBtn.focus(); // Devolve foco ao botão
    };

    toggleBtn.addEventListener('click', () => {
      const isOpen = mobilePanel.classList.contains('is-open');
      if (isOpen) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', closeMobileMenu);
    }

    if (backdrop) {
      backdrop.addEventListener('click', closeMobileMenu);
    }

    // Fechar ao clicar em qualquer link de navegação do menu móvel
    mobileLinks.forEach(link => {
      link.addEventListener('click', closeMobileMenu);
    });

    // Fechar com ESC e Focus Trap (Tab / Shift+Tab)
    document.addEventListener('keydown', (e) => {
      if (!mobilePanel.classList.contains('is-open')) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        closeMobileMenu();
        return;
      }

      if (e.key === 'Tab') {
        const focusables = Array.from(mobilePanel.querySelectorAll(focusableSelectors));
        if (focusables.length === 0) return;

        const firstElement = focusables[0];
        const lastElement = focusables[focusables.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    });
  }

  // 3. Item Ativo por IntersectionObserver (Baseado na Seção Visível)
  const navLinks = document.querySelectorAll('.site-header__link');
  const sectionIds = ['tilted-grid-hero-root', 'ministerio', 'cultos', 'avisos', 'mensagens', 'galeria', 'contato'];
  const sections = sectionIds
    .map(id => document.getElementById(id))
    .filter(el => el !== null);

  if ('IntersectionObserver' in window && sections.length > 0) {
    const observerOptions = {
      root: null,
      rootMargin: '-20% 0px -60% 0px',
      threshold: 0
    };

    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          let targetSection = 'inicio';

          if (id === 'ministerio' || id === 'next-section') targetSection = 'ministerio';
          else if (id === 'cultos') targetSection = 'cultos';
          else if (id === 'mensagens' || id === 'transmissoes') targetSection = 'mensagens';
          else if (id === 'galeria') targetSection = 'galeria';
          else if (id === 'contato') targetSection = 'contato';
          else if (id === 'tilted-grid-hero-root') targetSection = 'inicio';

          navLinks.forEach(link => {
            if (link.getAttribute('data-section') === targetSection) {
              link.classList.add('active');
            } else {
              link.classList.remove('active');
            }
          });
        }
      });
    }, observerOptions);

    sections.forEach(section => sectionObserver.observe(section));
  }

  // 4. Dropdowns do Cabeçalho (Sininho de Notificações e Menu do Usuário)
  const bellBtn = document.getElementById('header-bell-btn');
  const notifDropdown = document.getElementById('header-notifications-dropdown');
  const avatarBtn = document.getElementById('header-avatar-btn');
  const userDropdown = document.getElementById('header-user-dropdown');

  const closeDropdowns = () => {
    if (notifDropdown) {
      notifDropdown.classList.remove('show');
      notifDropdown.setAttribute('aria-hidden', 'true');
      if (bellBtn) bellBtn.setAttribute('aria-expanded', 'false');
    }
    if (userDropdown) {
      userDropdown.classList.remove('show');
      userDropdown.setAttribute('aria-hidden', 'true');
      if (avatarBtn) avatarBtn.setAttribute('aria-expanded', 'false');
    }
  };

  if (bellBtn && notifDropdown) {
    bellBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isShown = notifDropdown.classList.contains('show');
      closeDropdowns();
      if (!isShown) {
        notifDropdown.classList.add('show');
        notifDropdown.setAttribute('aria-hidden', 'false');
        bellBtn.setAttribute('aria-expanded', 'true');
      }
    });
  }

  if (avatarBtn && userDropdown) {
    avatarBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isShown = userDropdown.classList.contains('show');
      closeDropdowns();
      if (!isShown) {
        userDropdown.classList.add('show');
        userDropdown.setAttribute('aria-hidden', 'false');
        avatarBtn.setAttribute('aria-expanded', 'true');
      }
    });
  }

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.site-header__bell-wrap') && !e.target.closest('.site-header__user-menu')) {
      closeDropdowns();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeDropdowns();
    }
  });

  // 5. Suporte a rolagem suave para âncoras locais com foco acessível
  document.querySelectorAll('a[href*="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      const hashIndex = href.indexOf('#');
      if (hashIndex !== -1) {
        const hash = href.substring(hashIndex);
        if (hash.length > 1) {
          const targetEl = document.querySelector(hash);
          if (targetEl) {
            e.preventDefault();
            targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
            targetEl.setAttribute('tabindex', '-1');
            targetEl.focus({ preventScroll: true });
          }
        }
      }
    });
  });

  // 6. Prefers-reduced-motion check
  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  window.MLP_REDUCED_MOTION = mediaQuery.matches;
  mediaQuery.addEventListener('change', () => {
    window.MLP_REDUCED_MOTION = mediaQuery.matches;
  });
});
