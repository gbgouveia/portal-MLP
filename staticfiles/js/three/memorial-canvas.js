/**
 * Ministério Luz da Palavra — Experiência Espacial Memorial (Three.js)
 * Atmosfera abstrata de tempo, memória e luz dourada.
 * Implementa:
 * - Respeito a prefers-reduced-motion
 * - Interrupção de render loop com IntersectionObserver quando fora de viewport
 * - Fallback gracioso sem bloqueio de conteúdo
 * - Limitação de partículas para performance móvel
 */

class MLPMemorialCanvas {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;

    // Se usuário tiver redução de movimento ativada ou WebGL não suportado, não inicia
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      this.container.style.display = 'none';
      return;
    }

    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.particles = null;
    this.animationFrameId = null;
    this.isVisible = false;

    this.init();
  }

  init() {
    // Verifica se Three.js está carregado no escopo global
    if (typeof THREE === 'undefined') {
      return;
    }

    const width = this.container.clientWidth || window.innerWidth;
    const height = this.container.clientHeight || 400;

    // 1. Cena e Câmera
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    this.camera.position.z = 120;

    // 2. Renderizador com limites de performance
    try {
      this.renderer = new THREE.WebGLRenderer({
        alpha: true,
        antialias: false,
        powerPreference: 'low-power'
      });
      this.renderer.setSize(width, height);
      this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
      this.container.appendChild(this.renderer.domElement);
    } catch (e) {
      console.warn('WebGL não suportado ou desabilitado, fallback silencioso.', e);
      return;
    }

    // 3. Sistema de Partículas Sutis (Memória e Feixe de Luz)
    const particleCount = window.innerWidth < 768 ? 120 : 280;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    // Paleta Dourado Histórico (#A57A22) e Marfim (#F7F2E9)
    const goldColor = new THREE.Color(0xA57A22);
    const ivoryColor = new THREE.Color(0xF7F2E9);

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 220;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 160;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 120;

      const mixed = Math.random() > 0.4 ? goldColor : ivoryColor;
      colors[i * 3] = mixed.r;
      colors[i * 3 + 1] = mixed.g;
      colors[i * 3 + 2] = mixed.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 2.2,
      vertexColors: true,
      transparent: true,
      opacity: 0.55,
      blending: THREE.AdditiveBlending
    });

    this.particles = new THREE.Points(geometry, material);
    this.scene.add(this.particles);

    // 4. Observador de Interseção para Pausa Eficiente de Recursos
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        this.isVisible = entry.isIntersecting;
        if (this.isVisible) {
          this.animate();
        } else {
          if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
          }
        }
      });
    }, { threshold: 0.1 });

    observer.observe(this.container);

    // 5. Redimensionamento Responsivo
    window.addEventListener('resize', () => this.onResize());
  }

  onResize() {
    if (!this.container || !this.renderer || !this.camera) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  animate() {
    if (!this.isVisible) return;

    if (this.particles) {
      this.particles.rotation.y += 0.0006;
      this.particles.rotation.x += 0.0003;
    }

    this.renderer.render(this.scene, this.camera);
    this.animationFrameId = requestAnimationFrame(() => this.animate());
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('memorial-three-canvas')) {
    window.mlpMemorialCanvas = new MLPMemorialCanvas('memorial-three-canvas');
  }
});
