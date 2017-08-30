const debug = process.env.NODE_ENV !== "production";
const webpack = require('webpack');
const path = require('path');

module.exports = {
  context: path.join(__dirname, "webapp_src"),
  devtool: debug ? "inline-sourcemap" : null,
  entry: "./js/client.js",
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        query: {
          presets: ['es2017', 'react'],
          plugins: ['react-html-attrs', 'transform-class-properties'],
        }
      }
    ]
  },
  output: {
    path: path.join(__dirname, "webapp_dist/js"),
    publicPath: '/js/',
    filename: "client.min.js"
  },
  plugins: debug ? [] :[
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
  ],
};
