/**
 * Ministério Luz da Palavra — Coreografia Editorial (GSAP & Anime.js)
 * Orquestração respeitosa que não bloqueia leitura nem rolagem do usuário.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Se usuário preferir redução de movimento, encerra imediatamente
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  // 1. GSAP: Revelação suave do Hero Editorial e Tipografia
  if (typeof gsap !== 'undefined') {
    const heroTitle = document.querySelector('.hero-title');
    const heroQuote = document.querySelector('.hero-quote');
    const heroPortrait = document.querySelector('.hero-portrait-card');

    const heroTimeline = gsap.timeline({ defaults: { ease: 'power2.out' } });

    if (heroTitle) {
      heroTimeline.fromTo(
        heroTitle,
        { opacity: 0, y: 24 },
        { opacity: 1, y: 0, duration: 1.1 }
      );
    }

    if (heroQuote) {
      heroTimeline.fromTo(
        heroQuote,
        { opacity: 0, x: -16 },
        { opacity: 1, x: 0, duration: 0.8 },
        '-=0.6'
      );
    }

    if (heroPortrait) {
      heroTimeline.fromTo(
        heroPortrait,
        { opacity: 0, scale: 0.98 },
        { opacity: 1, scale: 1, duration: 1.2 },
        '-=0.7'
      );
    }

    // Revelação de Recorte Editorial da Fotografia (Clip-Path Reveal - Hero Section 2)
    const heroMask = document.querySelector('.hero-reveal-mask');
    if (heroMask) {
      heroTimeline.fromTo(
        heroMask,
        { clipPath: 'polygon(0 0, 100% 0, 100% 0%, 0 0%)' },
        { clipPath: 'polygon(0 0, 100% 0, 100% 100%, 0 100%)', duration: 1.3, ease: 'power3.inOut' },
        '-=0.9'
      );
    }

    const heroStats = document.querySelector('.hero-stats-strip');
    if (heroStats) {
      heroTimeline.fromTo(
        heroStats,
        { opacity: 0, y: 15 },
        { opacity: 1, y: 0, duration: 0.8 },
        '-=0.5'
      );
    }

    // ScrollTrigger para revelação suave dos marcos históricos (sem nunca ocultar texto)
    if (typeof ScrollTrigger !== 'undefined' && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      gsap.registerPlugin(ScrollTrigger);

      const timelineItems = document.querySelectorAll('.timeline-item');
      timelineItems.forEach((item) => {
        // Assegura visibilidade plena garantida
        gsap.set(item, { opacity: 1 });
        gsap.from(item, {
          y: 16,
          duration: 0.5,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: item,
            start: 'top 95%',
            once: true
          }
        });
      });
    }
  }

  // 2. Anime.js: Micro-animação sutil nos nós da timeline (evita conflito com GSAP)
  if (typeof anime !== 'undefined') {
    const nodes = document.querySelectorAll('.timeline-node');
    if (nodes.length) {
      nodes.forEach((node) => {
        node.addEventListener('mouseenter', () => {
          anime({
            targets: node,
            scale: [1, 1.35],
            borderColor: '#C49533',
            duration: 350,
            easing: 'easeOutElastic(1, .8)'
          });
        });
        node.addEventListener('mouseleave', () => {
          anime({
            targets: node,
            scale: 1,
            borderColor: '#A57A22',
            duration: 250,
            easing: 'easeOutQuad'
          });
        });
      });
    }
  }
});
