import "./mystyles.scss";

import Vue from 'vue';
import App from "./App";
import AppBull from "./AppBull";
import AppBullLabel from "./AppBullLabel";
import AppQuiz  from "./AppQuiz";
import SearchBar from "./components/SearchBar.vue";
import store from "./store";

var app = document.getElementById("app");
var appbull = document.getElementById("app-bull");
var appbulllabel = document.getElementById("app-bull-label");
var appquiz = document.getElementById("app-quiz");
var navapp = document.getElementById("nav-app");

import { mapState , mapMutations , mapActions } from 'vuex';





if(app){
  new Vue({
    store: store,
    el: '#app',
    components: { App }
  });
}

if(navapp)
{
  new Vue({
    el: '#nav-app',
    store: store,
    components: { SearchBar },
    data(){
      return {
        isActive: false
      }
    },

    computed: {
      ...mapState([
        "post_ids"
      ]),
      showLoupe: function(){
        return this.post_ids.length > 0
      }
    },

    methods: {
      ...mapActions([
        "toggleSearchBar"
      ]),
      toggleMenu: function(){
        this.isActive = !this.isActive
      }

    }
  });
}

if(appbull){
  new Vue({
    el: '#app-bull',
    components: { AppBull }
  });
}

if(appbulllabel){
  new Vue({
    el: '#app-bull-label',
    components: { AppBull, AppBullLabel }
  });
}

if(appquiz){
  new Vue({
    el: "#app-quiz",
    components: {AppQuiz},
  })
}
