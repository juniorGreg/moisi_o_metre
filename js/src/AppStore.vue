<template lang="html">
  <div class="container">
    <variants></variants>
    <size-table></size-table>
    <basket :paypal_client_id="paypal_client_id"></basket>

      <div v-for="index in lines_number" :key="index" class="tile is-ancestor">

        <div v-for="product in getSliceProducts(index)" class="tile is-parent">
          <div class="tile is-child box" @click="showVariants(product)">
            <h3 class="title is-size-6">{{product.name}}</h3>

            <figure class="image " v-if="product.variant_set[0].variant_image">
              <img class="no-dark-mode" :src="product.variant_set[0].variant_image.resized_preview" alt="product image">
            </figure>
            <br>

            <p>{{product.variant_set[0].price}} CDN$</p>
          </div>
        </div>

        <div v-for=" padding in getPaddingTilesNumber(index)" class="tile is-parent">

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
  props: ["paypal_client_id", "products_count"],
  components: {
      Variants,
      Basket,
      SizeTable
  },

  data: function(){
    return {
        columns_number: 5,
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

    ...mapMutations([
      "SET_PRODUCTS_COUNT"
    ]),

    getSliceProducts: function(index){

      var index0 = (index - 1) * this.columns_number;
      var index1 = index0 + this.columns_number;

      if (index1 > this.products.length) {
        index1 = this.products.length;
      }


      return this.products.slice(index0, index1)

    },

    getPaddingTilesNumber: function(index){
      var index0 = (index - 1) * this.columns_number;
      var index1 = index0 + this.columns_number;

      if (index1 > this.products.length) {
        return index1 - this.products.length;
      }

      return 0;
    },

    showVariants: function(product) {
      this.showVariantModal(product)
    },

    checkProducts: function(ev){
      if ((window.innerHeight + window.scrollY + 50) >= document.body.offsetHeight) {
          this.getProducts();
      }
    },

    checkWindowSize: function(ev) {
      if(window.innerWidth > 1300){
        this.columns_number = 5;
      }

      else if(window.innerWidth < 1300 && window.innerWidth > 800 ){
        this.columns_number = 3;
      }
    }
  },

  created: function(){
    window.addEventListener('scroll', this.checkProducts);
    window.addEventListener("resize", this.checkWindowSize)
    this.SET_PRODUCTS_COUNT(this.products_count)
  },

  mounted: function(){
    this.checkWindowSize()
    this.getProducts();
    this.setUpStore();
  }
}
</script>

<style lang="scss" scoped>
  p {
    margin-bottom: 0rem;
  }
  .tile.is-child.box {

    cursor: pointer;
    filter: grayscale(100%);
    &:hover {
      filter: grayscale(0%);

    }
  }
</style>
