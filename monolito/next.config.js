/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    async redirects() {
        return [
            {
                source: '/',
                destination: '/home.tsx',
                permanent: true
            }
        ]
    }
}

module.exports = nextConfig
