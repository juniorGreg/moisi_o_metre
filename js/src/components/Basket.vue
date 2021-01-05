<template lang="html">
  <div class="modal" :class="{'is-active': is_basket_visible}">
    <div class="modal-background"></div>
      <div class="modal-content">
        <!-- Any other Bulma elements you want -->
        <div class="box">

          <div>
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
                  <button class="delete" @click="removeItem(item)"></button>
              </div>

            </article>

            <nav class="level">
              <div class="level-left">
                <div class="level-item">
                    livraison (estimation):
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
                    {{ basket_total_price + shipping_cost}}
                  </div>
              </div>
            </nav>
          </div>
        <br>


          <div ref="paypal">

          </div>

        </div>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="hideBasketModal"></button>

  </div>
</template>

<script>
import { mapState , mapMutations , mapActions , mapGetters} from 'vuex';

export default {
  data: function() {
    return {
      loaded: false,
      paidFor: false,
    }
  },
  computed: {
    ...mapState([
      'basket',
      'is_basket_visible',
      'shipping_cost'
    ]),

    ...mapGetters([
      "basket_total_price"
    ]),

    checkout_button_msg: function(){
      if(!this.is_checkout){
        return "Passer à la caisse";
      } else {
        return "Retour au panier";
      }
    }
  },

  methods: {
    ...mapMutations([
      'REMOVE_VARIANT_FROM_BASKET'
    ]),

    ...mapActions([
      'hideBasketModal',
      'getShippingCost'
    ]),

    removeItem: function(item){
      this.REMOVE_VARIANT_FROM_BASKET(item);
      this.getShippingCost();
    },

    setLoaded: function() {
      this.loaded=true;
      window.paypal.Buttons({
        createOrder: (data, actions) => {

          return actions.order.create({
            purchase_units: [{
              amount: {
                value: this.basket_total_price + this.shipping_cost
              }
            }]
          });
        },

        onShippingChange: function(data, actions) {
          console.log(data);
        }
      }).render(this.$refs.paypal)
    }
  },

  mounted: function() {
    const script = document.createElement("script")
    script.src =
      "https://www.paypal.com/sdk/js?client-id=AbsjOVQ_dAtj3iG38tPjeASTnduZr3dzwpMA5KH2oxkAGax9rYmp-vCeGac6dtmZbid2v3GSIWUHQXmS"
      script.addEventListener("load", this.setLoaded);
      document.body.appendChild(script);
  },

  updated: function() {

    console.log("updated")
  }
}
</script>

<style lang="css" scoped>
</style>
