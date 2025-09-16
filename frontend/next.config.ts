// frontend/next.config.ts
import type { NextConfig } from 'next';

const API_ORIGIN = process.env.API_ORIGIN || 'http://localhost:8000';

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: '/api/:path*', destination: `${API_ORIGIN}/:path*` },
    ];
  },
};

export default nextConfig;