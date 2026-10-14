"use client";

import React, { useMemo } from "react";
import { TiltedGridHero } from "@/components/ui/tilted-grid-hero";
import { ministryImages, resolveAssetUrl } from "@/src/hero-gallery-data";

export interface HeroSectionProps {
  pastorPortraitUrl?: string;
  homeUrl?: string;
  ministryUrl?: string;
  wordUrl?: string;
  galleryUrl?: string;
  contactUrl?: string;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  pastorPortraitUrl,
  homeUrl = "#",
  ministryUrl = "#",
  wordUrl = "#",
  galleryUrl = "#",
  contactUrl = "#",
}) => {
  // Retrato REAL do Pastor Leonel isolado em fundo transparente
  const portraitSrc = useMemo(() => {
    if (pastorPortraitUrl && !pastorPortraitUrl.includes("pastor-leonel-portrait.webp")) {
      return pastorPortraitUrl;
    }
    if (typeof window !== "undefined" && (window as any).MLP_PASTOR_PORTRAIT) {
      return (window as any).MLP_PASTOR_PORTRAIT;
    }
    return resolveAssetUrl("/static/images/hero/pastor-leonel-real.webp");
  }, [pastorPortraitUrl]);

  const handleScrollDown = () => {
    const nextSection = document.querySelector(".section-editorial, #next-section, main > section:nth-of-type(2)");
    if (nextSection) {
      nextSection.scrollIntoView({ behavior: "smooth" });
    } else {
      window.scrollBy({ top: window.innerHeight * 0.9, behavior: "smooth" });
    }
  };

  return (
    <section
      className="relative min-h-[100svh] w-full bg-[#080605] overflow-hidden flex flex-col justify-between"
      aria-label="Abertura Cinematográfica do Ministério Luz da Palavra"
    >
      {/* 1. Navegação Superior Integrada Fiel à Referência Visual */}
      <nav
        className="relative z-30 w-full pt-6 pb-2 px-6 flex justify-center items-center pointer-events-auto"
        aria-label="Navegação Principal da Hero"
      >
        <div className="flex items-center gap-6 sm:gap-10 md:gap-12 text-xs sm:text-sm font-sans tracking-widest text-[#F2F1F0]/75">
          <a
            href={homeUrl}
            className="relative text-[#F2D16D] font-medium transition-colors hover:text-[#F2D16D] pb-1"
          >
            Início
            <span
              className="absolute bottom-0 left-0 right-0 h-[2px] bg-[#F2D16D] rounded-full shadow-[0_0_8px_#F2D16D]"
              aria-hidden="true"
            />
          </a>

          <a
            href={ministryUrl}
            className="transition-colors hover:text-[#F2D16D]"
          >
            Ministério
          </a>

          <a
            href={wordUrl}
            className="transition-colors hover:text-[#F2D16D]"
          >
            Palavra
          </a>

          <a
            href={galleryUrl}
            className="transition-colors hover:text-[#F2D16D]"
          >
            Galeria
          </a>

          <a
            href={contactUrl}
            className="transition-colors hover:text-[#F2D16D]"
          >
            Contato
          </a>
        </div>
      </nav>

      {/* 2. Galeria Orbital 3D Curva com TiltedGridHero */}
      <TiltedGridHero
        images={ministryImages}
        speed={4.5}
        tileHeight={27}
        aspectRatio={1.55}
        gap={8}
        axis={46}
        curve={74}
        fade={10}
        className="min-h-[100svh] w-full bg-[#080605] absolute inset-0"
      >
        {/* Halo Radiante Dourado / Backlight do Pastor */}
        <div
          className="pointer-events-none absolute inset-0 z-5 flex items-center justify-center"
          aria-hidden="true"
        >
          <div
            className="w-[480px] h-[480px] sm:w-[620px] sm:h-[620px] rounded-full blur-[85px] opacity-60 mix-blend-screen"
            style={{
              background:
                "radial-gradient(circle, rgba(242, 209, 109, 0.45) 0%, rgba(191, 135, 31, 0.28) 42%, rgba(140, 67, 3, 0.1) 70%, transparent 85%)",
            }}
          />
        </div>

        {/* 3. Retrato Real do Pastor Leonel (Centralizado em Primeiro Plano) */}
        <div
          className="relative z-15 flex flex-col items-center justify-center pointer-events-none mt-2 sm:mt-0"
          style={{ transform: "translateZ(50px)" }}
        >
          <div className="relative">
            {/* Brilho de recorte e halo suave no contorno do pastor */}
            <div
              className="absolute -inset-2 rounded-full opacity-60 blur-xl pointer-events-none"
              style={{
                background:
                  "radial-gradient(circle at 50% 25%, rgba(242, 209, 109, 0.45) 0%, rgba(191, 135, 31, 0.2) 50%, transparent 75%)",
              }}
            />

            <img
              src={portraitSrc}
              alt="Pastor Leonel — Ministério Luz da Palavra"
              className="relative w-[300px] sm:w-[380px] md:w-[440px] lg:w-[480px] max-h-[60vh] sm:max-h-[64vh] h-auto object-contain filter drop-shadow-[0_22px_45px_rgba(0,0,0,0.95)]"
              draggable={false}
              loading="eager"
            />
          </div>
        </div>

        {/* 4. Tipografia Institucional Fiel à Referência Visual */}
        <div
          className="relative z-25 flex flex-col items-center text-center px-4 max-w-4xl mx-auto -mt-16 sm:-mt-20 md:-mt-24 pointer-events-auto"
          style={{ transform: "translateZ(80px)" }}
        >
          {/* M I N I S T É R I O */}
          <span
            className="text-[0.72rem] sm:text-xs md:text-sm uppercase font-light text-[#F2F1F0]/90 drop-shadow-md mb-1 sm:mb-2"
            style={{ letterSpacing: "0.45em" }}
          >
            M I N I S T É R I O
          </span>

          {/* Luz da Palavra (Dourado majestoso editorial com serifa Cinzel) */}
          <h1
            className="text-4xl sm:text-6xl md:text-7xl lg:text-[5.4rem] font-normal tracking-tight text-transparent bg-clip-text drop-shadow-[0_8px_30px_rgba(0,0,0,0.95)] leading-tight my-1 sm:my-2"
            style={{
              fontFamily: "'Cinzel', Georgia, serif",
              backgroundImage:
                "linear-gradient(180deg, #FFF8DE 0%, #F5D77F 40%, #BF871F 80%, #8C4303 100%)",
            }}
          >
            Luz da Palavra
          </h1>

          {/* — Pastor Leonel — (Script cursivo com linhas finas douradas nas laterais) */}
          <div className="flex items-center justify-center gap-3 sm:gap-6 w-full my-1 sm:my-2">
            <span
              className="h-[1px] w-14 sm:w-28 md:w-40 bg-gradient-to-r from-transparent via-[#BF871F] to-[#F2D16D]"
              aria-hidden="true"
            />
            <span
              className="text-2xl sm:text-3xl md:text-4xl text-[#F2D16D] italic tracking-wide drop-shadow-lg"
              style={{ fontFamily: "'Playfair Display', cursive" }}
            >
              Pastor Leonel
            </span>
            <span
              className="h-[1px] w-14 sm:w-28 md:w-40 bg-gradient-to-l from-transparent via-[#BF871F] to-[#F2D16D]"
              aria-hidden="true"
            />
          </div>

          {/* 5. Botão Circular de Rolagem (Chevron Down como na Referência) */}
          <button
            onClick={handleScrollDown}
            className="mt-6 sm:mt-8 w-9 h-9 sm:w-10 sm:h-10 rounded-full border border-[#F2D16D]/60 flex items-center justify-center text-[#F2D16D] transition-all duration-300 hover:border-[#F2D16D] hover:scale-110 hover:shadow-[0_0_15px_rgba(242,209,109,0.5)] focus:outline-none focus:ring-2 focus:ring-[#F2D16D]/50 cursor-pointer"
            aria-label="Rolar para o conteúdo"
          >
            <svg
              className="w-4 h-4 sm:w-5 sm:h-5 transform transition-transform group-hover:translate-y-0.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>
        </div>
      </TiltedGridHero>
    </section>
  );
};

export default HeroSection;
