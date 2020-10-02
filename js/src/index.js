import Vue from 'vue';
import App from "./App"

new Vue({
  el: '#app',  
  components: { App }
});

new Vue({
  el: '#nav-app',
  data() {
    return {
      isActive: false
    }
  },

  methods: {
    toggleMenu: function(){
      this.isActive = !this.isActive
    },
  }
})
