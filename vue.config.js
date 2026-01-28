const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // Tell Vue CLI where to find the source files
  pages: {
    index: {
      entry: 'frontend/src/main.js',
      template: 'public/index.html',
      filename: 'index.html'
    }
  },
  
  // Configure webpack to resolve files from frontend/src
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'frontend/src')
      }
    }
  }
})