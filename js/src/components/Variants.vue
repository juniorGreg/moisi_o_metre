<template lang="html">
  <div class="modal" :class="{'is-active': is_variant_visible}">
    <div class="modal-background"></div>
      <div class="modal-content">
        <!-- Any other Bulma elements you want -->
        <div class="box" v-if="selected_variant">
            <p>{{ selected_product.name }}</p>
            <figure class="image">
                <img class="no-dark-mode" :src="selected_variant.preview" alt="product image">
            </figure>
            <br>
            <div class="buttons">
              <div class="text is-shared is-size-6 is-size-7-mobile">
                Couleurs disponibles:
              </div>
                <button v-for="color in variant_colors"
                        class="button is-small button-color no-dark-mode is-text"
                        :class="{'is-selected': isColorSelected(color)}"
                        :style="{'background-color': getHexColor(color)}"
                        @click="getVariantByColor(color)">

                </button>

            </div>
            <div class="buttons">
              <div class="text is-shared is-size-6 is-size-7-mobile">
                Grandeur disponibles:
              </div>
              <div class="control is-size-7">
                  <label v-for="size in variant_sizes" class="radio">
                      <input type="radio" name="size" :value="size" v-model="selected_size">
                      {{ size }}
                  </label>
              </div>


            </div>
            <p>{{ selected_variant.price }}</p>
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

      colors: [],
      sizes: [],

    }
  },

  computed: {
    ...mapState([
      'is_variant_visible',
      "selected_product",
      "selected_variant"
    ]),
    ...mapGetters([
      "variant_colors",
      "variant_sizes"
    ]),

    selected_size: {
      get() {

        return this.selected_variant.size

      },
      set(size) {
        //console.log(size)
        const color = this.selected_variant.color;
        this.getVariantBySizeAndColor(size, color);
      }
    },


  },

  methods: {
    ...mapActions([
      'hideVariantModal',
      "getVariantBySizeAndColor"
    ]),

    getHexColor: function(color) {
      var colormap = {
        "black": "#14191e",
        "navy": "#191c25",
        "dark heather": "#37363b",
        "red": "#a2312b"
      }

      return colormap[color];
    },

    isColorSelected: function(color) {
      return color === this.selected_variant.color;
    },

    getVariantByColor: function(color) {
      const size = this.selected_variant.size;
      console.log(color)
      this.getVariantBySizeAndColor(size, color);
    }
  }



}
</script>

<style lang="scss" scoped>
  .button-color {
    height: 25px;
    width: 25px;
    border-radius: 50%;
    background-color: blue;
    border-color: grey;
    border-width: 2px;

    &:hover, &.is-selected {
      height: 30px;
      width: 30px;

    }
  }

  .button-size {
    padding: 0.3rem;
    height: 1.3rem;

    &:hover {
      padding: 0.4rem;
    }
  }
</style>
