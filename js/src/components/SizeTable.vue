<template lang="html">
  <section class="modal" :class="{'is-active': is_size_table_visible}">>
    <div class="modal-background"></div>
      <div class="modal-content">
          <div class="box">
            <h1 class="subtitle">Tableau des tailles</h1>

            <div class="table-container" v-for="size in sizes" >
              <h2 class="subtitle is-size-6"> {{ Object.keys(size)[0] }} </h2>
              <table  class="table is-narrow is-size-7">
                  <thead>

                    <tr>
                      <th></th>
                      <th v-for="sub_size in sub_sizes(size)">{{ sub_size }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="mesure in  mesures">
                      <th>{{ mesure.name }}</th>
                      <td v-for="size_name in sub_sizes(size)">
                        {{ getMesureItem(size, size_name, mesure.key ) }}
                      </td>
                    </tr>
                  </tbody>
              </table>


            </div>



          </div>

      </div>
      <button class="modal-close is-large" aria-label="close" @click="hideSizeTableModal"></button>
  </section>
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
        ]},
        {'Casquette': [
            {'S/M': {'in': '21 ¼-22 ¾', 'cm': '54-57.8'}},
            {'L/XL': {'in': "22 ⅜-23 ⅞", "cm": '56.8-60.6'}}
        ]},
        { 'Autocollant': [
          {'3x3': {'in': '3', 'cm': '7.5'}},
          {'4x4': {'in': '4', 'cm': '10'}},
          {'5.5x5.5': {'in': '5 ½', 'cm': '14'}},
        ]},
        {
          'Toiles': [
            {'12x12': {'in': '12x12', 'cm': '30.5x30.5'}},
            {'12x16': {'in': '12x16', 'cm': "30.5x40.6"}},
            {'16x16': {'in': '16x16', 'cm': '40.6x40.6'}},
            {'16x20': {'in': '16x20', 'cm': '40.6x50.8'}},
            {'18x24': {'in': '18x24', 'cm': '45.7x61'}},
            {'24x36': {'in': '24x36', 'cm': '61x91.4'}}
          ]}

      ],

      mesures: [{name: "Pouces", key: 'in'}, {name: "Centimètres", key: 'cm'}]

    }
  },

  computed: {
    ...mapState([
      "is_size_table_visible"
    ]),


  },

  methods: {
    ...mapActions([
      'hideSizeTableModal'
    ]),

    sub_sizes: function(object){
      const list_sizes = Object.values(object)[0]

      const sizes = list_sizes.map( sub_size => {

        const key =Object.keys(sub_size)[0]

        return key
      })

      return sizes;
    },

    getMesureItem: function(object, size_name, mesure_key){
      const list_sizes = Object.values(object)[0]

      const mesure_item = list_sizes.filter( sub_size => {
        const key_size = Object.keys(sub_size)[0]
        return (key_size === size_name)
      })[0]
      return mesure_item[size_name][mesure_key];
    }
  }
}
</script>

<style lang="css" scoped>
</style>
