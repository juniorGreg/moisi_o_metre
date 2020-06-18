'use strict'



module.exports = function(env) {
  console.log('DEBUG: ', env.prod == 'true' ? 'production' : 'development')
  return {
    mode: env.prod == 'true' ? 'production' : 'development',
    stats: 'detailed',
    entry: {
      index: './index.js'
    },
    output: {
      filename: '../../static/js/bundle.js'
    },
    resolve: {
          alias: {
              'vue$': 'vue/dist/vue.esm.js'
          },
      },
    }

}
