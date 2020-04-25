
var app = new Vue({
  el: '#app',

  data: {
    isActive: false
  },

  methods: {
      toggleMenu: function(){
        this.isActive = !this.isActive
      }
  }
})
