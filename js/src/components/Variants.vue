<template lang="html">
  <section class="modal" :class="{'is-active': is_variant_visible}">
    <div class="modal-background"></div>
      <div class="modal-content">

        <div class="box box-variant" v-if="selected_variant">
            <p>{{ selected_product.name }}</p>
            <figure class="image is-square" v-if="selected_variant.variant_image">
                <img class="no-dark-mode" height="450" width="450" :src="selected_variant.variant_image.resized_preview" alt="product image">
            </figure>
            <br>
            <div class="buttons" v-if="is_color">
              <div class="text is-shared is-size-6 is-size-7-mobile">
                Couleurs disponibles:
              </div>
                <button v-for="color in variant_colors"
                        class="button is-small button-color no-dark-mode is-text"
                        :class="{'is-selected': isColorSelected(color)}"
                        :style="{'background-color': getHexColor(color)}"
                        @click="getVariantByColor(color)" :data-tooltip="color">

                </button>

            </div>
            <div v-if="is_size" >
              <div class="text is-shared is-size-6 is-size-7-mobile">
                Grandeur disponibles:
              </div>
              <div class="control is-size-7">
                  <label v-for="size in variant_sizes" class="radio">
                      <input type="radio" name="size" :value="size" v-model="selected_size">
                      {{ size }}
                    </input>
                  </label>
              </div>
              <button class="button is-text is-small" type="button" name="button" @click="showSizeTableModal">Guide des grandeurs</button>
            </div>
            <br>



            <p> {{ selected_variant.price }} CDN$</p>
            <button class="button no-dark-mode is-small is-info" @click="addItemToBasket">Ajouter au panier</button>
        </div>

      </div>
    <button class="modal-close is-large" aria-label="close" @click="hideVariantModal"></button>
  </section>
</template>

<script>
import { mapState , mapMutations , mapActions , mapGetters} from 'vuex';
export default {


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

        const color = this.selected_variant.color;
        this.getVariantBySizeAndColor({ size, color });
      }
    },

    is_size: function(){

      return this.variant_sizes[0] !== '';
    },
    is_color: function(){

      return this.variant_colors[0] !== '';
    }

  },

  methods: {
    ...mapActions([
      'hideVariantModal',
      "getVariantBySizeAndColor",
      "getShippingCost",
      "showSizeTableModal"
    ]),
    ...mapMutations([
      'ADD_VARIANT_TO_BASKET'
    ]),

    getHexColor: function(color) {
      var colormap = {
        "black": "#14191e",
        "navy": "#191c25",
        "dark navy": "#0a1b2b",
        "dark heather": "#37363b",
        "dark grey": "#666b64",
        "dark grey heather": "#3c302e",
        "military green": "#68664d",
        "red": "#a2312b",
        "sport grey": "#9b969c",
        "white": "#f1f0f5",
        "heather grey": "#a6a5a0",
        "spruce": "#263d2d",
        "royal blue": "#004074",
        "asphalt": "#353146",
        "navy blazer": "#292d3b",
        'maroon': "#7d263a",
        "charcoal heather": "#463e3d",
        "carbon grey": "#c7c3be"
      }

      return colormap[color];
    },

    isColorSelected: function(color) {
      return color === this.selected_variant.color;
    },

    getVariantByColor: function(color) {
      const size = this.selected_variant.size;

      this.getVariantBySizeAndColor({ size, color });
    },

    addItemToBasket: function() {
      this.ADD_VARIANT_TO_BASKET(this.selected_variant);
      this.getShippingCost()
      this.hideVariantModal()
    }
  }



}
</script>

<style lang="scss" scoped>
    p {
      margin-bottom: 0.75rem;
    }
    .box-variant {
      max-width: 500px;
    }

  .button-color {
    height: 25px;
    width: 25px;
    border-radius: 50%;
    background-color: blue;
    border-color: grey;
    border-width: 2px;
    margin: 0.1rem;

    &:hover, &.is-selected {
      height: 30px;
      width: 30px;
      margin: calc(0.1rem - 5px);

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
