Vue.component("custom-progress", {
  props: ['count'],

  template: "#custom-progress",

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

      console.log("oki");

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
      console.log("oki");
    this.cursor = this.$el.getElementsByTagName("img")[0];
  }
});

Vue.component("source-url", {
  props: ["source", "title"],
  template: "#source-url",
  delimiters: ['${', '}']
});

Vue.component("shared-button", {
  props : ['shared_url', "post_id", "local_url", "button_img", "alt_text", "text"],
  template: "#shared-button",
  delimiters: ['${', '}'],

  computed: {
    url: function(){
        return this.shared_url.replace("(link)", encodeURI(this.local_url+this.post_id)).replace("(text)", encodeURI(this.text));
    }
  }
})






var app = new Vue({
  el: '#app',

  delimiters: ['${', '}'],

  data: {
    isActive: false,
    posts: [],
  },

  methods: {
      toggleMenu: function(){

        this.isActive = !this.isActive
      },

      addPost: function(post){
        post.rottenpoint_set = post.rottenpoint_set.sort((a,b) => (a.order > b.order) ? 1 : -1);
        this.posts.push(post)
      }
  },

  mounted: function(){
    axios.get("/posts").then(
      response => (this.addPost(response.data))
    )
  }


})
