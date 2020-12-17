<template lang="html">
  <div class="container">
    <h1 class="title is-size-6-mobile">Les quiz de MoisiOMètre</h1>

  <!-- <quiz-bayes></quiz-bayes> -->
  <make-dilution></make-dilution>

  </div>
</template>

<script>

//import QuizBayes from "./games/QuizBayes.vue";
import MakeDilution from "./games/MakeDilution.vue";


export default {
  components: {
    MakeDilution
    //QuizBayes
  }
}
</script>

<style lang="css" scoped>

</style>
