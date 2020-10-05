<template lang="html">
<div>
  <section class="section">

    <div class="container">
        <h1 class="title">Ajouter un site web labellé</h1>
        <form name="labeled_website_form" @submit.prevent="add_labeled_website">
          <div class="field">
            <label for="website_url">Url: </label>
            <div class="control">
              <input type="url" name="website_url" v-model="labeled_url" required>
            </div>
          </div>

          <div class="field">
            <div class="control">

              <label class="checkbox">C'est de la bullshit ?
                <input type="checkbox" name="is_bullshit" v-model="is_bullshit">
              </label>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <button type="submit" class="button is-link is-small" :class="{'is-loading': loading_add}"  name="button">Ajouter</button>
            </div>
          </div>
        </form>
    </div>

  </section>
  <div v-if="labeled_website">
    <section class="section">
      <div class="container">
        <h1 class="title">{{labeled_website.title}}</h1>
        <p>Langue: {{labeled_website.lang}}</p>
        <p>{{labeled_website.texts}}</p>


      </div>
    </section>

  </div>
</div>

</template>

<script>

import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = 'csrftoken';

export default {
  data() {
    return {

      labeled_website: null,

      labeled_url: "",
      is_bullshit: false,
      loading_eval: false,
      loading_add: false,
      error: null
    }
  },

  methods: {
    add_labeled_website: function(e){
        let data = {
          url: this.labeled_url,
          is_bullshit: this.is_bullshit
        }
        this.loading_add = true;
        axios.post("/bullshit_o_metre/website/", data).then(response => {
          this.labeled_website = response.data
        }).catch(error =>{
          console.log(error)
        }).then(() => {
          this.labeled_url = "";
          this.is_bullshit = false;
          this.loading_add = false;
        });
    }
  }
}
</script>

<style lang="css" scoped>
</style>
