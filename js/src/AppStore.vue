<template lang="html">
  <div class="container">
    <variants></variants>
    <size-table></size-table>
    <basket :paypal_client_id="paypal_client_id"></basket>

      <div v-for="index in lines_number" :key="index" class="tile is-ancestor">

        <div v-for="product in getSliceProducts(index)" class="tile is-parent">
          <div class="tile is-child box" @click="showVariants(product)">
            <p class="title is-size-6">{{product.name}}</p>

            <figure class="image ">
              <img class="no-dark-mode" :src="product.variant_set[0].variant_image.resized_preview" alt="product image">
            </figure>
            <br>

            <p>{{product.variant_set[0].price}} $ CAD</p>
          </div>
        </div>

      </div>

  </div>

</template>

<script>

import { mapState , mapMutations , mapActions } from 'vuex';
import Variants from './components/Variants.vue';
import Basket from './components/Basket.vue';
import SizeTable from './components/SizeTable.vue';

export default {
  props: ["paypal_client_id"],
  components: {
      Variants,
      Basket,
      SizeTable
  },

  data: function(){
    return {
        columns_number: 3
    }

  },
  computed: {
    ...mapState([
      "products"
    ]),

    lines_number: function() {

      return Math.ceil(this.products.length / this.columns_number);
    }
  },

  methods: {
    ...mapActions([
      "getProducts",
      "showVariantModal",
      "setUpStore"
    ]),

    getSliceProducts: function(index){

      var index0 = (index - 1) * this.columns_number;
      var index1 = index0 + this.columns_number;

      if (index1 > this.products.length) {
        index1 = this.products.length;
      }

      console.log(index1)

      return this.products.slice(index0, index1)

    },

    showVariants: function(product) {
      this.showVariantModal(product)
      console.log("variants");
    }
  },

  mounted: function(){
    this.getProducts();
    this.setUpStore();
  }
}
</script>

<style lang="scss" scoped>
  .tile.is-child.box {

    cursor: pointer;
    filter: grayscale(100%);
    &:hover {
      filter: grayscale(0%);

    }
  }
</style>
