<template lang="html">
<div>
  <h1 class="title is-size-6-mobile">Évaluer un site</h1>

  <form id="website_form" @submit.prevent="evaluateWebsite">

    <div class="field">
      <label for="website_url">Url: </label>
      <div class="control">
        <input class="input is-small" onfocus="this.value=''" type="url" name="website_url" v-model="url" required>
      </div>
    </div>


    <div class="field">
      <div class="control">
        <button class="button is-link is-small" :class="{'is-loading': loading_eval }" type="submit" name="button">Évaluer</button>
      </div>
    </div>

  </form>
  <br>
  <div v-if="error">
    <div class="notification is-danger">
      {{error}}
    </div>
  </div>
  <div v-if="website">

    <h2 class="subtitle">{{website.title}}</h2>

    <p>Il y a environ {{website.score}} % selon Bullshit-O-Mètre</p>
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
      error: null
    }
  },


  methods: {
    evaluateWebsite: function(e){
        let url_escaped = encodeURIComponent(this.url);
        this.loading_eval = true;
        this.error = null;
        axios.get("/bullshit_o_metre/website/?url="+url_escaped).then(response => {
          console.log(response);
          this.website = response.data

        }).catch(api_error => {
          console.log(api_error);
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

<style lang="css" scoped>
</style>
