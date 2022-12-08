<template>
  <div class="particles-js-box">
    <div id="particles-js"></div>
  </div>
</template>
<script>
/* eslint-disable */
import particlesJs from "./particles.js";
import particlesConfig from "./particles.json";
export default {
  data() {
    return {};
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      particlesJS("particles-js", particlesConfig);
      document.body.style.overflow = "hidden";
    },
  },
};
</script>
<style scoped>
.particles-js-box {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -1;
}
#particles-js {
  /* background-color: #13181b; */
  background-image: url("../assets/Login_BGP8.jpg");
  background-position: center;
  background-repeat: no-repeat;
  background-size: 150%;
  width: 100%;
  height: 100%;
}
</style>