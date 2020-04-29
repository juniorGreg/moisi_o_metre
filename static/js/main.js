var customProgress = ("custom-progress", {
  props: ['count'],
  data: function() {
    return  {
      currentCount: 0,
      interval: null,
      observer: null,
      animated: false
    }
  },
  template: '<progress class="progress is-small" :value="currentCount" max="2"></progress>',

  methods: {
    animateValue: function(){
      console.debug("ok")
      if(this.currentCount < this.count){
        this.currentCount += 0.01
      }
      else{
        clearInterval(this.interval)
        console.debug("clear interval")
      }

    },

    startAnimation: function(){
      var element = this.$el;
      var position = element.getBoundingClientRect();

      // checking whether fully visible
      if(position.top >= 0 && position.bottom <= window.innerHeight) {
        console.log('Element is fully visible in screen');
        console.debug("ooki")
        if(!this.animated){

          this.interval = setInterval(this.animateValue, 10);

        }
        this.animated = true
      }

    }
  },

  created: function(){
    window.addEventListener('scroll', this.startAnimation);
  }


})



var app = new Vue({
  el: '#app',

  data: {
    isActive: false
  },

  components: {
    'custom-progress': customProgress
  },

  methods: {
      toggleMenu: function(){
        this.isActive = !this.isActive
      },

      onshow: function(event){
        console.debug("yo")
      }
  },


})
