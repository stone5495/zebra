/**
 * Created by sun on 2015/6/6.
 */
/* jshint ignore:start */

var assets = {};
function addAssets(kv, base) {
  Object.keys(kv).forEach(function(name) {
    if (/\.js$/.test(name) || /\.css$/.test(name)) {
      assets['assets/' + name] = base + kv[name];
    } else {
      assets['assets/' + name] = base + kv[name];
    }
  });
}

var cdnjs = {
  'js/jquery.js': 'jquery/2.0.3/jquery.js',
  //'js/jquery.gridster.js': 'jquery.gridster/0.5.4/jquery.gridster.js',
  //'css/jquery.gridster.css': 'jquery.gridster/0.5.4/jquery.gridster.css',

  'css/font-awesome.css': 'font-awesome/4.2.0/css/font-awesome.css',
  'fonts/FontAwesome.otf': 'font-awesome/4.2.0/fonts/FontAwesome.otf',
  'fonts/fontawesome-webfont.eot': 'font-awesome/4.2.0/fonts/fontawesome-webfont.eot',
  'fonts/fontawesome-webfont.svg': 'font-awesome/4.2.0/fonts/fontawesome-webfont.svg',
  'fonts/fontawesome-webfont.ttf': 'font-awesome/4.2.0/fonts/fontawesome-webfont.ttf',
  'fonts/fontawesome-webfont.woff': 'font-awesome/4.2.0/fonts/fontawesome-webfont.woff',

  'js/URI.min.js': 'URI.js/1.11.2/URI.min.js',
  'js/angular.js': 'angular.js/1.3.8/angular.js',
  "js/angular-sanitize.js": "angular.js/1.3.8/angular-sanitize.js",
  "js/angular-route.js": "angular.js/1.3.8/angular-route.js",

  'js/bootstrap.js': 'twitter-bootstrap/3.1.1/js/bootstrap.js',
  'css/bootstrap.css': 'twitter-bootstrap/3.1.1/css/bootstrap.css',
  'js/bootstrap-switch.js': 'bootstrap-switch/2.0.0/js/bootstrap-switch.js',
  //'js/topojson.min.js': 'topojson/1.1.0/topojson.min.js',
  //'js/bootstrap-datepicker.min.js': 'bootstrap-datepicker/1.3.0/js/bootstrap-datepicker.min.js',
  //'js/bootstrap-datepicker.zh-CN.min.js': 'bootstrap-datepicker/1.3.0/js/locales/bootstrap-datepicker.zh-CN.min.js',
  //'css/datepicker3.min.css': 'bootstrap-datepicker/1.3.0/css/datepicker3.min.css',
  //'js/d3.js': 'd3/3.4.3/d3.js',
  'css/material.css': 'materialize/0.96.1/css/materialize.min.css',
  'js/material.js': 'materialize/0.96.1/js/materialize.min.js'
};
addAssets(cdnjs, 'http://cdnjs.cloudflare.com/ajax/libs/');


/*var echarts = {
  'js/echarts.js': 'build/dist/echarts-all.js'
};
addAssets(echarts, "http://echarts.baidu.com/");*/

var flatui = {
  'js/bootstrap-select.js': '2.1.3/js/bootstrap-select.js',
  'js/jquery.tagsinput.js': '2.1.3/js/jquery.tagsinput.js',
  'css/flat-ui.css': '2.1.3/css/flat-ui.css',
  'images/switch/mask.png': '2.1.3/images/switch/mask.png',
  'fonts/flat-ui-icons-regular.eot': '2.1.3/fonts/flat-ui-icons-regular.eot',
  'fonts/flat-ui-icons-regular.svg': '2.1.3/fonts/flat-ui-icons-regular.svg',
  'fonts/flat-ui-icons-regular.ttf': '2.1.3/fonts/flat-ui-icons-regular.ttf',
  'fonts/flat-ui-icons-regular.woff': '2.1.3/fonts/flat-ui-icons-regular.woff'
};
addAssets(flatui, 'http://rawgithub.com/designmodo/Flat-UI/');


var bootstrap_table = {
  'css/bootstrap-table.css': 'wenzhixin/bootstrap-table/master/dist/bootstrap-table.css',
  'js/bootstrap-table.js': 'wenzhixin/bootstrap-table/master/dist/bootstrap-table.js'
};
addAssets(bootstrap_table, 'https://cdn.rawgit.com/');

module.exports = function(grunt) {

  grunt.initConfig({
    concat: {
      appjs: {
        src: ['app.js', 'utils.js', 'controllers/*', 'directives/*', 'services/*'].map(function(name) {
          return 'assets/js/' + name;
        }),
        dest: 'static/js/app.js'
      },
      appcss: {
        src: ['assets/css/*.css'],
        dest: 'static/css/app.css'
      },
      vendorjs: {
        src: Object.keys(assets).filter(function(name) {
          return /\.js$/.test(name);
        }),
        dest: 'static/js/vendor.js'
      },
      vendorcss: {
        src: Object.keys(assets).filter(function(name) {
          return /\.css$/.test(name);
        }),
        dest: 'static/css/vendor.css'
      }
    },
    uglify: {
      app: {
        src: 'static/js/app.js',
        dest: 'static/js/app.js'
      },
      vendor: {
        src: 'static/js/vendor.js',
        dest: 'static/js/vendor.js'
      }
    },
    cssmin: {
      app: {
        src: 'static/css/app.css',
        dest: 'static/css/app.css'
      },
      vendor: {
        src: 'static/css/vendor.css',
        dest: 'static/css/vendor.css'
      }
    },
    watch: {
      js: {
        files: ['assets/js/**/*.js'],
        tasks: ['concat:appjs']
      },
      css: {
        files: ['assets/css/**/*.js'],
        tasks: ['concat:appcss']
      }
    },
    curl: assets
  });

  grunt.loadNpmTasks('grunt-curl');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('build', ['concat', 'uglify', 'cssmin']);
  grunt.registerTask('init', ['curl', 'build']);
  grunt.registerTask('default', ['build']);
  grunt.registerTask('concat', ['concat']);

};
