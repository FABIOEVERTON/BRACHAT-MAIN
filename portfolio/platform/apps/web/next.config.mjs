/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Cloudflare Pages (E0-S10-homepage): site 100% estático
  images: { unoptimized: true },
  transpilePackages: ['@ezra/types', '@ezra/ui', '@ezra/api-contracts', '@ezra/crypto'],
};

export default nextConfig;