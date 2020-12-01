import "./mystyles.scss";

import Vue from 'vue';
import App from "./App";
import AppBull from "./AppBull";
import AppBullLabel from "./AppBullLabel";
import AppQuiz  from "./AppQuiz";
import SearchBar from "./components/SearchBar.vue";

var app = document.getElementById("app");
var appbull = document.getElementById("app-bull");
var appbulllabel = document.getElementById("app-bull-label");
var appquiz = document.getElementById("app-quiz");
var navapp = document.getElementById("nav-app");

var store = {

    searchedPostId: -1

}

var index = false;


if(app){
  new Vue({
    el: '#app',
    data() {
      return store
    },
    components: { App }
  });
  index = true;
}

if(navapp)
{
  new Vue({
    el: '#nav-app',

    components: { SearchBar },
    data() {
      return {
        index: index,
        isActive: false,
        isSearchBarVisible: false
      }
    },

    methods: {
      toggleMenu: function(){
        this.isActive = !this.isActive
      },
      showSearchBar: function(){
        this.isSearchBarVisible = !this.isSearchBarVisible
      },

      getSearchedPost: function(id){
        //console.log("emit id:"+id);
        store.searchedPostId = id;
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
