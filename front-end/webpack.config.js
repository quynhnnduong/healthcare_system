const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development', // Set mode to 'development'
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/main.html', // Updated path to main.html
    }),
  ],
  devServer: {
    port: 8080,
    open: true, // Automatically open the browser
    proxy: [
      {
        context: ['/api'], // Proxy requests with '/api' prefix
        target: 'http://localhost:8000', // Target URL for proxying
      },
    ],
  },
};
