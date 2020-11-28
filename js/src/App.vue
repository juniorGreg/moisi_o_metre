
<template>
  <div class="container">
    <div class="posts" v-for="post in posts">
      <div class="box">
        <h1 class="title is-size-6-mobile">{{post.title}}</h1>
        <h2 class="subtitle is-size-7 is-italic">Temps de lecture: environ {{post.statistics.avg_reading_time}} minutes</h2>

        <div v-if="post.post_type == 'BD'">
            <p class="has-text-justified">{{post.content}}</p>
            <br>
            <figure class='image'>
                <img :src="post.image" alt="imâge">
            </figure>
            <br>
        </div>

        <div v-else>
          <div v-if="post.image && !post.hidden_image">
            <img class="image-post is-hidden-mobile" :src="post.image" alt="imâge">
            <img class="image-post-mobile is-hidden-tablet" :src="post.image" alt="imâge">
          </div>

          <div v-if="post.image && post.hidden_image">
              <HiddenImage :image_src="post.image" :hidden_image_src="post.hidden_image" />
          </div>

          <div>
            <vue-showdown :markdown="post.content" :extensions="['targetlink']">
          </div>

          <div v-if="post.rottenpoint_set.length > 0 ">
            <h2 class="subtitle is-size-6-mobile">Les Points Moisis</h2>
            <div v-for="point in post.rottenpoint_set">
              <h3 class="has-text-weight-bold">{{point.title}}</h3>
              <br>
              <div>
                <vue-showdown :markdown="point.description">
              </div>
            </div>
          </div>
          <div v-if="post.pub" >
            <h2 class="subtitle is-size-6-mobile">Le lien affiliate du post</h2>
            <div>
              <vue-showdown :markdown="post.pub" :extensions="['targetlink']">
            </div>
          </div>

          <div v-if="post.sources.length > 0">
              <transition
                @enter="showSources"
                @leave="hideSources">
                <div class="sources" v-show="post.show_sources">
                  <h2 class="subtitle is-size-6-mobile">Les Sources</h2>
                  <div v-for="source in post.sources" >
                    <SourceUrl :title="source.title" :source="source.source" />
                  </div>
                </div>
              </transition>

              <button @click="post.show_sources = !post.show_sources" class="button is-small">
                <span v-if="post.show_sources">Cacher&nbsp</span>
                <span v-else>Afficher&nbsp</span>les sources
              </button>
          </div>




        </div>
        <br>

        <div class="is-size-7">Créer le {{post.date_created}}</div>
        <div v-if="post.show_modified_date">
          <div class="is-size-7">Modifier le {{post.date_modified}}</div>
        </div>

        <div class="buttons has-addons">
          <div class="is-shared is-size-6 is-size-7-mobile">
            Partagez:
          </div>


          <SharedButton shared_url="https://www.facebook.com/sharer.php?u=(link)"
              :local_url="local_url"
              :post_id="post.id"
              :button_img="facebook_button_img"
              alt_text="share button facebook"></SharedButton>

          <SharedButton shared_url="https://twitter.com/intent/tweet?url=(link)&text=(text)&hashtags=espritcritique,zététique,humour"
              :text="post.title"
              :local_url="local_url"
              :post_id="post.id"
              :button_img="twitter_button_img"
              alt_text="share button twitter"></SharedButton>
          <SharedButton shared_url="(link)" :local_url="local_url"
              :post_id="post.id" :button_img="copy_link_button_img" alt_text="copy link button"></SharedButton>

        </div>

      </div>

      <br>
    </div>
</template>


<script>
import Vue from 'vue'
import VueShowdown, { showdown } from 'vue-showdown'
import Vue2TouchEvents from 'vue2-touch-events'

import axios from 'axios'

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

//Extension to add target to link
showdown.extension('targetlink', function() {
  return [{
    type: 'lang',
    regex: /\[([^\[\]]+)\]\(([^\(\)]+)\)\{:target="([^\{\}]+)"\}/g,
    replace: function(wholematch, linkText, url, target) {
      console.log(url)
      console.log(linkText)
      console.log(target)
      var result = '<a href="' + url + '"';

      if (typeof title != 'undefined' && title !== '' && title !== null) {
        title = title.replace(/"/g, '&quot;');
        title = showdown.helper.escapeCharacters(title, '*_', false);
        result += ' title="' + title + '"';
      }

      if (typeof target != 'undefined' && target !== '' && target !== null) {
        result += ' target="' + target + '"';
      }

      result += '>' + linkText + '</a>';
      return result;
    }
  }];
});






// the second parameter of Vue.use() is optional
Vue.use(VueShowdown, {
  // set default flavor of showdown
  flavor: 'github',
  // set default options of showdown (will override the flavor options)
  options: {
    emoji: true,
  },
});

Vue.config.productionTip = false


import CustomProgress from "./components/CustomProgress.vue";
import SourceUrl from "./components/SourceUrl.vue";
import SharedButton from "./components/SharedButton.vue";
import HiddenImage from './components/HiddenImage.vue';


export default {
  name: 'App',

  props: ['local_url', "facebook_button_img", "twitter_button_img", 'copy_link_button_img' ,"support_href"],

  components: {
    CustomProgress,
    SourceUrl,
    SharedButton,
    HiddenImage
  },

  data() {
    return {
      posts: [],
      post_ids: [],
      post_index: 0,
      query_active: false,

    }
  },

  methods: {


      formatDate: function(date){
        var months = ["Janvier", "Février", "Mars", "Avril", "Mai", 'Juin', "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        var date_element = date.split(" ")
        var month_string = date_element[1];
        var month_index = parseInt(month_string);

        var new_date = date.replace(month_string, months[month_index - 1]);

        return new_date;
      },

      showModifiedDate: function(dateCreated, dateModified){
        var date_created_element = dateCreated.split(" ")
        var date_modified_element = dateModified.split(" ")
        if(date_created_element[0] < date_modified_element[0])
          return true;

        if(date_created_element[1] < date_modified_element[1])
          return true;

        if(date_created_element[2] < date_modified_element[2])
          return true;

        var time_created = date_created_element[3].split(":")
        var time_modified = date_modified_element[3].split(":")

        if(time_created[0] < time_modified[0])
          return true;

        if(time_created[1] < time_modified[1])
          return true;

        return false;
      },

      addPost: function(post){
        post.rottenpoint_set = post.rottenpoint_set.sort((a,b) => (a.order > b.order) ? 1 : -1);
        post["show_modified_date"] = this.showModifiedDate(post.date_created, post.date_modified);
        post.date_created = this.formatDate(post.date_created);
        post.date_modified = this.formatDate(post.date_modified);
        post["show_sources"] = false;
        this.posts.push(post);
      },

      getPost: function(){
        if(this.query_active)
          return;

        this.query_active = true;

        if(this.post_index < this.post_ids.length){
          axios.get("/posts/"+this.post_ids[this.post_index]).then(
            response => {this.addPost(response.data); this.post_index+=1;this.query_active=false;}
          )
        }

      },

      checkEndPost: function(ev){
        if ((window.innerHeight + window.scrollY + 50) >= document.body.offsetHeight) {
          this.getPost()
          }
      },

      showSources: function(el){
        el.style.maxHeight = el.scrollHeight + "px";
        console.log(el.style.maxHeight);
      },

      hideSources: function (el){
        console.log("leave");
        el.style.maxHeight = 0;
      },


  },

  created: function(){
    window.addEventListener('scroll', this.checkEndPost);
  },

  mounted: function(){
    try{
      this.post_ids = JSON.parse(document.getElementById("post-ids").innerHTML);
      this.getPost();
    } catch(error){
      this.post_ids = []
    }
  }
}
/*
var app_bull = new Vue({
  el: '#app_bull',

  delimiters: ['${', '}'],

  data: {
    website: null,
    labeled_website: null,
    url: "",
    labeled_url: "",
    is_bullshit: false,
    loading_eval: false,
    loading_add: false,
    error: null
  },

  methods: {
    evaluate_website: function(e){
        let url_escaped = encodeURIComponent(this.url);
        this.loading_eval = true;
        this.error = null;
        axios.get("/bullshit_o_metre/website/?url="+url_escaped).then(response => {
          this.website = response.data

        }).catch(error => {
          this.error = error.response.data.message
          console.log(error.response)
        }).then(()=>{
          //this.url = "";
          this.loading_eval = false;
        });
        e.preventDefault();
        //e.target.blur();
        //document.getElementById("website_form").reset();
    },

    add_labeled_website: function(e){
        let data = {
          url: this.labeled_url,
          is_bullshit: this.is_bullshit
        }
        this.loading_add = true;
        axios.post("/bullshit_o_metre/website/", data).then(response => {
          this.labeled_website = response.data
        }).catch(error =>{
          console.log(error)
        }).then(() => {
          this.labeled_url = "";
          this.is_bullshit = false;
          this.loading_add = false;
        });


        e.preventDefault();
    }

  }
})*/
</scripts>
