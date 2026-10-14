"use client";

import * as React from "react";
import { ChevronDown, Menu, X } from "lucide-react";
import { TiltedGridHero, type TiltedGridImage } from "@/components/ui/tilted-grid-hero";
import { ministryImages } from "@/data/ministry-images";
import "./hero-ministerio.css";

type NavItem = { label: string; href: string };

const getBase = () =>
  (typeof window !== "undefined" &&
    ((window as any).MLP_BASE_PATH ||
      (window.location.pathname.startsWith("/portal-MLP") ? "/portal-MLP" : ""))) ||
  "";

// Parâmetros da galeria por tamanho de tela.
const PRESETS = {
  small: { tileHeight: 22, aspectRatio: 1.3, gap: 6, axis: 44, curve: 62, fade: 14 },
  medium: { tileHeight: 26, aspectRatio: 1.5, gap: 6, axis: 46, curve: 68, fade: 12 },
  large: { tileHeight: 30, aspectRatio: 1.5, gap: 6, axis: 47, curve: 72, fade: 10 },
};

function useMedia(query: string) {
  const [matches, setMatches] = React.useState(false);
  React.useEffect(() => {
    const mq = window.matchMedia(query);
    const update = () => setMatches(mq.matches);
    update();
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, [query]);
  return matches;
}

export type HeroMinisterioProps = {
  /** Retrato real do Pastor Leonel (PNG/WebP com fundo transparente é o ideal). */
  portraitSrc?: string;
  navItems?: NavItem[];
  /** href do item ativo no menu. */
  activeHref?: string;
  /** id da seção seguinte, para a seta de rolagem. */
  nextSectionId?: string;
  /** Fotografias em órbita na galeria 3D configuradas no painel. */
  images?: TiltedGridImage[];
};

export function HeroMinisterio({
  portraitSrc,
  navItems,
  activeHref,
  nextSectionId = "next-section",
  images,
}: HeroMinisterioProps) {
  const base = getBase();
  const effectivePortrait = portraitSrc || `${base}/static/images/pastor-leonel.png`;
  const effectiveImages = images && images.length > 0 ? images : ministryImages;
  
  const effectiveNav: NavItem[] = navItems || [
    { label: "Início", href: `${base}/` },
    { label: "Ministério", href: `${base}/nossa-historia/` },
    { label: "Palavra", href: `${base}/mensagens-e-ao-vivo/` },
    { label: "Galeria", href: `${base}/acervo-fotografico/` },
    { label: "Contato", href: `${base}/contato-e-horarios/` },
  ];

  const effectiveActive = activeHref || `${base}/`;

  const isSmall = useMedia("(max-width: 639px)");
  const isMedium = useMedia("(max-width: 1023px)");
  const preset = isSmall ? PRESETS.small : isMedium ? PRESETS.medium : PRESETS.large;

  const [menuOpen, setMenuOpen] = React.useState(false);
  const [portraitOk, setPortraitOk] = React.useState(true);

  return (
    <section className="relative isolate bg-[#080605]">
      <TiltedGridHero
        images={effectiveImages}
        speed={4}
        {...preset}
        className="h-[100vh] h-[100svh] min-h-[560px] w-full bg-[#080605]"
      >
        {/* Fundo âmbar difuso */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 70% 40% at 50% 62%, rgba(140,67,3,.28), transparent 70%), radial-gradient(ellipse 90% 60% at 50% 110%, rgba(191,135,31,.14), transparent 70%)",
          }}
        />

        {/* Tom quente sobre a galeria (abaixo do retrato) */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 z-[5] mix-blend-color"
          style={{
            background:
              "linear-gradient(90deg, rgba(140,67,3,.55), rgba(140,67,3,.25) 50%, rgba(140,67,3,.55))",
          }}
        />

        {/* Halo dourado atrás do pastor */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 z-[6]"
          style={{
            background:
              "radial-gradient(ellipse 36% 46% at 50% 36%, rgba(242,209,109,.34), rgba(191,135,31,.13) 45%, transparent 72%)",
          }}
        />

        {/* Filete de luz dourada contornando a curva da galeria */}
        <div
          aria-hidden
          className="pointer-events-none absolute left-[2%] right-[2%] z-[6] rounded-[50%] border-b-2 border-[#F2D16D]/70 opacity-80"
          style={{
            top: `${preset.axis - 8}%`,
            height: "24%",
            boxShadow: "0 14px 24px -10px rgba(242,209,109,.55)",
            filter: "blur(.6px)",
          }}
        />

        {/* Retrato do pastor, à frente da galeria */}
        {portraitOk && (
          <div className="pointer-events-none absolute inset-x-0 top-[9%] z-10 flex h-[70%] justify-center">
            <img
              src={effectivePortrait}
              alt="Retrato do Pastor Leonel"
              onError={() => setPortraitOk(false)}
              className="h-full w-auto max-w-none select-none object-contain object-top"
              style={{
                WebkitMaskImage:
                  "linear-gradient(to bottom,#000 58%,transparent 100%)",
                maskImage: "linear-gradient(to bottom,#000 58%,transparent 100%)",
                filter:
                  "drop-shadow(0 0 28px rgba(242,209,109,.28)) contrast(1.05)",
              }}
              draggable={false}
            />
          </div>
        )}

        {/* Vinheta */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 z-[15]"
          style={{
            background:
              "radial-gradient(ellipse 85% 75% at 50% 45%, transparent 55%, rgba(8,6,5,.85) 100%), linear-gradient(to bottom, rgba(8,6,5,.55), transparent 18%, transparent 62%, rgba(8,6,5,.9) 100%)",
          }}
        />

        {/* Título */}
        <div className="absolute inset-x-0 bottom-[10%] z-20 flex flex-col items-center px-4 text-center">
          <span className="lp-sans text-[clamp(1.1rem,2.6vw,2.4rem)] font-light uppercase tracking-[.4em] sm:tracking-[.5em] pl-[.4em] sm:pl-[.5em] text-[#F2F1F0]">
            Ministério
          </span>
          <h1 className="lp-serif lp-gold-text mt-1 text-[clamp(2.6rem,9vw,8.5rem)] font-medium leading-[1.05] drop-shadow-[0_6px_30px_rgba(0,0,0,.6)]">
            Luz da Palavra
          </h1>
          <div className="mt-1 flex w-full max-w-[min(90vw,60rem)] items-center justify-center gap-4 sm:gap-8">
            <span aria-hidden className="hidden h-px flex-1 bg-gradient-to-r from-transparent to-[#F2D16D]/80 sm:block" />
            <span className="lp-script lp-gold-text text-[clamp(1.9rem,4.6vw,4.2rem)] leading-tight">
              Pastor Leonel
            </span>
            <span aria-hidden className="hidden h-px flex-1 bg-gradient-to-l from-transparent to-[#F2D16D]/80 sm:block" />
          </div>
        </div>

        {/* Seta de rolagem */}
        <a
          href={`#${nextSectionId}`}
          onClick={(e) => {
            const el =
              document.getElementById(nextSectionId) ||
              document.querySelector(".section-editorial") ||
              document.getElementById("main-content");
            if (el) {
              e.preventDefault();
              el.scrollIntoView({ behavior: "smooth" });
            }
          }}
          aria-label="Rolar para a próxima seção"
          className="lp-focus absolute bottom-[2.5%] left-1/2 z-20 flex h-9 w-9 -translate-x-1/2 items-center justify-center rounded-full border border-[#F2D16D]/80 text-[#F2D16D] transition hover:bg-[#F2D16D]/10"
        >
          <ChevronDown className="h-5 w-5" />
        </a>

        {/* Cabeçalho */}
        <header className="absolute inset-x-0 top-0 z-30">
          <nav
            aria-label="Principal"
            className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5 md:justify-center"
          >
            <ul className="lp-sans hidden items-center gap-10 text-[.95rem] tracking-wide text-[#F2F1F0] md:flex lg:gap-14">
              {effectiveNav.map((item) => {
                const active = item.href === effectiveActive;
                return (
                  <li key={item.href} className="relative">
                    <a
                      href={item.href}
                      aria-current={active ? "page" : undefined}
                      className={`lp-focus pb-2 transition-colors hover:text-[#F2D16D] ${active ? "text-[#F2D16D]" : ""}`}
                    >
                      {item.label}
                    </a>
                    {active && (
                      <span aria-hidden className="absolute inset-x-0 -bottom-0.5 h-px bg-[#F2D16D] shadow-[0_0_8px_#F2D16D]" />
                    )}
                  </li>
                );
              })}
            </ul>

            <button
              type="button"
              className="lp-focus ml-auto rounded-full p-2 text-[#F2F1F0] md:hidden"
              aria-expanded={menuOpen}
              aria-controls="menu-movel"
              aria-label={menuOpen ? "Fechar menu" : "Abrir menu"}
              onClick={() => setMenuOpen((o) => !o)}
            >
              {menuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </nav>

          {menuOpen && (
            <ul
              id="menu-movel"
              className="lp-sans mx-4 rounded-xl border border-[#F2D16D]/25 bg-[#080605]/95 p-3 text-[#F2F1F0] backdrop-blur md:hidden"
            >
              {effectiveNav.map((item) => {
                const active = item.href === effectiveActive;
                return (
                  <li key={item.href}>
                    <a
                      href={item.href}
                      aria-current={active ? "page" : undefined}
                      onClick={() => setMenuOpen(false)}
                      className={`lp-focus block rounded-lg px-4 py-3 ${active ? "text-[#F2D16D]" : "hover:text-[#F2D16D]"}`}
                    >
                      {item.label}
                    </a>
                  </li>
                );
              })}
            </ul>
          )}
        </header>
      </TiltedGridHero>
    </section>
  );
}

export default HeroMinisterio;
