<template lang="html">
  <div class="container">
    <h1 class="title">Les quiz de MoisiOMètre</h1>
    <h2 class="subtitle">Pensez-vous Bayésien ?</h2>

    <form class="" action="index.html" method="post" @submit.prevent="respond">
      <div class="field">
        <div class="control" v-for="respond in responds">
          <label class="radio">
            <input type="radio" name="answer" :value="respond" v-model="selected_respond">
              {{respond}}
            </label>
        </div>
      </div>
      <div class="field">
        <div class="control">
            <button class="button" type="submit" >Répondre</button>
        </div>
      </div>

    </form>
  </div>
</template>

<script>
export default {
  data(){
    return {
      responds: ['a', 'b', 'c'],
      selected_respond: ""

    }
  },

  methods: {
    respond: function(){
      console.log(this.selected_respond);
    }
  }
}
</script>

<style lang="css" scoped>
</style>
