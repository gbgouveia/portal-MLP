import type { TiltedGridImage } from "@/components/ui/tilted-grid-hero";

export const resolveUrl = (path: string): string => {
  if (typeof window === "undefined") return path;
  const base = (window as any).MLP_BASE_PATH || (window.location.pathname.startsWith("/portal-MLP") ? "/portal-MLP" : "");
  const staticPrefix = "/static";
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  const fullPath = cleanPath.startsWith(staticPrefix) ? cleanPath : `${staticPrefix}${cleanPath}`;
  return `${base}${fullPath}`;
};

export const ministryImages: TiltedGridImage[] = [
  { src: resolveUrl("/images/ministerio/foto-01.webp"), alt: "Pastor Leonel pregando no púlpito" },
  { src: resolveUrl("/images/ministerio/foto-02.webp"), alt: "Congregação e coro reunidos no templo" },
  { src: resolveUrl("/images/ministerio/foto-03.webp"), alt: "Pastor Leonel ministrando as Sagradas Escrituras" },
  { src: resolveUrl("/images/ministerio/foto-04.webp"), alt: "Culto de adoração solene e louvor diante da cruz" },
  { src: resolveUrl("/images/ministerio/foto-05.webp"), alt: "Pastor Leonel e liderança em comunhão ministerial" },
  { src: resolveUrl("/images/ministerio/foto-06.webp"), alt: "Registro histórico das primeiras reuniões nos anos 1970" },
  { src: resolveUrl("/images/ministerio/foto-07.webp"), alt: "Celebração comunitária da Santa Ceia do Senhor" },
  { src: resolveUrl("/images/ministerio/foto-08.webp"), alt: "Memória de edificação e crescimento do templo" },
  { src: resolveUrl("/images/ministerio/foto-09.webp"), alt: "Vigília de oração e intercessão congregacional" },
  { src: resolveUrl("/images/ministerio/foto-10.webp"), alt: "Famílias e gerações no Ministério Luz da Palavra" },
];
