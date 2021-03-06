import Vue from 'vue';
import Vuex from 'vuex';

import axios from 'axios'

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

Vue.use(Vuex);

export default new Vuex.Store({
  state: () => ({
    posts: [],
    post_ids: [],
    post_index: 0,
    query_active: false,
    is_search_bar_visible: false,
    searched_posts: [],
    searched_word: "",
    searched_post_id: 0,
    searched_post_active: false,
    new_searched_post_active: false,
    dark_mode: false,
    is_snowing: false,
    country_code: "",
    //store states
    is_store: false,
    is_variant_visible: false,
    is_basket_visible: false,
    is_size_table_visible: false,
    is_loading: true,
    selected_product: null,
    selected_variant: null,
    products: [],
    products_count: 0,

    basket: [],

    shipping_cost: 0

  }),
  mutations: {
    ADD_POST: (state, post) => {
      function formatPost(post){

        function showModifiedDate(dateCreated, dateModified){
          var date_created_element = dateCreated.split(" ")
          var date_modified_element = dateModified.split(" ")
          if(date_created_element[0] < date_modified_element[0])
            return true;

          if(date_created_element[1] < date_modified_element[1])
            return true;

          if(date_created_element[2] < date_modified_element[2])
            return true;

          var time_created = date_created_element[3].split(":")
          var time_modified = date_modified_element[3].split(":")

          if(time_created[0] < time_modified[0])
            return true;

          if(time_created[1] < time_modified[1])
            return true;

          return false;
        }

        function formatDate(date){
          var months = ["Janvier", "Février", "Mars", "Avril", "Mai", 'Juin', "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
          var date_element = date.split(" ")
          var month_string = date_element[1];
          var month_index = parseInt(month_string);

          var new_date = date.replace(month_string, months[month_index - 1]);

          return new_date;
        }

        post.rottenpoint_set = post.rottenpoint_set.sort((a,b) => (a.order > b.order) ? 1 : -1);
        post["show_modified_date"] = showModifiedDate(post.date_created, post.date_modified);
        post.date_created = formatDate(post.date_created);
        post.date_modified = formatDate(post.date_modified);
        post["show_sources"] = false;


        return post
      }



      state.posts.push(formatPost(post))
    },

    SET_COUNTRY_CODE: (state, value) => {
      state.country_code = value;
    },

    SET_POST_IDS: (state, post_ids) => {
      state.post_ids = post_ids
    },

    SET_POST_INDEX: (state, post_index) => {
        state.post_index = post_index
    },

    SET_IS_SEARCH_BAR_VISIBLE: (state, value) => {
      state.is_search_bar_visible = value
    },


    SET_IS_SIZE_TABLE_VISIBLE: (state, value) => {
      state.is_size_table_visible = value
    },

    SET_QUERY_ACTIVE: (state, value) => {
      state.query_active = value
    },

    SET_SEARCHED_POSTS: (state, value) => {
      state.searched_posts = value
    },

    SET_SEARCHED_WORD: (state, value) => {
      state.searched_word = value
    },

    SET_SEARCHED_POST_ACTIVE: (state, value) => {
      state.searched_post_active = value
    },

    SET_NEW_SEARCHED_POST_ACTIVE: (state, value) => {
      state.new_searched_post_active = value
    },

    SET_SEARCHED_POST_ID: (state, value) => {
      state.searched_post_id = value
    },

    SET_DARK_MODE: (state, value) => {
      state.dark_mode = value
      localStorage.setItem("darkMode", JSON.stringify(value));
    },

    SET_IS_SNOWING: (state, value) => {
      state.is_snowing = value
    },

    SET_IS_LOADING: (state, value) => {
      state.is_loading = value;
    },

    SET_IS_BASKET_VISIBLE: (state, value) => {
      state.is_basket_visible = value
    },

    ADD_PRODUCTS: (state, value) => {
      state.products = state.products.concat(value)
      //remove duplicates

      state.products = [...new Set(state.products)]
    },

    SET_PRODUCTS_COUNT: (state, value) => {
      state.products_count = value;
    },

    SET_SELECTED_PRODUCT: (state, value) => {
      state.selected_product = value;
    },

    SET_SELECTED_VARIANT: (state, value) => {
      state.selected_variant = value;
    },

    SET_IS_STORE: (state, value) => {
      state.is_store = value
      if(value)
      {
          var basket = localStorage.getItem("basketMoisi");
          if(basket){
            state.basket = JSON.parse(basket);
          }
      }

    },

    ADD_VARIANT_TO_BASKET: (state, variant) => {
      state.basket.push(variant);
      localStorage.setItem("basketMoisi", JSON.stringify(state.basket));
    },

    REMOVE_VARIANT_FROM_BASKET: (state, deleted_variant) => {
        state.basket = state.basket.filter(function(variant){
            return variant.id !== deleted_variant.id;
        })

        localStorage.setItem("basketMoisi", JSON.stringify(state.basket));


    },

    CLEAR_BASKET: (state) => {
      while(state.basket.length > 0){
        state.basket.pop();
      }

      state.shipping_cost = 0;
      localStorage.setItem("basketMoisi", JSON.stringify(state.basket));
    },

    SET_IS_VARIANT_VISIBLE: (state, value) => {
      state.is_variant_visible = value
    },

    SET_SHIPPING_COST: (state, value) => {
      state.shipping_cost = value
    }



  },
  actions: {
    getPost: (context, id) => {

      axios.get("/posts/"+id).then(
        response => {
          context.commit("ADD_POST", response.data);
        })
    },

    getNextPost: (context) => {
      if(context.state.query_active)
        return;

      context.commit("SET_QUERY_ACTIVE", true);

      if(context.state.post_index < context.state.post_ids.length){
        var id = context.state.post_ids[context.state.post_index]
        return context.dispatch('getPost', id).then(() => {
          var newIndex = context.state.post_index + 1;
          context.commit("SET_POST_INDEX", newIndex);          

        }).finally(() => {
          setTimeout(() => {
              context.commit("SET_QUERY_ACTIVE", false);
          }, 1000)

        })
      }
    },

    getSearchedPost: (context, id) => {
        context.commit("SET_SEARCHED_POST_ID", id);

        var posts = context.state.posts.filter((post) => {
          return post.id === id;
        })

        if(posts.length > 0){
          context.commit("SET_SEARCHED_POST_ACTIVE", true);
          context.commit("SET_IS_SEARCH_BAR_VISIBLE", false);
          return
        }


        return context.dispatch("getPost", id).then(()=>{

          var post_ids = context.state.post_ids.filter(
            function(post_id){
              return post_id !== id
            }
          )

          context.commit("SET_POST_IDS", post_ids);
          context.commit("SET_NEW_SEARCHED_POST_ACTIVE", true);
          context.commit("SET_IS_SEARCH_BAR_VISIBLE", false);


        })
    },

    fetchSearchedPosts: (context) => {

      var word = context.state.searched_word;
      if(word.length > 0)
      {
        axios.get("/search/"+word).then(
          response => {
             context.commit("SET_SEARCHED_POSTS", response.data)
          }
        )
      }else{
        context.commit("SET_SEARCHED_POSTS", []);
      }
    },

    getCountryCode: (context) => {
      axios.get("/location").then(response => {
          context.commit("SET_COUNTRY_CODE", response.data.country_code);
      })

    },

    showSearchBar: (context) => {
      context.commit("SET_IS_SEARCH_BAR_VISIBLE", true);
    },

    hideSearchBar: (context) => {
      context.commit("SET_IS_SEARCH_BAR_VISIBLE", false);
    },

    showBasketModal: (context) => {
      context.commit("SET_IS_BASKET_VISIBLE", true);
    },

    hideBasketModal: (context) => {
      context.commit("SET_IS_BASKET_VISIBLE", false);
    },

    getDarkMode: (context) => {
      var darkMode = localStorage.getItem("darkMode");
      if(darkMode){
        context.commit("SET_DARK_MODE", JSON.parse(darkMode));
      }
    },

    isSnowing: (context) => {

      var d = new Date();
      var month = d.getMonth();
      var date = d.getDate();

      if((month === 11 && date === 25) ||
          (month === 0 && date === 1)){
        context.commit("SET_IS_SNOWING", true)
      }
    },

    getProducts: (context) => {
      if(context.state.query_active)
        return;

      context.commit("SET_QUERY_ACTIVE", true);

      if(context.state.products.length < context.state.products_count){
        const request_index = context.state.products.length;
        const request_length = 10;
        const request = "/store/products/"+request_index+"/"+request_length;
        axios.get(request).then(response => {
          context.commit("ADD_PRODUCTS", response.data)
        }).finally(() => {
          setTimeout(() => {
              context.commit("SET_QUERY_ACTIVE", false);
          }, 1000)

        })
      }

    },

    showVariantModal: (context, product) => {
      context.commit("SET_SELECTED_PRODUCT", product)
      context.commit("SET_SELECTED_VARIANT", product.variant_set[0])
      context.commit("SET_IS_VARIANT_VISIBLE", true)
    },

    hideVariantModal: (context) => {
      context.commit("SET_IS_VARIANT_VISIBLE", false)
    },

    showSizeTableModal: (context) => {
      context.commit("SET_IS_SIZE_TABLE_VISIBLE", true)
    },

    hideSizeTableModal: (context) => {
      context.commit("SET_IS_SIZE_TABLE_VISIBLE", false)
    },

    getVariantBySizeAndColor: (context, {size, color}) => {
      function isSizeAndColor(variant){
        return variant.size === size && variant.color === color
      }

      function isColor(variant) {
        return variant.color === color;
      }

      const variant = context.state.selected_product.variant_set.find(isSizeAndColor);
      if(variant){
          context.commit("SET_SELECTED_VARIANT", variant)
      }else {
        console.log("variant not found")
        const variant_color = context.state.selected_product.variant_set.find(isColor);
        console.log(variant_color)
        context.commit("SET_SELECTED_VARIANT", variant_color);
      }




    },

    getShippingCost: (context, location = {}) => {
      const itemsSet = new Map()
      const items = []

      if(context.state.basket.length === 0){
        context.commit("SET_SHIPPING_COST", 0.0);
        return;
      }

      context.state.basket.forEach((variant) => {
        const variant_id = variant.variant_id;
        if(itemsSet.has(variant_id)){
          itemsSet.set(variant_id, itemsSet.get(variant_id) + 1)
        }else {
          itemsSet.set(variant_id, 1)
        }
      })

      itemsSet.forEach((quantity, variant_id) => {
          const item = { variant_id: variant_id, quantity: quantity}
          items.push(item);
      });

      const request = {
        recipient: location,
        items: items
      }


      return axios.post("/store/shipping_cost", request).then(response => {
        const shipping_rates = response.data

        const standard_shipping_rate = shipping_rates.filter(shipping_rate => shipping_rate.id == "STANDARD")

        context.commit("SET_SHIPPING_COST", Number(response.data[0].rate));
      })

    },

    setUpStore: (context) => {
      context.commit("SET_IS_STORE", true);
      context.dispatch("getShippingCost");
    },

    createOrder: (context, order) => {
      const itemsSet = new Map()
      const items = []

      context.state.basket.forEach((variant) => {
        const id = variant.id;
        if(itemsSet.has(id)){
          itemsSet.set(id, itemsSet.get(id) + 1)
        }else {
          itemsSet.set(id, 1)
        }
      })

      itemsSet.forEach((quantity, id) => {
          const item = { sync_variant_id: id, quantity: quantity}
          items.push(item);
      });

      order.order.items = items;

      return axios.post('/store/order', order)

    },


  },
  getters: {
      variant_colors: state => {
        if(state.selected_product){
          return [ ...new Set(state.selected_product.variant_set.map((variant) => {

            return variant.color;
          }))]
        }


        return []
      },

      variant_sizes: state => {


        if(state.selected_product){
          let selected_variant = state.selected_product.variant_set[0]
          if(state.selected_variant){
            selected_variant = state.selected_variant;
          }

          return [ ...new Set(state.selected_product.variant_set.filter((variant) => {
            return variant.color === selected_variant.color;
          }).map((variant) => {

              return variant.size;

          }))].sort((a, b) => {
            var sizes_order = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', 'S/M', 'L/XL']

            var orderA = sizes_order.indexOf(a)
            var orderB = sizes_order.indexOf(b)

            //if size on in list sort alphabeticly
            if(orderA  === -1 && orderB === -1){
              if(a < b){
                return -1
              }
              else if(a > b){
                return 1
              }
              else {
                return 0;
              }
            }

            if(orderA > orderB) {
              return 1;
            }

            else if(orderA < orderB) {
              return -1;
            }

            else {
              return 0
            }


          })
        }

        return []
      },

      basket_items_count: (state) => {
        return state.basket.length
      },

      basket_total_price: state => {
        return state.basket.reduce(( total, { price }) => total + price, 0);
      }


  }
});
