module.exports = (grunt) ->
  
  # project configuration
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'
    uglify:
      my_target:
        files: 
          'application/static/application.min.js': ['application/static/application.js']

  # load the plugin that provides the uglify task
  grunt.loadNpmTasks 'grunt-contrib-uglify'

  # default tasks
  grunt.registerTask('default', ['uglify'])
