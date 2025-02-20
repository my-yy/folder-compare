<template>
  <div>
    <div class="top_bar">
      <el-button @click="$router.push('/collection/')">NewCollection</el-button>
      <el-button @click="onNewCkptCollection">NewCkptCollection</el-button>
    </div>
    <div class="the_item_wrapper">
      <div v-for="item in collection_list" class="single_item">
        <div>
          <span class="created_date">{{ formateDate(item.created_date) }}</span>
          <span v-if="item.content_type==='ckpt'" style="color: #42b983">【CKPT】</span>
          <span class="name_link" @click="onLinkNameClick(item)">{{ item.name }}</span>

        </div>
      </div>
    </div>


  </div>
</template>

<script>
import web_util from "@/utils/web_util";
import moment from 'moment'

export default {
  name: 'Empty',
  components: {},
  props: [],
  data() {
    return {
      collection_list: []
    }
  },
  async mounted() {
    console.log("get data...")
    const {data} = await web_util.getHttp().post("/get_all_collection")
    console.log(data)
    data.reverse()
    this.collection_list = data
  },
  methods: {
    onLinkNameClick(item) {
      if (item.content_type === "ckpt") {
        this.$router.push('/figure/' + item.id)
        return
      }

      if (item.raw_folders) {
        this.$router.push('/raw/' + item.id)
      } else {
        this.$router.push('/collection/' + item.id)
      }
    },
    formateDate(date) {
      return moment(date).format('YYYY-MM-DD');
    },
    async onNewCkptCollection() {
      const re = await web_util.getHttp().post("/new_collection", {
        name: "未命名:" + new Date().getTime(),
        content_type: "ckpt"
      })
      this.$router.push('/figure/' + re.data.id)
    }

  }
}
</script>
<style scoped>

.single_item {
  margin-bottom: 1em;
}

.created_date {
  margin-right: 10px;
  color: #999999;
}

.name_link {
  cursor: default;
}

.name_link:hover {
  text-decoration: underline;
}

.top_bar {
  text-align: center;
  margin-bottom: 10px;
}

.the_item_wrapper {
  margin-left: 20vw;
  max-height: calc(100vh - 80px);
  overflow-y: auto;
}
</style>

