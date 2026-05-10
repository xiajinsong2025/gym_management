<template>
  <div style="height: 100%; display: grid; place-items: center">
    <el-result icon="warning" title="403" sub-title="无权限访问该页面">
      <template #extra><el-button type="primary" @click="$router.push('/')">返回首页</el-button></template>
    </el-result>
  </div>
</template>
