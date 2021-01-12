<template lang="html">
  <div class="modal" :class="{'is-active': is_basket_visible}">
    <div class="modal-background"></div>
    <div class="modal-content">
        <!-- Any other Bulma elements you want -->
        <div class="box">

          <div v-show="order_process">

            <h1 class="subtitle">Votre panier</h1>
            <article v-for="item in basket" class="media">

              <figure class="media-left">
                <p class="image is-48x48">
                  <img class="no-dark-mode" :src="item.variant_image.thumbnail" alt="image item">
                </p>
              </figure>

              <div class="media-content">
                <div class="content is-size-7">
                  <nav class="level is-mobile">
                    <div class="level-left">
                      <div class="level-item variant-item">
                          {{ item.name }}
                      </div>
                    </div>
                    <div class="level-right">
                      <div class="level-item">
                        ${{ item.price }}
                      </div>
                    </div>
                  </nav>

                </div>

              </div>

              <div class="media-right">
                  <button class="delete is-warning" @click="removeItem(item)"></button>
              </div>

            </article>

            <nav class="level is-mobile">
              <div class="level-left">
                <div class="level-item">
                    livraison (estimation):
                </div>
              </div>

              <div class="level-right">
                  <div class="level-item">
                    ${{ shipping_cost }}
                  </div>
              </div>
            </nav>

            <nav class="level is-mobile">
              <div class="level-left">
                <div class="level-item">
                    coût total:
                </div>
              </div>

              <div class="level-right">
                  <div class="level-item">
                    ${{ basket_total_price + shipping_cost}}
                  </div>
              </div>
            </nav>

            <div ref="paypal"></div>


          </div> <!-- End div order processed -->


          <div v-if="order_success">
            <p>
              La commande a bien été reçu ! D'ici quelques minutes,
              vous devriez recevoir un courriel de confirmation.
            </p>
            <p>
              Merci d'avoir magasiner sur la boutique du MoisiOMètre. :)
            </p>
          </div>


          <div v-if="order_failed">
            <p>
              Désolé, une erreur s'est produite durant l'envoie de votre commande.
              Vous n'avez pas été débité. L'administrateur a été informé de l'accident.
            </p>
            <p>
              SVP, revenez plus tard, le problème devrait être corrigé dans un future très proche.
            </p>

          </div>

        </div><!-- End div box -->

      </div><!-- End -div modal content-->




    <button class="modal-close is-large" aria-label="close" @click="hideBasket"></button>
  </div>



</template>

<script>
import { mapState , mapMutations , mapActions , mapGetters} from 'vuex';

export default {
  props: ["paypal_client_id"],
  data: function() {
    return {
      loaded: false,
      paidFor: false,
      order_success: false,
      order_failed: false,
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


    order_process: function(){
      return !this.order_success && !this.order_failed;
    }
  },

  methods: {
    ...mapMutations([
      'REMOVE_VARIANT_FROM_BASKET',
      'CLEAR_BASKET'
    ]),

    ...mapActions([
      'hideBasketModal',
      'getShippingCost',
      'createOrder',
    ]),

    removeItem: function(item){
      this.REMOVE_VARIANT_FROM_BASKET(item);
      this.getShippingCost();
    },

    hideBasket:  function() {
      this.hideBasketModal();
      this.order_failed = false;
      this.order_success = false;
    },

    setLoaded: function() {
      this.loaded=true;
      window.paypal.Buttons({
        createOrder: (data, actions) => {

          return actions.order.create({
            purchase_units: [{
              amount: {
                currency_code: 'CAD',
                value: this.basket_total_price + this.shipping_cost,
                breakdown: {
                  item_total: {
                    currency_code: 'CAD',
                    value: this.basket_total_price
                  },
                  shipping: {
                    currency_code: 'CAD',
                    value: this.shipping_cost
                  }
                }

              }
            }]
          });
        },

        onShippingChange: (data, actions) => {
          const shipping_address = data.shipping_address
          const location = {
            city: shipping_address.city,
            state: shipping_address.state,
            country_code: shipping_address.country_code,
            zip: shipping_address.postal_code
          }

          const current_shipping_cost = this.shipping_cost;
          console.log(current_shipping_cost);

          this.getShippingCost(location).then(() => {
            if(current_shipping_cost !== this.shipping_cost){
              console.log("new shipping cost")
              return actions.order.patch([
                {
                  op: 'replace',
                  path: '/purchase_units/@reference_id==\'default\'/amount',
                  value: {
                    currency_code: 'CAD',
                    value: this.basket_total_price + this.shipping_cost,
                    breakdown: {
                      item_total: {
                        currency_code: 'CAD',
                        value: this.basket_total_price
                      },
                      shipping: {
                        currency_code: 'CAD',
                        value: this.shipping_cost
                      }
                    }
                  }
                }
              ])
            }
          })


          console.log(location);
        },

        onApprove: (data, actions) => {
          console.log("Approuve")
          console.log(actions)
          return actions.order.get().then((details) => {
            console.log(details);
            const shipping = details.purchase_units[0].shipping;
              const order = {
                paypal_id: details.id,
                total_cost: details.purchase_units[0].amount.value,
                order: {
                  recipient: {
                    name: shipping.name.full_name,
                    address1: shipping.address.address_line_1,
                    address2: shipping.address.address_line_2,
                    city: shipping.address.admin_area_2,
                    state_code: shipping.address.admin_area_1,
                    country_code: shipping.address.country_code,
                    zip: shipping.address.postal_code,
                    email: details.payer.email_address

                  },
                  items: []
                }
              }

              return this.createOrder(order).then(() => {
                return actions.order.capture().then((details) => {
                  console.log(details);
                  this.order_success = true;
                  this.CLEAR_BASKET();
                })
              }).catch(() => {
                this.order_failed = true;
              });
        });
      }

      }).render(this.$refs.paypal)
    }
  },

  mounted: function() {
    const script = document.createElement("script")
    const paypal_src_url="https://www.paypal.com/sdk/js?currency=CAD&client-id="+this.paypal_client_id;
    script.src = paypal_src_url;

    script.addEventListener("load", this.setLoaded);
    document.body.appendChild(script);
    console.log("basket: "+this.basket.length);
    if(this.basket.length > 0){
      this.getShippingCost();
    }
  }


}
</script>

<style lang="css" scoped>
@media screen and (max-width:600px){
  .variant-item{
    width: 50vw;
    overflow-wrap: break-work;
  }
}


</style>
