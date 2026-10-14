import React from "react";
import ReactDOM from "react-dom/client";
import { HeroMinisterio } from "./components/hero-ministerio";
import "./index.css";
import "./components/hero-ministerio.css";

// Auto-montagem do HeroMinisterio oficial no DOM do template Django
function mountHero() {
  const rootEl = document.getElementById("tilted-grid-hero-root");
  if (!rootEl) return;

  const portrait = rootEl.getAttribute("data-portrait") || undefined;
  const homeUrl = rootEl.getAttribute("data-home-url") || undefined;
  const ministryUrl = rootEl.getAttribute("data-ministry-url") || undefined;
  const wordUrl = rootEl.getAttribute("data-word-url") || undefined;
  const galleryUrl = rootEl.getAttribute("data-gallery-url") || undefined;
  const contactUrl = rootEl.getAttribute("data-contact-url") || undefined;

  const navItems = [
    { label: "Início", href: homeUrl || "/" },
    { label: "Ministério", href: ministryUrl || "/nossa-historia/" },
    { label: "Palavra", href: wordUrl || "/mensagens-e-ao-vivo/" },
    { label: "Galeria", href: galleryUrl || "/acervo-fotografico/" },
    { label: "Contato", href: contactUrl || "/contato-e-horarios/" },
  ];

  let orbitImages: { src: string; alt?: string }[] | undefined = undefined;
  const rawImages = rootEl.getAttribute("data-orbit-images");
  if (rawImages) {
    try {
      const parsed = JSON.parse(rawImages);
      if (Array.isArray(parsed) && parsed.length > 0) {
        orbitImages = parsed;
      }
    } catch (e) {
      console.warn("Nao foi possivel carregar data-orbit-images", e);
    }
  }

  ReactDOM.createRoot(rootEl).render(
    <React.StrictMode>
      <HeroMinisterio
        portraitSrc={portrait}
        navItems={navItems}
        activeHref={homeUrl || window.location.pathname}
        nextSectionId="next-section"
        images={orbitImages}
      />
    </React.StrictMode>
  );
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", mountHero);
} else {
  mountHero();
}

export { HeroMinisterio };
