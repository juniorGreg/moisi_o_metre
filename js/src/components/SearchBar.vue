<template lang="html">

    <section class="modal is-active" :style="{ 'opacity': opacity , 'pointer-events': pointer_events }" >
        <div class="modal-background" @click="hideSearchBar"></div>
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

        <button :style="{'pointer-events': pointer_events}" class="modal-close is-large" aria-label="close"  @click="hideSearchBar"></button>
    </section>

</template>

<script>


import { mapState , mapMutations , mapActions } from 'vuex';


export default {


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
        'is_search_bar_visible',
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
      },

      opacity: function(){
        if(this.is_search_bar_visible){
          return 1.0
        }else{
          return 0.0
        }
      },
      pointer_events: function(){
        if(this.is_search_bar_visible){
            return 'auto';
        }else {
          return 'none'
        }
      }


  },
  methods: {
      ...mapActions([
        'hideSearchBar',
        'fetchSearchedPosts',
        'getSearchedPost'
      ]),
  },
  watch: {
    searched_word: function(){
      this.fetchSearchedPosts();
    }
  },
  updated: function(){

    if(this.is_search_bar_visible){

        var searchBarInput = document.getElementById("searchBarInput");
        searchBarInput.focus();

    }
  }

}
</script>

<style lang="css" scoped>
  .modal {
    transition: opacity 1s;
  }

  .panel {
    background-color: white
  }
</style>
