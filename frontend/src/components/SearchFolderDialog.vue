<template>
  <el-dialog title="FolderSearch" :visible.sync="dialogVisible" width="70%">
    <div>

      <el-input v-model="search_text" placeholder="Search Text..." style="margin-bottom: 10px;"/>

      <div class="item_wrapper">
        <div v-for="f in searchResult" :key="f.id" class="the_item" @click="onItemClick(f)">
          <span class="created_date">{{ formateDate(f.created_date) }}</span>
          <span v-if="f.content_type==='ckpt'" style="color: #42b983">[CKPT]</span>
          <span>{{ f.custom_name || f.name }}</span>
          <span class="desc"> {{ f.desc }}</span>
        </div>
      </div>

    </div>


  </el-dialog>
</template>

<script>
import web_util from "@/utils/web_util";
import moment from "moment/moment";


export default {
  name: 'SearchFolder',
  components: {},
  props: [],
  data() {
    return {
      dialogVisible: false,
      resolve: null,
      all_folders: [],
      search_text: null,
    }
  },
  mounted() {
    // this.dialogVisible = true
    this.refreshOptionList()
  },
  computed: {
    searchResult() {
      if (!this.search_text) {
        return this.all_folders
      }
      return this.all_folders.filter(f => {
        return f.name.includes(this.search_text) || f.custom_name.includes(this.search_text)
      })
    }
  },
  methods: {
    show() {
      this.dialogVisible = true
      return new Promise(((resolve, reject) => {
        this.resolve = resolve
      }))
    },
    async refreshOptionList() {
      const {data} = await web_util.getHttp().post("/get_all_folder")
      this.all_folders = data
    },
    async hide() {
      this.dialogVisible = false
      this.resolve(re.data)
    },
    formateDate(date) {
      return moment(date).format('YYYY-MM-DD');
    },
    onItemClick(f) {
      console.log("onItemClick", f)
      this.$emit('select', f)
    }
  }
}
</script>
<style scoped>

.created_date {
  margin-right: 10px;
  color: #999999;
}

.item_wrapper {
  max-height: 60vh;
  overflow: auto;
}

.desc {
  color: gray;
  font-size: small;
}

.the_item {
  cursor: default;
}

.the_item:hover {
  background-color: #f5f7fa;
  color: red;
}
</style>
