<template>
  <div class="home">
    <div class="topbar">
      <div>
        <el-button size="small" @click="$router.push('/')" icon="el-icon-s-home"></el-button>
        <el-button size="small" @click="onSearch" icon="el-icon-search"></el-button>
        <el-button size="small" @click="createFolder" icon="el-icon-plus"></el-button>
      </div>
      <div>
        <div v-if="collection" class="title_bar">
          <div>{{ collection.name }}
            <el-link icon="el-icon-edit-outline" @click="updateCollection"></el-link>
            <el-link v-if="show_save_icon" icon="el-icon-document-checked" style="margin-left: 1em;"
                     @click="saveCollection"></el-link>
          </div>
          <div class="desc">{{ collection.desc }}</div>
        </div>
      </div>
      <div>
        <el-button size="small" v-if="!collection" @click="newCollection">NewCollection</el-button>
      </div>
    </div>


    <div class="column_wrapper">
      <MyTableView :all_data="column_list" @close_folder="onCloseFolder" @edit_folder="onEditFolder"/>
    </div>

    <FolderDialog ref="FolderDialog"/>
    <CollectionDialog ref="CollectionDialog"/>
    <SearchFolderDialog ref="SearchFolderDialog" @select="onAddFolder"/>
  </div>
</template>

<script>
import web_util from "@/utils/web_util";
import LazyAudio from "@/components/LazyAudio.vue";
import FolderDialog from "@/components/FolderDialog.vue";
import CollectionDialog from "@/components/CollectionDialog.vue";
import SearchFolderDialog from "@/components/SearchFolderDialog.vue";
import MyTableView from "@/components/MyTableView.vue";

export default {
  name: 'HomeView',
  components: {
    FolderDialog, LazyAudio, CollectionDialog, SearchFolderDialog, MyTableView
  },
  props: ['id'],
  data() {
    return {
      collection: null,
      column_list: [],
      all_folders: [],
      options: [],
      show_save_icon: false,
    }
  },
  async mounted() {

    this.refreshOptionList()

    if (!this.id) {
      return
    }

    //1. 获取collection
    const {data} = await web_util.getHttp().post("/get_collection", {'id': parseInt(this.id)})
    this.collection = data

    //2. 获取collection的folder
    const re = await web_util.getHttp().post("/get_folders_of_collection", {'id': parseInt(this.id)})
    for (const item of re.data) {
      await this.onAddFolder(item, true)
    }
  },
  computed: {},
  methods: {
    async saveCollection() {
      // ids字段
      this.collection.ids = this.column_list.map(obj => obj.id)

      // order_text 字段
      this.collection.folder_order = JSON.stringify(this.column_list.map(obj => obj.id))

      try {
        await web_util.getHttp().post("/update_collection", this.collection)
      } catch (e) {
        this.$message.error("error" + e)
        return
      }
      this.$message.success("save success")
      this.show_save_icon = false
    },
    async onAddFolder(f, is_init_add = false) {
      // console.log("onAddFolder", f)
      try {
        const {data} = await web_util.getHttp().post("/parse_folder", {'id': f.id})
        this.column_list.push(data)
      } catch (e) {
        console.log('error for loading folder', f)
        console.log(e)
        this.$message.error("error" + e)
      }
      if (!is_init_add) {
        //不是开始时的加载，而是后期的增加
        this.show_save_icon = true
      }
    },
    async onSearch() {
      this.$refs.SearchFolderDialog.show()
    },
    async refreshOptionList() {
      const {data} = await web_util.getHttp().post("/get_all_folder")
      this.all_folders = data
      //创建options
      this.options = this.all_folders.map(item => {
        let label = item.custom_name || item.name
        if (item.desc) {
          label = label + " " + item.desc
        }

        return {
          value: item.path,
          label: label
        }
      })
    },
    async createFolder() {
      const obj = await this.$refs.FolderDialog.newFolder()
      const re = await web_util.getHttp().post("/parse_folder", {'id': obj.id})
      this.column_list.push(re.data)
      this.$refs.SearchFolderDialog.refreshOptionList()
    },
    async onEditFolder(column) {
      const data = await this.$refs.FolderDialog.editFolder(column)
      this.$refs.SearchFolderDialog.refreshOptionList()
    },
    onCloseFolder(column) {
      //从this.column_list中删除column
      this.column_list = this.column_list.filter(item => item !== column)
      this.show_save_icon = true
    },

    async newCollection() {
      const data = await this.$refs.CollectionDialog.newCollection(this.column_list)
      console.log("data", data)
      this.$router.replace("/collection/" + data.id)
      this.collection = data
    },
    async updateCollection() {
      this.$refs.CollectionDialog.updateCollection(this.collection, this.column_list)
    }
  }
}
</script>
<style scoped>

.topbar {
  display: flex;
  margin-bottom: 10px;
}

.topbar > div {
  flex: 1;
}

.title_bar {
  text-align: center;
}

.title_bar > .desc {
  font-size: small;
  color: gray;
  white-space: pre-wrap;
}

.folder_input input {
  width: 80vw;
}

.input_wrapper {
  display: flex;
  flex-direction: row;
  margin-bottom: 10px;
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
  /*white-space: nowrap; !* 确保文本在一行内显示 *!*/
  /*overflow: hidden; !* 隐藏超出部分 *!*/
  /*text-overflow: ellipsis; !* 当文本被截断时显示省略号 *!*/
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

.item_list2 {
  border: 1px black solid;
  overflow-y: auto;
  max-height: calc(100vh - 200px);
}


.column_name {
  font-size: xx-small;
  font-weight: bold;
  width: 100%; /* 或者你可以设置一个固定宽度 */
  white-space: nowrap; /* 确保文本在一行内显示 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 当文本被截断时显示省略号 */
}

.single_wav_score {
  font-size: small;
}

</style>
