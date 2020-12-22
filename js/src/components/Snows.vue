<template lang="html">
  <div id="neiges" class="no-dark-mode">
    <br>


    <img v-for="n in snowflake_count" :src="snowflake_img" alt="snowflake">

  </div>
</template>

<script>

import anime from 'animejs/lib/anime.es.js'

export default {
  props: ["snowflake_img"],
  data: function(){
    return {
      snowflake_density: 4,
    }
  },

  computed: {
    snowflake_count: function(){
      var width = screen.width;
      return Math.round((width/50) * this.snowflake_density);
    }
  },

  mounted: function(){

    var snowflakes = this.$el.getElementsByTagName("img");
    var height = screen.height + 100;
    var width = screen.width;

    console.log("screen height: "+height);

    Array.from(snowflakes).forEach(function(snowflake, index)
    {
      snowflake.style.left =(-25 + (50 * index) % width)+"px";
      anime({
        targets: snowflake,
        translateY: height,
        //translateX: function(){return anime.random(0,1024)},
        loop: true,
        rotate: function(){return anime.random(-180, 180)},
        scale: function(){ return anime.random(-1.5, 1.5)},
        easing: 'easeInSine',


        //duration: 10000,
        duration: function(){ return anime.random(1000, 30000)},
        opacity: function() {return anime.random(0.5, 1)}
      })
    })

  }

}
</script>

<style lang="css" scoped>
  #neiges {
    position: fixed;
    pointer-events: none;
    display: block;
    color: white;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 2;
    width: 100%;
    height: 100%;
    /*background-color: rgba(0,0,0,0.5);*/

  }

  img {
    opacity: 0;
    z-index: 3;
    position: absolute;
    top:0;

  }
</style>
