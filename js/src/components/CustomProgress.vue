<template lang="html">
  <div class="no-dark-mode">
    <img :src="image_src" class="cursor image is-48x48">
    <progress class="progress is-small" :value="currentCount" :max="maxCount"></progress>
  </div>
</template>

<script>
import anime from 'animejs/lib/anime.es.js'

export default {
  name: "custom-progress",
  props: ['count', 'image_src'],

  data: function() {
    return  {
      currentCount: 0,
      animated: false,
      cursor: null,
      maxCount: 7
    }
  },

  methods: {

    startAnimation: function(){
      var element = this.$el;
      var position = element.getBoundingClientRect();


      // checking whether fully visible
      if(position.top >= 0 && position.bottom <= window.innerHeight) {

        if(!this.animated){
          var rect = this.$el.getBoundingClientRect();
          var cursor_position = this.count/this.maxCount * rect.width - 12;

            anime({
              targets: this.cursor,
              translateX: cursor_position,
              duration: 5000
            });

            anime({
              targets: this,
              currentCount: this.count,
              duration: 5000,
              update: this.setCursorPosition
            })
          //this.interval = setInterval(this.animateValue, 5);

        }
        this.animated = true
      }

    },

    setCursorPosition: function(){

      var positionPercent = this.currentCount/this.maxCount * 100;

      var gradient = `linear-gradient(to right, lightgreen ${100 - positionPercent}%, yellow)`;

      if(positionPercent > 33.3333)
        gradient = `linear-gradient(to right, lightgreen ${66.6666 - 16.6666 * ((positionPercent-33.3333)/33.3333)}%, yellow)`;
      if(positionPercent > 66.6666)
        gradient = `linear-gradient(to right, lightgreen ${50 - 16.6666 * ((positionPercent-66.666)/33.3333)}%, yellow ${100 - 33.3333 * ((positionPercent-66.6666)/33.3333)}%, red)`;

      this.$el.style.setProperty('--progress-bar-background', gradient);
    }
  },

  created: function(){
    window.addEventListener('scroll', this.startAnimation);
  },

  mounted: function(){

    this.cursor = this.$el.getElementsByTagName("img")[0];
  }
}
</script>

<style lang="css" scoped>
</style>
