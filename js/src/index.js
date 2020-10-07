import "./mystyles.scss";

import Vue from 'vue';
import App from "./App";
import AppBull from "./AppBull";
import AppBullLabel from "./AppBullLabel";
import AppQuiz  from "./AppQuiz";

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
});

new Vue({
  el: '#app-bull',
  components: { AppBull }
});

new Vue({
  el: '#app-bull-label',
  components: { AppBull, AppBullLabel }
});

new Vue({
  el: "#app-quiz",
  components: {AppQuiz},

})
