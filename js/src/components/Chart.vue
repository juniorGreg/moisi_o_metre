<template lang="html">
  <div class="">
    <p>Chart</p>
    <canvas ref="chart" width="400" height="400"></canvas>
  </div>
</template>

<script>

import Chart from "chart.js";

export default {
  data() {
    return {
      chart: null,
      ctx: null
    }
  },
  mounted: function(){
    this.ctx = this.$refs.chart.getContext('2d');

    this.chart = new Chart(this.ctx,
    {
        type: 'bar',

        data: {
            labels: ["Group 1", 'Group 2'],
            datasets: [{
                label: 'Groups',
                data: [5, 5],
                backgroundColor: ['red', 'blue']

            }]
        },

        options: {
          aspectRatio: 10
        }




    });

    this.$refs.chart.style.height = "30em";
    this.chart.resize();

    //this.chart.update();

  }
}
</script>

<style lang="css" scoped>

</style>
