<template lang="html">
  <div class="modal" :class="{'is-active': is_variant_visible}">
    <div class="modal-background"></div>
      <div class="modal-content">
        <!-- Any other Bulma elements you want -->
        <div class="box" v-if="selected_product">
            <p>{{ selected_product.name }}</p>
            <figure class="image">
                <img class="no-dark-mode" :src="selected_product.variant_set[variant_index].preview" alt="product image">
            </figure>
            <br>
            <div class="buttons">
              <div class="text is-shared is-size-6 is-size-7-mobile">
                Couleurs disponibles:
              </div>
                <button v-for="color in variant_colors" class="button is-small button-color no-dark-mode is-text" :style="{'background-color': getHexColor(color)}">

                </button>

            </div>
            <div class="buttons">
              <div class="text is-shared is-size-6 is-size-7-mobile">
                Grandeur disponibles:
              </div>
                <button v-for="size in variant_sizes" class="button is-small is-text" >
                    {{size}}
                </button>

            </div>
            <p>{{ selected_product.variant_set[variant_index].price}}</p>
            <button class="button no-dark-mode is-small is-info">Ajouter au panier</button>
        </div>

      </div>
    <button class="modal-close is-large" aria-label="close" @click="hideVariantModal"></button>
  </div>
</template>

<script>
import { mapState , mapMutations , mapActions , mapGetters} from 'vuex';
export default {
  data: function(){
    return {
      variant_index: 0,
      colors: [],
      sizes: []
    }
  },

  computed: {
    ...mapState([
      'is_variant_visible',
      "selected_product"
    ]),
    ...mapGetters([
      "variant_colors",
      "variant_sizes"
    ])
  },

  methods: {
    ...mapActions([
      'hideVariantModal'
    ]),

    getHexColor: function(color) {
      var colormap = {
        "black": "#14191e",
        "navy": "#191c25",
        "dark heather": "#37363b",
        "red": "#a2312b"
      }

      return colormap[color];
    }
  },

}
</script>

<style lang="scss" scoped>
  .button-color {
    height: 25px;
    width: 25px;
    border-radius: 50%;
    background-color: blue;
    border-color: grey;
  }
</style>
