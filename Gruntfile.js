'use strict';

module.exports = function(grunt) {
  grunt.initConfig({
    concat: {
      options: {
        separator: ';',
        sourceMap: true
      },
      dist: {
        src: ['static/modules/**.js',
              'static/config/**.js',
              'static/directives/**.js',
              'static/services/**.js',
              'static/controllers/**.js'],
        dest: 'static/build/app.concat.js',
      },
    },
    uglify: {
      options: {
        mangle: false,
        sourceMap: true
      },
      my_target: {
        files: {
          'static/build/app.min.js': ['static/build/app.concat.js']
        }
      }
    },
    watch: {
      scripts: {
        files: ['static/controllers/**.js'],
        tasks: ['concat', 'uglify'],
        options: {
          spawn: false,
        },
      },
    },
  });

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-uglify');
};
