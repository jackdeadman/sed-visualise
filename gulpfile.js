var debug = process.env.NODE_ENV !== "production";
var gulp = require('gulp');
var gutil = require("gulp-util");
var webpack = require("webpack");
var webpackStream = require("webpack-stream");
var WebpackDevServer = require("webpack-dev-server");
// var sass = require('gulp-sass');
// var rename = require("gulp-rename");
// var livereload = require('gulp-livereload');
// var htmlreplace = require('gulp-html-replace');
var path = require('path');




gulp.task("webpack-dev-server", function(callback) {
  // Start a webpack-dev-server
  var config = require('./webpack.config.js');
  var compiler = webpack(config);
  console.log(config);
  new WebpackDevServer(compiler, {
    contentBase: "src",
    inline: true,
    hot: true
  })
  .listen(8080, "localhost", function(err) {
    if(err) throw new gutil.PluginError("webpack-dev-server", err);
    // Server listening
    gutil.log("[webpack-dev-server]", "http://localhost:8080/webpack-dev-server/index.html");

    // keep the server alive or continue?
    callback();
  });
});

gulp.task('compileJS', function() {
  process.env.NODE_ENV = "production";
  var config = require('./webpack.config.js');
  return gulp.src('src/client.js')
    .pipe(webpackStream(config))
    .pipe(gulp.dest('static/js'));
});

gulp.task('sass:watch', function() {
  livereload.listen();
  debug
    ? gulp.watch('src/css/**/*.sass', ['sass:debug'])
    : gulp.watch('src/css/**/*.sass', ['sass:production']);
});

gulp.task('webpack:watch', function() {
  gulp.watch('src/js/**/*.js', ['webpack']);
});

gulp.task('moveIndex', function() {
  return gulp.src('src/index.html').pipe(gulp.dest('dist'));
});

gulp.task('default', ['sass:debug', 'sass:watch', 'webpack-dev-server']);
gulp.task('build', ['sass:production', 'compileJS', 'moveIndex']);