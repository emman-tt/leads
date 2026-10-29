import type { NextConfig } from "next";

// Bundler: Webpack (opt-in via `--webpack` on dev/build scripts).
// CSS: Tailwind v4 through PostCSS (`postcss.config.mjs` -> @tailwindcss/postcss).
// Demo build: the one verified client photo (200x200 page avatar) is
// hotlinked; everything else is type, rules and CSS gradients by design.
const nextConfig: NextConfig = {
  images: { unoptimized: true },
};

export default nextConfig;
