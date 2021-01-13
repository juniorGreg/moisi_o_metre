<template lang="html">
  <div class="modal" :class="{'is-active': is_size_table_visible}">>
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
        ]},
        {
          'Toiles': [
            {'12x12': {'in': '12x12', 'cm': '30x30'}},
            {'16x16': {'in': '12x12', 'cm': '45x45'}}
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
      console.log(sizes)
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
