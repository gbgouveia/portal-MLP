import type { TiltedGridImage } from "@/components/ui/tilted-grid-hero";

/**
 * Obtém URL resolvida considerando o subcaminho do GitHub Pages (ex: /portal-MLP/)
 */
export const resolveAssetUrl = (relativePath: string): string => {
  if (typeof window === "undefined") return relativePath;
  const path = relativePath.startsWith("/") ? relativePath : `/${relativePath}`;

  const customBase = (window as any).MLP_BASE_PATH;
  if (typeof customBase === "string" && customBase.length > 0) {
    const cleanBase = customBase.endsWith("/") ? customBase.slice(0, -1) : customBase;
    return `${cleanBase}${path}`;
  }

  if (window.location.pathname.startsWith("/portal-MLP")) {
    return `/portal-MLP${path}`;
  }

  return path;
};

/**
 * Coleção de registros fotográficos autênticos da referência visual do ministério
 */
export const ministryImages: TiltedGridImage[] = [
  {
    src: resolveAssetUrl("/static/images/hero/foto-pulpito-jovem.webp"),
    alt: "Pastor Leonel pregando no púlpito nos primeiros anos do ministério",
  },
  {
    src: resolveAssetUrl("/static/images/hero/foto-congregacao-salao.webp"),
    alt: "Congregação e coro reunidos no templo",
  },
  {
    src: resolveAssetUrl("/static/images/hero/foto-pregacao-pastor.webp"),
    alt: "Pastor Leonel ministrando com as Sagradas Escrituras",
  },
  {
    src: resolveAssetUrl("/static/images/hero/foto-adoracao-cruz.webp"),
    alt: "Momento solene de louvor e adoração diante da cruz",
  },
  {
    src: resolveAssetUrl("/static/images/hero/foto-casal-pastoral.webp"),
    alt: "Pastor Leonel e liderança pastoral em comunhão",
  },
  {
    src: resolveAssetUrl("/static/images/hero/culto-historico-1970.webp"),
    alt: "Arquivo histórico das primeiras reuniões de fé",
  },
  {
    src: resolveAssetUrl("/static/images/hero/ceia-senhor-memorial.webp"),
    alt: "Celebração comunitária da Ceia do Senhor",
  },
  {
    src: resolveAssetUrl("/static/images/hero/edificacao-templo.webp"),
    alt: "Registro de edificação e crescimento do templo",
  },
];
