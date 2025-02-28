<template>
  <el-select v-if="platform" v-model="platform" placeholder="请选择" style="position: fixed;left: 10px;top: 10px;"
             size="small">
    <el-option v-for="item in platform_options" :key="item" :label="item" :value="item">
    </el-option>
  </el-select>

</template>

<script>


export default {
  name: 'Empty',
  components: {},
  props: [],
  data() {
    return {
      platform: null,
      platform_options: [
        "shannon",
        "hamming",
        "kruskal",
      ]
    }
  },
  watch: {
    platform(newVal, oldVal) {
      // 当 platform 发生变化时，这里可以获取新值和旧值
      console.log('新选项:', newVal);
      console.log('旧选项:', oldVal);
      this.onJumpPlatform(newVal, oldVal);
    },
  },
  async mounted() {
    this.platform_options.forEach(s => {
      if (window.location.href.indexOf(s) > 0) {
        this.platform = s
      }
    })
  },
  methods: {
    onJumpPlatform(new_val, old_val) {
      console.log({new_val, old_val})
      console.log(window.location.href)
      window.location.href = window.location.href.replace(old_val, new_val)
    }

  }
}
</script>
<style scoped>

</style>
