<template lang="html">
<div>
  <h2 class="title is-size-6-mobile">Évaluer un site</h2>

  <form id="website_form" @submit.prevent="evaluateWebsite">

    <div class="field">
      <label for="website_url">Url: </label>
      <div class="control">
        <input class="input is-small" onfocus="this.value=''" type="url" name="website_url" v-model="url">
      </div>
    </div>

    OU

    <div class="field">
      <label for="text" class="label" >Text: </label>
      <div class="control">
        <textarea  class="textarea is-small" name="text" rows="4" cols="50" v-model="text"></textarea>
      </div>
    </div>



    <div class="field">
      <div class="control">
        <button class="button is-link is-small" :class="{'is-loading': loading_eval }" type="submit" name="button">Évaluer</button>
      </div>
    </div>

  </form>
  <br>
  <div v-if="website" class="notification is-success">

    <h3 class="subtitle">{{website.title}}</h3>

    <p>Il y a environ {{website.score}} % de b*llshit selon le B*llshit-O-Mètre</p>
  </div>
  <div v-if="error">
    <div class="notification is-danger">
      {{error}}
    </div>
  </div>
  <div v-if="warning">
    <div class="notification is-warning">
      {{warning}}
    </div>
    <br>
  </div>

</div>
</template>

<script>

import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = 'csrftoken';

export default {
  name: "AppBull",

  data() {
    return {
      website: null,
      loading_eval:false,
      url: "",
      text: "",
      error: null,
      warning: null
    }
  },


  methods: {
    evaluateWebsite: function(e){
        let url_escaped = encodeURIComponent(this.url);
        this.loading_eval = true;
        this.error = null
        this.warning = null;
        if(this.text.length > 0){
          this.url = "";
          this.warning="Seulement le text va être évalué. Url ou Text !"
        }

        const request = {
          "url": this.url,
          "text": this.text
        }


        axios.put("/bullshit_o_metre/website", request).then(response => {

          this.website = response.data

        }).catch(api_error => {

          this.error = api_error.response.data.message;
          this.website = null;
        }).then(()=>{
          //this.url = "";
          this.loading_eval = false;
        });


    }

  }
}

</script>

<style lang="scss" scoped>
  .notification p{
    color: white;
  }
</style>
