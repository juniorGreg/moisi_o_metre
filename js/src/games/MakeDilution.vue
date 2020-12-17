<template lang="html">
  <div class="box">
    <h2 class="subtitle is-size-6-mobile">Faîtes votre propre dilution homéopathique</h2>
    <p>En partant d'une teinture mère, faîtes votre propre dilution homéopathique en CH.
    Plus que la solution est bleue, plus qu'elle est diluée</p>

    <div class="dilution-game">
      <p>CH: {{ CH }}</p>
      <p class="format-percent">% de teinture originale: {{ format_percent_tinture }}</p>
      <p class="has-text-weight-bold">{{ message }}</p>

      <div id="solution" :style="{ 'background-color': 'hsl(200, '+ saturation + '%, '+ lighness +'%)'}">
      </div>


      <br>
      <div class="buttons has-addons is-align-content-center">
        <button class="button is-info" type="button" name="button" @click="increment" >Diluer</button>
        <button class="button is-black" type="button" name="button" @click="decrement" >Reconcentrer</button>
      </div>
    </div>


  </div>
</template>

<script>
export default {
  data(){
    return {
      CH: 0,
      percent_tinture: 100,
      saturation: 0,
      lighness: 0,
    }
  },
  computed: {
    format_percent_tinture: function() {
      if(this.CH > 1){
        return this.percent_tinture.toFixed(this.CH + (this.CH - 2));
      }
      else{
        return this.percent_tinture;
      }
    },

    message: function(){
      if(this.CH == 0){
        return "Allez-y ! Diluez-moi ça !"
      }
      else if(this.CH == 1){
        return "Déjà, vous pouvez le constater. À 1 CH, la solution est déjà très bleue. Déjà visuellement, ça risque de plus changer beaucoup. Mais on est encore très loin des dilutions homéopathiques.";
      }

      else if(this.CH > 1 && this.CH < 5) {
        return "Dynamisez-moi ça encore plus "+this.exclamation(this.CH);
      }
      else if(this.CH >= 5 && this.CH < 12) {
        return "Ne vous découragez pas. Vous y êtes presque "+this.exclamation(this.CH)
      }
      else if(this.CH == 12){
        return "Ça y est ! Vous y êtes arrivé. À partir de 12 CH, il n'y a plus aucune molécule de la teinture original. :) Mais continuez pour voir !"
      }
      else if(this.CH > 12 && this.CH < 30){
          return "C'est encore une dilution valide en homéopathie. Allez-y encore plus "+this.exclamation(this.CH)
      }
      else if(this.CH == 30){
        return "Bravo, à 30 CH, c'est comme diluer un litre d'eau dans la Voie Lactée."
      }
      else if(this.CH == 51){
        return "Désolé, vous avez atteint les limites même de Javascript. Après ça, le nombre de dilution est trop petit ! ;("
      }
      else {
        return "eau pure"
      }
    }
  },
  methods: {
    increment: function(){
      if(this.CH < 51){
        this.CH++;
      }
    },

    decrement: function() {
      if(this.CH > 0){
        this.CH--;
      }
    },
    exclamation: function(CH) {
      return "!".repeat(CH);
    }
  },

  watch: {
    CH: function(){

      this.percent_tinture = 100 * 0.01 ** this.CH;
      this.saturation = 100 - (this.percent_tinture);
      this.lighness = 50 - (this.percent_tinture/2);
    }
  }
}
</script>

<style lang="css" scoped>
#solution {
  height: 10rem;
  width: 10rem;
  transition: background-color 5s;
  border-radius: 15px;
  border: 3px solid grey;
  margin:auto;
}

.buttons {
  margin: auto;
  width: 12.8rem;
}

.dilution-game p {
  text-align: center;
}

.format-percent{
  word-break: break-all;
}
</style>
