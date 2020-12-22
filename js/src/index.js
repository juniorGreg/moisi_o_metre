import "./mystyles.scss";

import Vue from 'vue';
import App from "./App";
import AppBull from "./AppBull";
import AppBullLabel from "./AppBullLabel";
import AppQuiz  from "./AppQuiz";
import SearchBar from "./components/SearchBar.vue";
import Snows from './components/Snows.vue';

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
    components: { SearchBar , Snows },
    data(){
      return {
        isActive: false
      }
    },

    computed: {
      ...mapState([
        "post_ids",
        "dark_mode",
        "is_snowing"
      ]),
      showLoupe: function(){
        return this.post_ids.length > 0
      }
    },

    methods: {
      ...mapActions([
        "toggleSearchBar",
        "getDarkMode",
        "isSnowing"
      ]),
      ...mapMutations([
        "SET_DARK_MODE"
      ]),
      toggleMenu: function(){
        this.isActive = !this.isActive
      },
      toggleDarkMode: function(){
        var mode = !this.dark_mode;
        this.SET_DARK_MODE(mode);
        this.isActive = false;
      }

    },

    created: function(){
        this.getDarkMode();
    },

    mounted: function(){
      setTimeout(() => {
        console.log("preload")
        document.documentElement.classList.remove("preload");
      }, 1000);

      this.isSnowing();
    },

    watch: {
      dark_mode: function(){

        var mainSection = document.getElementById("main-section");


        if(this.dark_mode){
            mainSection.classList.add("dark-mode");
            document.documentElement.classList.add("dark-mode-html");
            //document.body.c
        }else{
          mainSection.classList.remove("dark-mode");
          document.documentElement.classList.remove("dark-mode-html");
        }



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
