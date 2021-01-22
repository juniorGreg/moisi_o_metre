
<template>
  <div class="container">
    <div class="posts" v-for="post in posts">
      <post :post="post"
           :local_url="local_url"
           :facebook_button_img="facebook_button_img"
           :twitter_button_img="twitter_button_img"
           :copy_link_button_img="copy_link_button_img"
           :support_href="support_href"
           :cursor_img="cursor_img"
           :spotify_img="spotify_img"
           :soundcloud_img="soundcloud_img"
           :itunes_img="itunes_img"
           :google_podcast_img="google_podcast_img">
      </post>
      <br>
    </div>
</template>


<script>
import Vue from 'vue'

import { mapState , mapMutations , mapActions } from 'vuex';

import Post from "./components/Post.vue"




export default {
  name: 'App',

  props: ['local_url', "facebook_button_img", "twitter_button_img", 'copy_link_button_img',
          "support_href", "cursor_img", "spotify_img", "itunes_img", "soundcloud_img",
          "google_podcast_img"],

  components: {
    Post
  },

  computed: {
    ...mapState([
      'posts',
      'post_ids',
      'post_index',
      'searched_post_active',
      'new_searched_post_active',
      'searched_post_id'
    ]),

  },

  methods: {
      ...mapMutations([
          'SET_POST_IDS',
          'SET_POST_INDEX',
          'SET_SEARCHED_POST_ACTIVE',
          'SET_NEW_SEARCHED_POST_ACTIVE'
      ]),

      ...mapActions([
        'getNextPost',
        "getCountryCode"
      ]),

     scrollToPost: function(){
        var postElement = document.getElementById(this.searched_post_id);
        if(postElement){
          var postRect = postElement.getBoundingClientRect();
          var scrollTop = postRect.top + window.scrollY - 50;

          window.scrollTo({ top: scrollTop, left: 0, behavior: 'smooth'});
        }
      },

      checkEndPost: function(ev){
        if ((window.innerHeight + window.scrollY + 50) >= document.body.offsetHeight) {
          this.getNextPost()
          }
      },



  },

  updated: function() {
    if(this.new_searched_post_active){
        this.scrollToPost();
        this.SET_NEW_SEARCHED_POST_ACTIVE(false);
    } 

  },

  created: function(){
    window.addEventListener('scroll', this.checkEndPost);
  },

  mounted: function(){
    try{
      var post_ids = JSON.parse(document.getElementById("post-ids").innerHTML);
      this.SET_POST_IDS(post_ids);
      this.getNextPost();
      this.getCountryCode();
      //this.checkEndPost();
    } catch(error){
      //this.post_ids = []
    }
  },

  watch: {
    searched_post_active: function(){
      if(this.searched_post_active){
          this.scrollToPost();
          this.SET_SEARCHED_POST_ACTIVE(false);
      }
    }
  }

}

</script>
