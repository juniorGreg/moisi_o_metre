<template lang="html">
  <div class="modal" :class="{'is-active': is_size_table_visible}">>
    <div class="modal-background"></div>
      <div class="modal-content">
          <div class="box">
            <h1 class="subtitle">Tableau des tailles</h1>

          </div>

      </div>
      <button class="modal-close is-large" aria-label="close" @click="hideSizeTableModal"></button>
  </div>
</template>

<script>

import { mapState , mapMutations , mapActions , mapGetters} from 'vuex';

export default {

  data: function(){
    return {
      sizes: [
        {'T-shirt et gilet (Poitrine)': [
          {'XS': {'in': '31-34', 'cm': '79-86'}},
          {'S': {'in': '34-37', 'cm': '86-94'}},
          {'M': {'in': '38-41', 'cm': '96-104'}},
          {'L': {'in': '42-45', 'cm': '107-114'}},
          {'XL': {'in': '46-49', 'cm': '117-124'}},
          {'2XL': {'in': '50-53', 'cm': '127-135'}},
          {'3XL': {'in': '54-57', 'cm': '137-145'}},
          {'4XL': {'in': '58-51', 'cm': '147-155'}}
        ]}
      ]

    }
  },

  computed: {
    ...mapState([
      "is_size_table_visible"
    ])
  },

  methods: {
    ...mapActions([
      'hideSizeTableModal'
    ])
  }
}
</script>

<style lang="css" scoped>
</style>
