<template lang="html">

    <div class="modal" :class="{'is-active': isvisible}">
        <div class="modal-background" @click="toggle"></div>
        <div class="modal-content">
          <article class="panel is-dark">
            <p class="panel-heading">
              Rechercher un article
            </p>
            <div class="panel-block">
              <p class="control">
                <input class="input is-small" type="text" placeholder="Rechercher un article" v-model="word">

              </p>
            </div>
            <a class="panel-block" v-for="post in posts" @click="getPost(post.id)">
              {{ post.title }}
            </a>

          </article>
        </div>

        <button class="modal-close is-large" aria-label="close"  @click="toggle"></button>
    </div>

</template>

<script>

import axios from 'axios'

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  props: ['isvisible'],
  data() {
    return {
      posts: [],
      word: ""
    }
  },
  methods: {
      search: function(){
        if(this.word){
          axios.get("/search/"+this.word).then(
            response => {this.posts = response.data}
          )
        }else{
          this.posts = []
        }
      },

      getPost: function(id){
        this.$emit("searchedpostid", id)
        this.toggle();
      },

      toggle: function(){
        //this.isvisible = !this.isvisible
        this.$emit('update:isvisible', !this.isvisible)
      }
  },
  watch: {
    word: function(){
      this.search();
    }
  }

}
</script>

<style lang="css" scoped>
  .panel {
    background-color: white
  }
</style>
