<template lang="html">
  <div class="modal" :class="{'is-active': is_variant_visible}">
    <div class="modal-background"></div>
      <div class="modal-content">
        <!-- Any other Bulma elements you want -->
        <p>keekkchose</p>
      </div>
    <button class="modal-close is-large" aria-label="close" @click="toggleVariantModal"></button>
  </div>
</template>

<script>
import { mapState , mapMutations , mapActions } from 'vuex';
export default {

  computed: {
    ...mapState([
      'is_variant_visible'
    ])
  },

  methods: {
    ...mapActions([
      'toggleVariantModal'
    ])
  }

}
</script>

<style lang="css" scoped>
</style>
