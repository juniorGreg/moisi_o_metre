import "./mystyles.scss";

import Vue from 'vue';
import App from "./App";
import AppBull from "./AppBull";
import AppBullLabel from "./AppBullLabel";
import AppQuiz  from "./AppQuiz";

import AppStore from './AppStore';
import NavBar from './NavBar';

import store from "./store";

var app = document.getElementById("app");
var appbull = document.getElementById("app-bull");
var appbulllabel = document.getElementById("app-bull-label");
var appquiz = document.getElementById("app-quiz");
var navapp = document.getElementById("nav-app");
var appstore = document.getElementById("app-store")


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
    components: { NavBar }
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

if(appstore){
  new Vue({
    el: '#app-store',
    components: {AppStore},
    store: store
  })
}
