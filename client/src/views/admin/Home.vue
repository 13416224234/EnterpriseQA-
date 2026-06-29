<template>
  <div class="admin-home">
    <h3 class="page-title">系统概览</h3>
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6" v-for="item in statCards" :key="item.label">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value">{{ item.value }}</div>
          <div class="stat-label">{{ item.label }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header>近7日对话趋势</template>
          <v-chart :option="convChartOption" style="height: 320px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header>文档分类统计</template>
          <v-chart :option="categoryChartOption" style="height: 320px" autoresize />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { adminApi } from "../../api/index.js"
import VChart from "vue-echarts"
import { use } from "echarts/core"
import { CanvasRenderer } from "echarts/renderers"
import { LineChart, PieChart } from "echarts/charts"
import { GridComponent, TooltipComponent, LegendComponent } from "echarts/components"
use([CanvasRenderer, LineChart, PieChart, GridComponent, TooltipComponent, LegendComponent])

const dashboardData = ref({
  user_count: 0, doc_count: 0, conv_count: 0, msg_count: 0,
  category_stats: [], recent_convs: []
})

const statCards = computed(() => [
  { label: "用户总数", value: dashboardData.value.user_count },
  { label: "文档总数", value: dashboardData.value.doc_count },
  { label: "对话总数", value: dashboardData.value.conv_count },
  { label: "消息总数", value: dashboardData.value.msg_count }
])

const convChartOption = computed(() => ({
  tooltip: { trigger: "axis" },
  xAxis: { type: "category", data: dashboardData.value.recent_convs.map(c => c.date) },
  yAxis: { type: "value" },
  series: [{ data: dashboardData.value.recent_convs.map(c => c.count), type: "line",
    smooth: true, areaStyle: { opacity: 0.3 }, lineStyle: { width: 3 }, itemStyle: { color: "#409EFF" } }]
}))

const categoryChartOption = computed(() => ({
  tooltip: { trigger: "item" },
  legend: { orient: "vertical", right: 10, top: "center" },
  series: [{ type: "pie", radius: ["40%", "70%"], center: ["40%", "50%"],
    data: dashboardData.value.category_stats,
    emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: "rgba(0, 0, 0, 0.5)" } } }]
}))

onMounted(async () => {
  try {
    const res = await adminApi.getDashboard()
    if (res.code === 200) dashboardData.value = res.data
  } catch (e) { console.error("获取统计数据失败", e) }
})
</script>

<style scoped>
.page-title { margin: 0 0 16px; font-size: 18px; color: #303133; }
.stat-card { text-align: center; cursor: default; }
.stat-value { font-size: 32px; font-weight: bold; color: #409EFF; }
.stat-label { font-size: 14px; color: #909399; margin-top: 8px; }
</style>
