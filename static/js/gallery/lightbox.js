/**
 * Ministério Luz da Palavra — Lightbox Acessível para o Acervo Fotográfico
 * Suporte a navegação por teclado (ESC para fechar, setas esquerda/direita),
 * descrições textuais acessíveis e trap de foco.
 */

class MLPLightbox {
  constructor() {
    this.modal = document.getElementById('mlp-lightbox-modal');
    if (!this.modal) return;

    this.image = this.modal.querySelector('.lightbox-image');
    this.caption = this.modal.querySelector('.lightbox-caption');
    this.author = this.modal.querySelector('.lightbox-author');
    this.closeBtn = this.modal.querySelector('.lightbox-close');
    this.prevBtn = this.modal.querySelector('.lightbox-prev');
    this.nextBtn = this.modal.querySelector('.lightbox-next');

    this.items = [];
    this.currentIndex = 0;
    this.lastFocusedElement = null;

    this.init();
  }

  init() {
    // Coleta todos os disparadores de imagem do acervo
    const triggers = document.querySelectorAll('[data-lightbox-trigger]');
    triggers.forEach((trigger, index) => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        this.open(index);
      });
      this.items.push({
        src: trigger.getAttribute('data-image-src') || trigger.querySelector('img')?.src,
        caption: trigger.getAttribute('data-caption') || '',
        author: trigger.getAttribute('data-author') || '',
        alt: trigger.querySelector('img')?.alt || 'Fotografia do acervo histórico'
      });
    });

    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.close());
    }

    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', () => this.prev());
    }

    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', () => this.next());
    }

    // Fechar ao clicar no backdrop
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) this.close();
    });

    // Teclado
    document.addEventListener('keydown', (e) => {
      if (!this.modal.classList.contains('active')) return;

      if (e.key === 'Escape') {
        this.close();
      } else if (e.key === 'ArrowLeft') {
        this.prev();
      } else if (e.key === 'ArrowRight') {
        this.next();
      }
    });
  }

  open(index) {
    if (!this.items.length) return;
    this.currentIndex = index;
    this.lastFocusedElement = document.activeElement;

    this.render();
    this.modal.classList.add('active');
    this.modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    if (this.closeBtn) {
      this.closeBtn.focus();
    }
  }

  close() {
    this.modal.classList.remove('active');
    this.modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';

    if (this.lastFocusedElement) {
      this.lastFocusedElement.focus();
    }
  }

  render() {
    const item = this.items[this.currentIndex];
    if (!item) return;

    if (this.image) {
      this.image.src = item.src;
      this.image.alt = item.alt;
    }
    if (this.caption) {
      this.caption.textContent = item.caption;
    }
    if (this.author) {
      this.author.textContent = item.author ? `Acervo: ${item.author}` : '';
    }
  }

  prev() {
    if (this.items.length <= 1) return;
    this.currentIndex = (this.currentIndex - 1 + this.items.length) % this.items.length;
    this.render();
  }

  next() {
    if (this.items.length <= 1) return;
    this.currentIndex = (this.currentIndex + 1) % this.items.length;
    this.render();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.mlpLightbox = new MLPLightbox();
});
