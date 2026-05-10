# API Conventions

## 1. 基础路径

- API 前缀：`/api/v1`

## 2. 统一响应结构

成功与失败都遵循统一 JSON 结构：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

业务错误示例：

```json
{
  "code": 40301,
  "message": "permission denied",
  "data": null
}
```

## 3. 分页约定

列表接口统一使用：

- `page`：页码，从 `1` 开始
- `page_size`：每页条数，当前实现普遍上限为 `100`

分页响应：

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

## 4. 鉴权约定

- 登录接口：`POST /api/v1/auth/login`
- 业务接口通过 `Authorization: Bearer <token>` 传递 JWT
- 未登录：返回 HTTP `401`
- 无权限：返回 HTTP `403` + `code=40301`

## 5. 权限码约定

采用 `<resource>:<action>`：

- `members:read` / `members:write`
- `transactions:read` / `transactions:write`
- `courses:read` / `courses:write`
- `pt:read` / `pt:write`
- `frontdesk:read` / `frontdesk:write`
- `reports:read`
- `marketing:read` / `marketing:write`

## 6. 常见业务错误码

- `40401` member not found
- `40301` permission denied
- `40051` member already checked in
- `40052` checkin already checked out
- `40053` bracelet already borrowed

说明：错误码会随着模块扩展增加，建议前端按 `code` 做分支处理，`message` 只做展示。
