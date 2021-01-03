<template lang="html">
  <div class="modal" :class="{'is-active': is_basket_visible}">
    <div class="modal-background"></div>
      <div class="modal-content">
        <!-- Any other Bulma elements you want -->
        <div class="box">
          <h1 class="title">Votre panier</h1>
          <article v-for="item in basket" class="media">

            <figure class="media-left">
              <p class="image is-64x64">
                <img class="no-dark-mode" :src="item.thumbnail" alt="image item">
              </p>
            </figure>

            <div class="media-content">
              <div class="content is-size-7">
                <nav class="level">
                  <div class="level-left">
                    <div class="level-item">
                        {{ item.name }}
                    </div>
                  </div>
                  <div class="level-right">
                    <div class="level-item">
                      {{ item.price }}
                    </div>
                  </div>
                </nav>

              </div>

            </div>

            <div class="media-right">
                <button class="delete" @click="REMOVE_VARIANT_FROM_BASKET(item)"></button>
            </div>

          </article>
          <nav class="level">
            <div class="level-left">
              <div class="level-item">
                  coût de livraison:
              </div>
            </div>

            <div class="level-right">
                <div class="level-item">
                  {{ shipping_cost }}
                </div>
            </div>
          </nav>
          <nav class="level">
            <div class="level-left">
              <div class="level-item">
                  coût total:
              </div>
            </div>

            <div class="level-right">
                <div class="level-item">
                  {{ basket_total_price }}
                </div>
            </div>
          </nav>
          <button type="button" class="button is-small is-info" name="button">Passer à la caisse</button>

        </div>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="hideBasketModal"></button>

  </div>
</template>

<script>
import { mapState , mapMutations , mapActions , mapGetters} from 'vuex';

export default {
  computed: {
    ...mapState([
      'basket',
      'is_basket_visible',
      'shipping_cost'
    ]),

    ...mapGetters([
      "basket_total_price"
    ])
  },

  methods: {
    ...mapMutations([
      'REMOVE_VARIANT_FROM_BASKET'
    ]),

    ...mapActions([
      'hideBasketModal',
      'getShippingCost'
    ])
  },

  updated: function() {
    this.getShippingCost();
    console.log("updated")
  }
}
</script>

<style lang="css" scoped>
</style>
