<template lang="html">
  <div>
    <div class="pageloader is-black" :class="{'is-active': is_loading}"><span class="title">Un momento, por favor</span></div>
    <snows v-if="is_snowing" :snowflake_img="snow_img_url"></snows>
    <nav class="navbar is-fixed-top is-transparent" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
            <a class="navbar-item banner" :href="index_href">
              <img :src="moisibanner_img">
            </a>


              <a  v-if="showLoupe" class="navbar-item" role="button" @click="showSearchBar">
                <img :src="loupe_img_src" alt="loupe de recherche">
              </a>

              <a  v-if="is_store" class="navbar-item" role="button" @click="showBasketModal">
                 <span title="Badge right" class="badge is-right is-danger">{{ basket_items_count }}</span>
                 <img :src="basket_img_src" alt="panier d'achats">
              </a>



            <a role="button" :class="{'is-active': isActive}" @click="toggleMenu()" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasic">
             <span aria-hidden="true"></span>
             <span aria-hidden="true"></span>
             <span aria-hidden="true"></span>
           </a>
        </div>


        <div :class="{'is-active': isActive}" id="navbarBasic" class="navbar-menu">
          <div class="navbar-end is-size-7">
            <a class="navbar-item" :href="bullshit_href">B*llshit O Mètre</a>
            <a class="navbar-item" :href="quiz_href">Jeux et Quiz</a>
            <a class="navbar-item" :href="references_href">Références</a>
            <a class="navbar-item" :href="about_href">À propos</a>
            <a class="navbar-item" :href="contact_href">Contact</a>
            <a class="navbar-item" :href="support_href">Supportez le blog</a>
            <a  class="navbar-item" :href="store_index_href" ><span ref="storeButton" style="display: inline-block;">Boutique</span></a>
            <a class="navbar-item" role="button" @click="toggleDarkMode">
              <img :src="dark_mode_icon_src" alt="icon mode sombre">
            </a>
          </div>
        </div>
      </div>
    </nav>
    <div v-if="showLoupe">
        <search-bar />
    </div>
  </div>

</template>

<script>
import { mapState , mapMutations , mapActions, mapGetters } from 'vuex';

import SearchBar from "./components/SearchBar.vue";
import Snows from './components/Snows.vue';

import anime from 'animejs/lib/anime.es.js';

export default {

  components: { SearchBar , Snows },
  data(){
    return {
      isActive: false,
    }
  },

  props: ['loupe_img_src',
          'snow_img_url',
          'moisibanner_img',
          'basket_img_src',
          'dark_mode_icon_src',
          'index_href',
          'bullshit_href',
          'quiz_href',
          'references_href',
          'about_href',
          'contact_href',
          'support_href',
          'store_index_href'
        ],

  computed: {
    ...mapState([
      "post_ids",
      "dark_mode",
      "is_snowing",
      "is_store",
      'is_basket_visible',
      'is_loading'
    ]),
    ...mapGetters([
      "basket_items_count"
    ]),

    showLoupe: function(){
      return this.post_ids.length > 0
    }
  },

  methods: {
    ...mapActions([
      "showSearchBar",
      "getDarkMode",
      "isSnowing",
      'showBasketModal'
    ]),
    ...mapMutations([
      "SET_DARK_MODE",
      "SET_IS_LOADING"
    ]),
    toggleMenu: function(){
      this.isActive = !this.isActive
      if(this.isActive && !this.is_store){
        setTimeout(this.initAnimStoreButton, 500)
      }
    },
    toggleDarkMode: function(){
      var mode = !this.dark_mode;
      this.SET_DARK_MODE(mode);
      this.isActive = false;
    },

    initAnimStoreButton: function(){
      console.log("ok")
      anime({
        targets: this.$refs.storeButton,
        loop: 2,
        direction: "alternate",
        easing: "linear",
        color: "rgb(255,100,100)",
        scale: [1.0, 2.3],
        //'text-shadow': ["0 0 0 #000","0 0 300px #FFF"],
        duration: 1000

      })
    }

  },

  created: function(){
      this.getDarkMode();

  },

  mounted: function(){

    this.isSnowing();
    setTimeout(() => {this.SET_IS_LOADING(false)}, 1000)
    setTimeout(() => {
      if(!this.is_store){
        setTimeout(this.initAnimStoreButton, 2000)
        setTimeout(this.initAnimStoreButton, 30000)
      }
    }, 1000)
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

}
</script>

<style lang="css" scoped>
</style>
