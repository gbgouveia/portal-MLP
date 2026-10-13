/**
 * Ministério Luz da Palavra — Linha do Tempo Histórica Interativa
 * Filtragem por décadas, expansão documental e acessibilidade por teclado.
 */

document.addEventListener('DOMContentLoaded', () => {
  const decadeButtons = document.querySelectorAll('.decade-filter-btn');
  const milestoneItems = document.querySelectorAll('.timeline-item');

  // 1. Filtragem por Décadas
  if (decadeButtons.length && milestoneItems.length) {
    decadeButtons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const selectedDecade = btn.getAttribute('data-decade');

        decadeButtons.forEach((b) => {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');

        milestoneItems.forEach((item) => {
          const itemDecade = item.getAttribute('data-decade');
          if (selectedDecade === 'all' || itemDecade === selectedDecade) {
            item.style.display = 'flex';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });
  }

  // 2. Expansão de Detalhes Históricos (Accordion Acessível)
  const detailToggles = document.querySelectorAll('.milestone-expand-btn');
  detailToggles.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const detailsBody = document.getElementById(targetId);
      if (!detailsBody) return;

      const isExpanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', !isExpanded);
      btn.textContent = isExpanded ? 'Ver Contexto Histórico Completo' : 'Ocultar Contexto Detalhado';

      if (isExpanded) {
        detailsBody.style.maxHeight = '0px';
        detailsBody.style.opacity = '0';
        detailsBody.setAttribute('aria-hidden', 'true');
      } else {
        detailsBody.style.maxHeight = detailsBody.scrollHeight + 'px';
        detailsBody.style.opacity = '1';
        detailsBody.setAttribute('aria-hidden', 'false');
      }
    });
  });
});
