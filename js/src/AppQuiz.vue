<template lang="html">
  <div class="container">
    <h1 class="title">Les quiz de MoisiOMètre</h1>

    <div class="box">
      <article class="media">
        <div class="media-content">
          <div class="content">
            <h2 class="title">Pensez-vous Bayésien ?</h2>

            <h3 class="subtitle">{{ question.title }}</h3>
            <transition name="fade" mode="out-in">
              <form @submit.prevent="respond" v-for="sub_question in question.sub_questions"
                  v-if="question.sub_questions.indexOf(sub_question) ===  sub_questions_sequence"
                  :key="question.sub_questions.indexOf(sub_question)">
                <h4>{{sub_question.title}}</h4>
                <div class="field">
                  <div class="control" v-for="value in sub_question.values">
                    <label class="radio">
                      <input type="radio" name="answer" :value="value" v-model="selected_value">
                        {{value}}
                      </label>
                  </div>
                </div>
                <div class="field">
                  <div class="control">
                      <button class="button" type="submit" >Répondre</button>
                  </div>
                </div>

              </form>
              <div v-if="question.sub_questions.length === sub_questions_sequence" :key="question.sub_questions.length">

              </div>

          </transition>
          <chart></chart>
          </div>
        </div>

      </article>
    </div>

  </div>
</template>

<script>

import Chart from "./components/Chart.vue";

export default {
  components: {
    Chart
  },
  data(){
    return {
      question:
        { title: "Qui a construit les pyramides de Kheops ?" ,
          sub_questions: [
            { title: "Les extraterrestres", values: [0, 0.01, 50.0, 95.0, 100] },
            { title: "Les anciens égyptiens", values: [0.001, 0, 100, 3.1416] }
          ]
        }
      ,
      selected_value: "",
      values: [],
      sub_questions_sequence: 0,


    }
  },

  methods: {
    respond: function(){
      this.values.push(this.selected_value);
    this.next_sub_question();
      //console.log(this.selected_respond);
    },
    next_sub_question: function() {
      this.sub_questions_sequence++;
      //this.current_sub_question = this.question.sub_questions[this.sub_questions_sequence];
    }
  },
  mounted: function(){
    //this.next_sub_question();
  }
}
</script>

<style lang="css" scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
