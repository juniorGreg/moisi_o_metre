var customProgress = ("custom-progress", {
  props: ['count'],

  data: function() {
    return  {
      currentCount: 0,
      interval: null,
      observer: null,
      animated: false,
      cursor: null,
      maxCount: 2
    }
  },

  template: '<div><img src="/static/images/moisiometre.png" class="image is-24x24"><progress class="progress is-small" :value="currentCount" :max="maxCount"></progress></div>',

  methods: {
    animateValue: function(){
      console.debug("ok")
      if(this.currentCount < this.count && this.currentCount < this.maxCount){
        this.currentCount += 0.005
        this.setCursorPosition()
      }
      else{
        clearInterval(this.interval)
        //console.debug("clear interval")
      }

    },

    startAnimation: function(){
      var element = this.$el;
      var position = element.getBoundingClientRect();

      // checking whether fully visible
      if(position.top >= 0 && position.bottom <= window.innerHeight) {
        //console.log('Element is fully visible in screen');
        //console.debug("ooki")
        if(!this.animated){

          this.interval = setInterval(this.animateValue, 5);

        }
        this.animated = true
      }

    },

    setCursorPosition: function(){
      var rect = this.$el.getBoundingClientRect();

      var position = this.currentCount/this.maxCount * rect.width - 12;
      var positionPercent = this.currentCount/this.maxCount * 100;

      this.cursor.style.left = `${position}px`;



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
    window.addEventListener('resize', this.setCursorPosition);

  },

  mounted: function(){
    this.cursor = this.$el.getElementsByTagName("img")[0];
    var rect = this.$el.getBoundingClientRect();
    console.debug(rect)
    this.cursor.style.top = `${this.cursor.style.top + 20}px`;

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
      }
  },


})
