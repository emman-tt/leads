import type { NextConfig } from "next";

// Bundler: Webpack (opt-in via `--webpack` on dev/build scripts).
// CSS: Tailwind v4 through PostCSS (`postcss.config.mjs` -> @tailwindcss/postcss).
// Demo build: hotlinked vitalray.com photography, no optimizer pipeline needed.
const nextConfig: NextConfig = {
  images: { unoptimized: true },
};

export default nextConfig;
