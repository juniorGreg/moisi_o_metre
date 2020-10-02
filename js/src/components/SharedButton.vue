<template lang="html">
  <a ref="source" target='_blank' :href="url" @click="copyLink">
    <button class="button is-text">
      <img class="image is-24x24" :src="button_img" :alt="alt_text">
    </button>
  </a>
</template>

<script>
export default {
  props : ['shared_url', "post_id", "local_url", "button_img", "alt_text", "text"],

  computed: {
    clean_local_url: function() {
      let regex_clean_local_url = /https?:\/\/[a-z.]*:?[0-9]*\//i;
      return this.local_url.match(regex_clean_local_url) + this.post_id;
    },
    url: function(){

        //console.log(local_url);
        return this.shared_url.replace("(link)", encodeURI(this.clean_local_url)).replace("(text)", encodeURI(this.text));
    }
  },
  methods: {
    copyLink: function(e){
      if(this.clean_local_url == this.url){
        e.preventDefault();
        navigator.clipboard.writeText(this.url);

        document.execCommand("copy");
      }


      //console.log(this.$el.value);

    }
  }

}
</script>

<style lang="css" scoped>
</style>
