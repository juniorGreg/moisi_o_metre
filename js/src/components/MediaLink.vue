<template lang="html">
  <article class="media">
    <div class="media-content">
      <div class="content">
        <figure class="image is-16by9">
          <iframe class="has-ratio" :src="mediaLink.video_link" width="640" height="360" frameborder="0" allowfullscreen></iframe>
        </figure>
      </div>
      <nav v-if="isAudioLinked" class="level is-mobile">
        <div class="level-left">
          <span class="level-item is-size-7 has-text-centered">Liens audios: </span>
          <a class="level-item has-text-centered" v-if="mediaLink.spotify_link" :href="mediaLink.spotify_link" target="_blank">
            <figure class="button is-text image is-24x24" data-tooltip="lien audio spotify">
              <img :src="spotify_img" alt="lien audio spotify" >
            </figure>
          </a>
          <a class="level-item has-text-centered" v-if="mediaLink.soundcloud_link" :href="mediaLink.soundcloud_link" target="_blank">
            <figure class="button is-text image is-24x24" data-tooltip="lien audio soundcloud">
              <img :src="soundcloud_img" alt="lien audio soundcloud" >
            </figure>
          </a>
          <a class="level-item has-text-centered" v-if="mediaLink.itunes_link" :href="mediaLink.itunes_link" target="_blank">
            <figure class="button is-text image is-24x24" data-tooltip="lien audio itunes">
              <img :src="itunes_img" alt="lien audio itunes">
            </figure>
          </a>
          <a class="level-item has-text-centered" v-if="mediaLink.google_podcast_link" :href="mediaLink.google_podcast_link" target="_blank">
            <figure class="button is-text image is-24x24" data-tooltip="lien audio google podcast">
              <img :src="google_podcast_img" alt="lien audio google podcast" >
            </figure>
          </a>

        </div>
      </nav>
    </div>
  </article>
</template>

<script>
export default {
  props: ["mediaLink", "spotify_img", "soundcloud_img", "itunes_img", "google_podcast_img"],
  computed: {
    isAudioLinked: function(){
      if(this.mediaLink.spotify_link){
        return true;
      }
      else if(this.mediaLink.soundcloud_link){
        return true;
      }
      else if(this.mediaLink.itunes_link){
        return true;
      }
      else if(this.mediaLink.google_podcast_link){
        return true;
      }
      else{
        return false;
      }
    }
  }
}
</script>

<style lang="css" scoped>
  .content figure {
    margin-left: 0;
    margin-right:0;
  }
</style>
