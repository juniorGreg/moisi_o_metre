import Vue from 'vue';
import Vuex from 'vuex';

import axios from 'axios'

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    posts: [],
    post_ids: [],
    post_index: 0,
    query_active: false,
    isSearchBarVisible: false,
    searched_posts: [],
    searched_word: "",
    searched_post_id: 0,
    searched_post_active: false,
    new_searched_post_active: false,
    dark_mode: false

  },
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

    SET_POST_IDS: (state, post_ids) => {
      state.post_ids = post_ids
    },

    SET_POST_INDEX: (state, post_index) => {
        state.post_index = post_index
    },

    SET_IS_SEARCH_BAR_VISIBLE: (state, value) => {
      state.isSearchBarVisible = value
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
      //console.log(value);
      localStorage.setItem("darkMode", JSON.stringify(value));
    }

  },
  actions: {
    getPost: (context, id) => {


      console.log("next post: "+id)
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

    toggleSearchBar: (context) => {

      var newState = !context.state.isSearchBarVisible;
      context.commit("SET_IS_SEARCH_BAR_VISIBLE", newState);
    },

    getDarkMode: (context) => {
      var darkMode = localStorage.getItem("darkMode");
      if(darkMode){
        context.commit("SET_DARK_MODE", JSON.parse(darkMode));
      }
    }
  },
  getters: {

  }
});
