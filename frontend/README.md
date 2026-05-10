# 健身房管理系统前端

基于 Vue 3 + Vite + Vuetify 3 的单店健身房管理系统前端。

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Vuetify 3** - Material Design 组件框架
- **TypeScript** - 类型安全
- **Pinia** - Vue 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP 客户端

## 功能模块

### 已实现

1. **登录认证**
   - 用户登录
   - JWT Token 管理
   - 权限控制

2. **会员管理**
   - 会员列表（分页、搜索、筛选）
   - 新增会员
   - 编辑会员
   - 查看会员详情

3. **卡务交易**
   - 卡种管理
   - 会员卡管理
   - 交易记录

4. **课程管理**
   - 课程列表
   - 排期管理
   - 预约记录

5. **私教管理**
   - 私教课包管理
   - 排课记录

## 开发运行

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 接口
│   ├── components/       # 公共组件
│   ├── plugins/          # 插件配置
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia 状态管理
│   ├── types/            # TypeScript 类型定义
│   ├── utils/            # 工具函数
│   ├── views/            # 页面组件
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── public/               # 静态资源
└── index.html            # HTML 模板
```

## API 配置

前端通过 Vite 代理连接后端 API：

- 前端地址：`http://localhost:3000`
- 后端地址：`http://localhost:8000`
- API 前缀：`/api/v1`

## 开发说明

1. 确保后端服务已启动（默认端口 8000）
2. 登录时会自动授予所有权限（开发环境）
3. Token 存储在 localStorage 中
4. 所有 API 请求自动携带 Token

## 后续优化

- [ ] 完善卡务交易模块的 CRUD 功能
- [ ] 完善课程管理的预约功能
- [ ] 完善私教管理的排课消课功能
- [ ] 添加前台管理模块
- [ ] 添加报表统计模块
- [ ] 添加营销活动模块
- [ ] 优化 UI/UX
- [ ] 添加单元测试
- [ ] 添加 E2E 测试
