<template>
  <div class="home">
    <div>
      <button v-if="!this.id" @click="newCollection">SaveCollection</button>
      <button v-if="this.id" @click="updateCollection">UpdateCollection</button>
    </div>

    <div class="multi_path_wrapper">
      <textarea v-model="raw_folder_text" style="flex: 1;height: 4rem;"/>
      <el-button @click="onSearchRawFolder2">Parse</el-button>
    </div>

    <div class="column_wrapper">
      <div v-for="column in column_list" class="one_column">
        <div class="column_desc">
          <div class="column_name">
            <span>
            {{ column.custom_name || column.name }}
            </span>
          </div>
          <div class="column_info">
            {{ formatKVDict(column.info) }}
          </div>

        </div>

        <div class="item_list">
          <div v-for="item in column.items" class="item">
            <div class="item_name">{{ item.name }}</div>
            <div class="info_text">{{ formatKVDict(item.info) }}</div>
            <LazyAudio :path="item.path"></LazyAudio>
          </div>
        </div>


      </div>
    </div>
    <CollectionDialog ref="CollectionDialog"/>
  </div>
</template>

<script>
import web_util from "@/utils/web_util";
import LazyAudio from "@/components/LazyAudio.vue";
import FolderDialog from "@/components/FolderDialog.vue";
import CollectionDialog from "@/components/CollectionDialog.vue";

export default {
  name: 'HomeView',
  components: {
    FolderDialog, LazyAudio, CollectionDialog
  },
  props: ['id'],
  data() {
    return {
      collection: null,
      column_list: [],
      raw_folder: null,
      raw_folder_text: null,
      multiline_mode: false,
    }
  },
  async mounted() {
    // this.multiline_mode = localStorage.getItem("multiline_mode") === "true"

    if (!this.id) {
      return
    }

    //1. 获取collection
    const {data} = await web_util.getHttp().post("/get_collection", {'id': parseInt(this.id)})
    this.collection = data
    this.raw_folder_text = data.raw_folders

    //2.解析内容
    this.onSearchRawFolder2()
    // this.raw_folder = "/workspace/audio_team/usr/cgy/1_projects/65_cosyvoice-flow/outputs/vq1222-dit-40w/1231_093015_vq1222-dit-40w"
    // this.raw_folder_text = "/workspace/audio_team/usr/cgy/1_projects/65_cosyvoice-flow/outputs/vq1222-dit-40w/1231_093015_vq1222-dit-40w/block_input25"
    // this.raw_folder_text += "\n/workspace/audio_team/usr/cgy/1_projects/65_cosyvoice-flow/outputs/vq1222-dit-40w/1231_093015_vq1222-dit-40w/block_input_10_25_att_mask_69_172"

  },
  computed: {},
  watch: {
    // multiline_mode(newVal) {
    //   localStorage.setItem('multiline_mode', newVal);
    // },
  },
  methods: {
    async onSearchRawFolder2() {
      this.column_list = []
      const text = this.raw_folder_text.trim()
      if (!text) {
        return
      }
      const lines = text.split("\n").map(l => l.trim()).filter(s => s.length > 0)
      for (let line of lines) {
        const arr = line.split(" ").map(l => l.trim()).filter(s => s.length > 0)
        const the_path = arr[0]
        const custom_name = arr[1]
        const {data} = await web_util.getHttp().post("/parse_raw_folder", {'path': the_path})
        data['custom_name'] = custom_name
        this.column_list.push(data)
      }
    },
    async newCollection() {
      const text = this.raw_folder_text.trim()
      this.$refs.CollectionDialog.newCollection([], text)
    },
    async updateCollection() {
      this.collection.raw_folders = this.raw_folder_text
      this.$refs.CollectionDialog.updateCollection(this.collection, [])
    },
    formatKVDict(dict) {
      if (!dict) {
        return null
      }

      const formattedText = Object.entries(dict).map(([key, value]) => {
        try {
          return `${key}:${value.toFixed(2)}`;
        } catch {
          return `${key}:${value}`;
        }
      }).join(';');
      return formattedText
    }
  }
}
</script>
<style scoped>

.folder_input input {
  width: 80vw;
}


.column_wrapper {
  display: flex;
  flex-direction: row;
}


.item {
  margin-bottom: 20px;
  height: 100px;
}

.item_name {
  font-size: xx-small;
  width: 100%; /* 或者你可以设置一个固定宽度 */
  white-space: nowrap; /* 确保文本在一行内显示 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 当文本被截断时显示省略号 */
  color: gray;
}

.one_column {
  width: 300px;
  margin-right: 10px;
}

.column_desc {
  height: 50px;
  margin-bottom: 10px;
}


.column_name {
  font-size: xx-small;
  font-weight: bold;
  width: 100%; /* 或者你可以设置一个固定宽度 */
  white-space: nowrap; /* 确保文本在一行内显示 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 当文本被截断时显示省略号 */
}

.multi_path_wrapper {
  display: flex;
  flex-direction: row;
  font-size: small;
}

.info_text {
  font-size: small;
  color: gray;
}

.column_info {
  font-size: small;
}

</style>
