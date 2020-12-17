<template lang="html">

    <div class="modal" :class="{'is-active': isSearchBarVisible}">
        <div class="modal-background" @click="toggleSearchBar"></div>
        <div class="modal-content">
          <article class="panel is-dark" :class="{'dark-mode': dark_mode}">
            <p class="panel-heading">
              Rechercher un article
            </p>
            <div class="panel-body">
              <div class="panel-block">
                <p class="control">
                  <input id="searchBarInput" class="input is-small" type="text" placeholder="Rechercher un article"
                  :value='searched_word'  @input='evt=>searched_word=evt.target.value'>

                </p>
              </div>
              <a class="panel-block" v-for="post in searched_posts" @click="getSearchedPost(post.id)">
                {{ post.title }}
              </a>
            </div>


          </article>
        </div>

        <button class="modal-close is-large" aria-label="close"  @click="toggleSearchBar"></button>
    </div>

</template>

<script>

import axios from 'axios'

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

import { mapState , mapMutations , mapActions } from 'vuex';


export default {
  emits: ['searchedpostidevent'],

  data() {
    return {
      posts: [],
      word: "",
      eventId: 0,
      currentId: -1
    }
  },
  computed: {
      ...mapState([
        'isSearchBarVisible',
        'searched_posts',
        'dark_mode'
      ]),

      searched_word: {
          get(){
            return this.$store.state.searched_word;
          },

          set(value){

            this.$store.commit("SET_SEARCHED_WORD", value)
          }
      }
  },
  methods: {
      ...mapActions([
        'toggleSearchBar',
        'fetchSearchedPosts',
        'getSearchedPost'
      ]),
  },
  watch: {
    searched_word: function(){
      this.fetchSearchedPosts();
    },
  },
  updated: function(){

    if(this.isSearchBarVisible){
        //console.log("updated");
        var searchBarInput = document.getElementById("searchBarInput");
        searchBarInput.focus();

    }else{
        //this.$emit("searchedpostidevent", 1);
    }
  }

}
</script>

<style lang="css" scoped>
  .panel {
    background-color: white
  }
</style>
