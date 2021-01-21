<template lang="html">
  <div :id="post.id" class="box">
    <h1 class="title is-size-6-mobile">{{post.title}} </h1>
    <h2 class="subtitle is-size-7 is-italic">
      Temps de lecture: <span v-if="post.statistics.avg_reading_time > 1"> environ {{post.statistics.avg_reading_time}} minutes </span>
                        <span v-if="post.statistics.avg_reading_time == 1">environ une minute</span>
                        <span v-if="post.statistics.avg_reading_time == 0">moins qu'une minute</span>
                        <span class="has-text-danger" v-if="post.admin_only">ADMIN SEULEMENT</span>
    </h2>

    <div v-if="post.post_type == 'BD'">
        <p class="has-text-justified">{{post.content}}</p>
        <br>
        <figure class='image'>
            <img class="no-dark-mode" :src="post.image" alt="imâge">
        </figure>
        <br>
    </div>

    <div class="post-content" v-else>
      <div v-if="post.image && !post.hidden_image" class="no-dark-mode">
        <img class="image-post is-hidden-mobile no-dark-mode" :src="post.image" alt="imâge">
        <img class="image-post-mobile is-hidden-tablet no-dark-mode" :src="post.image" alt="imâge">
      </div>

      <div v-if="post.image && post.hidden_image">
          <HiddenImage :image_src="post.image" :hidden_image_src="post.hidden_image" />
      </div>

      <div v-if="post.content">
        <vue-showdown :markdown="post.content" :extensions="['targetlink']">
      </div>

      <div v-if="post.rottenpoint_set.length > 0 ">
        <div v-for="point in post.rottenpoint_set">
          <h2 class="subtitle is-size-6-mobile has-text-weight-bold">{{point.title}}</h2>

          <div>
            <vue-showdown :markdown="point.description">
          </div>
        </div>
      </div>

      <div v-if="post.media_link">
        <MediaLink :mediaLink="post.media_link" :spotify_img="spotify_img" :itunes_img="itunes_img"
          :soundcloud_img="soundcloud_img" :google_podcast_img="google_podcast_img" />
      </div>

      <div v-if="post.post_type == 'CRITIC'">
        <CustomProgress :count="post.rotten_score" :image_src="cursor_img"/>
      </div>

      <br>

      <div v-if="post.pub && country_code" >
        <h2 class="subtitle is-size-6-mobile">Le lien affiliate du post</h2>
        <article class="media">
          <div class="media-content">
            <div class="content">
              <figure v-if="post.image_pub" style="float: left; margin-top: 0; margin: 0.5rem;">
                <a :href="getPubLink(post)" target="_blank" class="image is-128x128">
                  <img ref="image_pub" :src="post.image_pub" alt="image publicitaire" width="128" height="128">
                </a>
              </figure>

                <vue-showdown :markdown="post.pub" :extensions="['targetlink']"></vue-showdown>
                <p class="is-size-7">
                  Lien: <a :href="getPubLink(post)" class="is-size-7" target="_blank">{{post.link_title}}</a>
                </p>

            </div>

          </div>

        </article>
      </div>
      <br>
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
            <span class="text">
            <span v-if="post.show_sources">Cacher&nbsp</span>
            <span v-else>Afficher&nbsp</span>les sources
          </span>
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


</template>

<script>
import Vue from 'vue'
import { mapState , mapMutations , mapActions } from 'vuex';

import VueShowdown, { showdown } from 'vue-showdown'
import Vue2TouchEvents from 'vue2-touch-events'

import anime from 'animejs/lib/anime.es.js'
import { ref, onMounted } from 'vue'


//Extension to add target to link
showdown.extension('targetlink', function() {
  return [{
    type: 'lang',
    regex: /\[([^\[\]]+)\]\(([^\(\)]+)\)\{:target="([^\{\}]+)"\}/g,
    replace: function(wholematch, linkText, url, target) {

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


import CustomProgress from "./CustomProgress.vue";
import SourceUrl from "./SourceUrl.vue";
import SharedButton from "./SharedButton.vue";
import HiddenImage from './HiddenImage.vue';
import MediaLink from './MediaLink.vue'

export default {
  props: ["post", 'local_url', "facebook_button_img", "twitter_button_img", 'copy_link_button_img',
          "support_href", "cursor_img", "spotify_img", "itunes_img", "soundcloud_img",
          "google_podcast_img"],
  components: {
    CustomProgress,
    SourceUrl,
    SharedButton,
    HiddenImage,
    MediaLink
  },
  computed: {
    ...mapState([
      "country_code"
    ])
  },

  methods: {
    showSources: function(el){
      el.style.maxHeight = el.scrollHeight + "px";
      //console.log(this.$refs.image_pub);

    },

    hideSources: function (el){
        el.style.maxHeight = 0;
    },

    getPubLink: function(post){
      if(this.country_code === "CA"){
        return post.link_ca;
      }else{
        return post.link_fr;
      }

    },

    loadImagePubAnimation: function(){
      console.log("mounted")
      anime({
        targets: this.$refs.image_pub,
        direction: "alternate",
        easing: "linear",
        scale: 1.2,
        loop: true
      })
    }

  },

  updated: function(){
    //console.log(this.$refs.image_pub)
  },

  mounted: function() {

    setTimeout(this.loadImagePubAnimation, 2000);

  },

}
</script>

<style lang="css" scoped>
</style>
