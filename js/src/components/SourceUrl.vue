<template lang="html">
  <div v-if="source">
    <h5>{{ title }}</h5>
      <div v-if="source.includes('http')">
          <a target='_blank' :href="source">{{ source }}</a>
      </div>
      <div v-else>
        {{ source }}
      </div>
      <br>
  </div>
</template>

<script>
export default {
  props: ["source", "title"],
}
</script>

<style lang="css" scoped>
</style>
