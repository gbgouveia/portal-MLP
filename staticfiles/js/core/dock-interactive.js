/**
 * Ministério Luz da Palavra — Mac OS Dock Interativo
 * Baseado na referência 21st.dev (mac-os-dock.tsx) adaptado para Vanilla JS
 * Funcionalidades:
 * - Física de proximidade harmônica (magnification)
 * - Suporte a teclado completo (Tab, Enter, Space)
 * - Tooltips acessíveis com role="tooltip"
 * - Fallback inteligente para toque (touch) e prefers-reduced-motion
 */

class MLPDock {
  constructor() {
    this.dock = document.querySelector('.mlp-dock');
    if (!this.dock) return;

    this.items = Array.from(this.dock.querySelectorAll('.mlp-dock-item'));
    if (!this.items.length) return;

    this.maxScale = 1.35;
    this.maxDistance = 120; // Raio de influência do cursor em pixels
    this.isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    this.init();
  }

  init() {
    // Em dispositivos puramente touch ou com redução de movimento, desativa a distorção física
    if (this.isTouch || this.reducedMotion) {
      return;
    }

    this.dock.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    this.dock.addEventListener('mouseleave', () => this.handleMouseLeave());

    // Suporte a foco via teclado
    this.items.forEach((item) => {
      item.addEventListener('focus', () => {
        item.style.transform = `scale(1.2) translateY(-4px)`;
      });
      item.addEventListener('blur', () => {
        item.style.transform = `scale(1) translateY(0)`;
      });
    });
  }

  handleMouseMove(e) {
    const mouseX = e.clientX;

    this.items.forEach((item) => {
      const rect = item.getBoundingClientRect();
      const itemCenterX = rect.left + rect.width / 2;
      const distance = Math.abs(mouseX - itemCenterX);

      if (distance < this.maxDistance) {
        // Interpolação suave cosseno entre 1.0 e maxScale
        const normalized = distance / this.maxDistance;
        const scale = 1 + (this.maxScale - 1) * Math.cos((normalized * Math.PI) / 2);
        const translateY = -((scale - 1) * 16);
        item.style.transform = `scale(${scale.toFixed(3)}) translateY(${translateY.toFixed(1)}px)`;
      } else {
        item.style.transform = 'scale(1) translateY(0)';
      }
    });
  }

  handleMouseLeave() {
    this.items.forEach((item) => {
      item.style.transform = 'scale(1) translateY(0)';
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.mlpDock = new MLPDock();
});
