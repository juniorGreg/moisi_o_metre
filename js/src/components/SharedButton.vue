<template lang="html">
  <a ref="source" target='_blank' :href="url" @click="copyLink">
    <button :class="{'has-tooltip-active': tooltipActive}" class="has-tooltip-arrow button is-text" :data-tooltip="tooltipMsgActive" >
      <img class="image is-24x24" :src="button_img" :alt="alt_text" >
    </button>
  </a>

</template>

<script>



export default {



  props : ['shared_url', "post_id", "local_url", "button_img", "alt_text", "text"],

  data(){
    return {
        tooltipActive: false,
        tooltipMsgActive: null,
        tooltipMsg: "Le lien a été copié dans le presse-papier."
    }
  },

  computed: {
    clean_local_url: function() {
      let regex_clean_local_url = /https?:\/\/[a-z0-9.-]*:?[0-9]*\//i;
      return this.local_url.match(regex_clean_local_url) + this.post_id;
    },
    url: function(){

        //console.log(local_url);
        return this.shared_url.replace("(link)", encodeURI(this.clean_local_url)).replace("(text)", encodeURI(this.text));
    }
  },
  methods: {
    copyLink: function(e){
      //alert("clik")

      if(this.clean_local_url == this.url){

        e.preventDefault();

        var temp = document.createElement("input");

        this.$el.appendChild(temp);
        //console.log(temp);

        temp.setAttribute("value", this.url);
        temp.focus();
        temp.select();

        const isSuccessful = document.execCommand("copy");
        if(!isSuccessful){
          console.error("Failed to copy text");
        }

        this.showTooltip();

        this.$el.removeChild(temp);
      }
    },

    showTooltip: function(){
      this.tooltipActive = true;
      this.tooltipMsgActive = this.tooltipMsg;

      setTimeout(function(obj){
          obj.tooltipActive = false;
          obj.tooltipMsgActive = null;
      }, 3000, this);
    }
  }

}
</script>

<style lang="css" scoped>
</style>
