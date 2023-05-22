const path = require('path')
const HTMLWebpackPlugin = require('html-webpack-plugin')
const {CleanWebpackPlugin} = require('clean-webpack-plugin')
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin")
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const TerserWebpackPlugin = require('terser-webpack-plugin')

const isDev = process.env.NODE_ENV === 'development'
const isProd = !isDev
console.log('is dev', isDev)


module.exports = {
  context: path.resolve(__dirname, './src'),
  mode: 'development',
  entry: {
    index: './scripts/index.js',
    gameboard: './scripts/gameboard.js',
    registration : './scripts/validation.js',
    players_list: './scripts/players_list.js'
  },
  output : {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'dist')
  },
  devServer: {
    port: 4200,
    hot: isDev
  },
  optimization : {
    minimizer: [ 
      new CssMinimizerPlugin(),
      new TerserWebpackPlugin()
    ],
    minimize: isProd
  },
  plugins: [
    new HTMLWebpackPlugin({
      filename: 'index.html',
      template: './index.html',
      chunks: ['index'],
      minify: {
        collapseWhitespace: isProd
      }
    }),
    new HTMLWebpackPlugin({
      filename: 'players_list.html',
      template: './pages/players_list.html',
      chunks: ['players_list'],
      minify: {
        collapseWhitespace: isProd
      }
    }),
    new HTMLWebpackPlugin({
      filename: 'gameboard.html',
      template: './pages/gameboard.html',
      chunks: ['gameboard'],
      minify: {
        collapseWhitespace: isProd
      }
    }),
    new HTMLWebpackPlugin({
      filename: 'registration.html',
      template: './pages/registration.html',
      chunks: ['registration'],
      minify: {
        collapseWhitespace: isProd
      }
      }),
      new CleanWebpackPlugin(),

      new MiniCssExtractPlugin({
        filename: '[name].[contenthash].css'
      }),

  ],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              
            },
          },
          'css-loader'
        ]
      }
  ]
}
}

