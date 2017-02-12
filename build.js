/**
 * Created by tomek on 12/10/16.
 */
var compressor = require('node-minify');

var mimficator = 'uglifyjs';
if (process.argv[2] !== 'production') {
  mimficator = 'no-compress';
}

console.log(process.argv[2], 'Using ' + mimficator);

new compressor.minify({
  compressor: mimficator,
  input: [
    'node_modules/jquery/dist/jquery.js',
    'node_modules/vue/dist/vue.js',
    'node_modules/bootstrap/dist/js/bootstrap.js',
    'core/assets/js/main.js',
  ],
  output: 'core/static/core/js/build.min.js',
  callback: function (err, min) {
    if (err) {
      console.error(err);
    }
    //console.log(min);
    console.log('Done js');
  }
});

new compressor.minify({
  compressor: 'clean-css',
  input: [
    'node_modules/bootstrap/dist/css/bootstrap.css',
    'node_modules/bootstrap/dist/css/bootstrap-theme.css',
    'core/assets/css/main.css',
  ],
  output: 'core/static/core/css/build.min.css',
  callback: function (err, min) {
    if (err) {
      console.error(err);
    }
    //console.log(min);
    console.log('Done css');
  }
});