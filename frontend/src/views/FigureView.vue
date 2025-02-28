<template>
  <div v-if="collection">
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
          </div>
          <div class="desc">{{ collection.desc }}</div>
        </div>
      </div>
      <div>
      </div>
    </div>


    <div>
      <div v-for="f in folder_list">
        <el-link icon="el-icon-close" @click="onRemoveFolder(f)"></el-link>
        <span> {{ f.name }}</span>
        <el-link icon="el-icon-edit" @click="onEditFolder(f)"></el-link>
      </div>
    </div>
    <div style="text-align: center;">
      <el-radio-group v-model="cur_key" @change="showKey">
        <el-radio-button v-for="key in float_keys" :key="key" :label="key"></el-radio-button>
      </el-radio-group>
    </div>

    <div class="display_wrapper">
      <div ref="chart" style="width: 70vw; height: 60vh;margin: 0 auto"></div>
      <!--      <div class="raw_step_eval_logs">-->
      <!--        <div v-for="obj in obj_list" :key="obj.name">-->
      <!--          {{ obj }}-->
      <!--        </div>-->
      <!--      </div>-->
    </div>
    <FolderDialog ref="FolderDialog"/>
    <CollectionDialog ref="CollectionDialog" @delete="onCollectionDeleted"/>
    <SearchFolderDialog ref="SearchFolderDialog" @select="onAddFolder"/>
  </div>
</template>

<script>
import web_util from "@/utils/web_util";
import * as echarts from 'echarts';
import FolderDialog from "@/components/FolderDialog.vue";
import CollectionDialog from "@/components/CollectionDialogV2.vue";
import SearchFolderDialog from "@/components/SearchFolderDialog.vue";

export default {
  name: 'Empty',
  components: {SearchFolderDialog, CollectionDialog, FolderDialog},
  props: ["id"],
  data() {
    return {
      collection: null,
      folder_list: [],
      float_keys: [],
      cur_key: null,
    }
  },
  async mounted() {
    //1. 获取collection
    const {data} = await web_util.getHttp().post("/get_collection", {'id': parseInt(this.id)})
    this.collection = data

    //2. 获取collection的folder
    const re = await web_util.getHttp().post("/get_folders_of_collection", {'id': parseInt(this.id)})
    this.folder_list = re.data
    const folder_list = re.data
    console.log(this.folder_list)

    //等待页面渲染完成
    await this.$nextTick()

    //3.获得float keys

    let total_float_keys = new Set()
    for (const fobj of this.folder_list) {
      let data
      try {
        const re = await web_util.getHttp().post("/parse_ckpt_folder", {path: fobj.path})
        data = re.data
      } catch (e) {
        continue
      }
      fobj.obj_list = data.list
      const float_keys = data.float_keys
      // console.log("float_keys single:", float_keys)
      float_keys.forEach(s=>total_float_keys.add(s))
      // total_float_keys.add(...float_keys)
    }
    total_float_keys = Array.from(total_float_keys)
    total_float_keys.sort()
    // console.log("total_float_keys", total_float_keys)
    this.float_keys = total_float_keys

    this.cur_key = total_float_keys[0]


    this.chart = echarts.init(this.$refs.chart);
    if (this.cur_key) {
      this.setChartOption()
    }

  },
  methods: {
    showKey(key) {
      this.cur_key = key
      this.setChartOption()

    },
    async onSearch() {
      this.$refs.SearchFolderDialog.show()
    },
    async createFolder() {
      const obj = await this.$refs.FolderDialog.newFolder('ckpt')
      const id = obj.id

      //保存到当前collection中
      await this.addNewFolderIdInCollection(id)
      //3.push进去
      this.folder_list.push(obj)
    },
    async addNewFolderIdInCollection(id) {
      const exist_ids = this.getCollectionFolderIds(this.collection)
      exist_ids.push(id)
      await this.updateCollectionFolderIds(exist_ids)
    },
    async updateCollectionFolderIds(exist_ids) {
      const folder_order = JSON.stringify(exist_ids)
      await web_util.getHttp().post("/update_collection", {id: this.id, folder_order: folder_order})
      this.collection.folder_order = folder_order
    },
    getCollectionFolderIds(collection) {
      const folder_order_str = collection.folder_order
      let exist_ids = []
      if (folder_order_str) {
        exist_ids = JSON.parse(folder_order_str)
      }
      return exist_ids
    },
    async setChartOption() {
      const series = []
      const legendData = []; // 用于存储图例数据
      const legend_selected = {}
      for (const fobj of this.folder_list) {
        // let data
        // try {
        //   const re = await web_util.getHttp().post("/parse_ckpt_folder", {path: fobj.path})
        //   data = re.data
        // } catch (e) {
        //   console.log(e)
        //   this.$message.error("加载失败")
        //   continue
        // }
        const obj_list = fobj.obj_list || []
        // const float_keys = data.float_keys

        const seriesItem = {
          name: fobj.name,
          type: 'line',
          data: obj_list.map(item => [item.step, item[this.cur_key]]),
          // visible: false,
        };
        series.push(seriesItem);
        legendData.push(seriesItem.name); // 将曲线名称添加到图例数据中
        legend_selected[seriesItem.name] = true
      }

      const option = {
        // title: {
        //   text: "seed50_recons_sim"
        // },
        legend: {
          data: legendData, // 使用图例数据
          selected: legend_selected //用于显示，隐藏
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'value',
          name: 'Step',
        },
        yAxis: {
          type: 'value',
          name: this.cur_key
        },
        series: series,
        // dataZoom: [
        //   {
        //     type: 'slider', // 滑动条型
        //     start: 0, // 初始显示范围的起始百分比
        //     end: 100 // 初始显示范围的结束百分比
        //   },
        // ],
        dataZoom: [
          {
            id: 'dataZoomX',
            type: 'slider', // 内置型缩放
            xAxisIndex: [0], // 控制 X 轴
            filterMode: 'filter', // X 轴缩放模式
            start: 0, // 初始显示范围的起始百分比
            end: 100 // 初始显示范围的结束百分比
          },
          {
            id: 'dataZoomY',
            type: 'slider', // 内置型缩放
            yAxisIndex: [0], // 控制 Y 轴
            filterMode: 'empty', // Y 轴缩放模式
            start: 0,
            end: 100
          }
        ]
      };
      this.chart.setOption(option);
    },


    async onRemoveFolder(f) {
      const exist_ids = this.getCollectionFolderIds(this.collection)
      exist_ids.splice(exist_ids.indexOf(f.id), 1)
      await this.updateCollectionFolderIds(exist_ids)
      this.folder_list.splice(this.folder_list.indexOf(f), 1)
    },
    async updateCollection() {
      this.$refs.CollectionDialog.updateCollection(this.collection, this.folder_list)
    },
    async onEditFolder(f) {
      const data = await this.$refs.FolderDialog.editFolder(f)
      // this.$refs.SearchFolderDialog.refreshOptionList()
    },
    async onAddFolder(f) {
      this.folder_list.push(f)
      this.setChartOption()
      await this.addNewFolderIdInCollection(f.id)
    },
    onCollectionDeleted() {
      this.$router.replace("/")
    }
  }
}
</script>
<style scoped>
.display_wrapper {
  display: flex;
  flex-direction: row;
}

.raw_step_eval_logs {
  font-size: small;
}

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

</style>
