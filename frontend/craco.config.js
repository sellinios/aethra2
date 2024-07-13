module.exports = {
  // Add any custom configuration here
  webpack: {
    // Example of adding custom configuration to webpack
    configure: {
      // Custom Webpack configuration
    },
  },
  devServer: {
    // Example of customizing the development server configuration
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  babel: {
    // Example of customizing Babel configuration
    plugins: [
      // Custom Babel plugins
    ],
  },
};