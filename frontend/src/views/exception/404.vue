<template>
  <div style="height: 100%; display: grid; place-items: center">
    <el-result icon="info" title="404" sub-title="页面不存在">
      <template #extra><el-button type="primary" @click="$router.push('/')">返回首页</el-button></template>
    </el-result>
  </div>
</template>
