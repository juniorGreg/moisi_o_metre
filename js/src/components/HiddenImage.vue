<template lang="html">
  <div @mouseover="showHiddenImage" @mouseout="showImage" v-touch:start="showHiddenImageMobile" v-touch:end="showImageMobile">
    <img v-show="!hidden" class="image-post is-hidden-mobile"  :src="image_src" alt="image source" >
    <img v-show="!hidden" class="image-post-mobile is-hidden-tablet"  :src="image_src" alt="image source" >

    <img v-show="hidden" class="image-post is-hidden-mobile"  :src="hidden_image_src" alt="image source" >
    <img v-show="hidden" class="image-post-mobile is-hidden-tablet" :src="hidden_image_src" alt="image source" >
  </div>
</template>

<script>

import Vue from 'vue'
import Vue2TouchEvents from 'vue2-touch-events'

Vue.use(Vue2TouchEvents, {
  touchHoldTolerance: 10000,
  longTapTimeInterval: 10000
})

export default {
  props : ["image_src", "hidden_image_src"],
  template: "#hidden-image",
  delimiters: ['${', '}'],

  data: function() {
    return {
      hidden: false,
    }
  },

  methods: {
    showHiddenImage: function(){
        if(typeof window.ontouchstart !== 'undefined'){
            return;
        }

        this.hidden=true;
    },

    showImage: function(){
      if(typeof window.ontouchstart !== 'undefined'){
          return;
      }
      this.hidden = false;
    },

    showHiddenImageMobile: function(){
        this.hidden=true;
    },

    showImageMobile: function(){
      this.hidden = false;
    }
  },

  mounted: function(){
    this.$el.addEventListener('contextmenu', e=> {
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
      return false;
    })
  }

}
</script>

<style lang="css" scoped>
</style>
