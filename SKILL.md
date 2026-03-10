# CRUD Code Generator

自动实现增改删查（CRUD）代码的 AI 技能。

## 触发条件

当用户提到以下关键词时自动触发：
- "增删改查"、"CRUD"
- "创建接口"、"添加接口"
- "生成 API"、"自动生成代码"
- "数据库操作"、"数据模型"

## 功能说明

此技能可以帮助 AI 自动生成以下代码：

### 1. Create（增）
- 数据库插入操作
- API 创建接口
- 表单提交处理

### 2. Read（查）
- 数据库查询操作
- API 列表/详情接口
- 分页查询
- 条件筛选

### 3. Update（改）
- 数据库更新操作
- API 更新接口
- 部分字段更新

### 4. Delete（删）
- 数据库删除操作
- API 删除接口
- 批量删除
- 软删除

## 使用方法

```
用户: 帮我生成用户模块的 CRUD 代码
AI: [自动识别项目结构，生成相应的增删改查代码]
```

## 输出格式

根据项目技术栈自动选择合适的模板：
- **后端**: Controller, Service, Repository, Model
- **前端**: API 调用, 组件, 类型定义

## 配置选项

可在 `config.json` 中配置：
- `language`: 编程语言（默认自动检测）
- `framework`: 使用的框架
- `database`: 数据库类型
- `style`: 代码风格（restful/graphql/rpc）

## 示例

输入：
```
为 Product 实体生成 CRUD 接口
字段：id, name, price, stock, createdAt
```

输出：
- `product.controller.ts` - 控制器
- `product.service.ts` - 服务层
- `product.model.ts` - 数据模型
- `product.routes.ts` - 路由定义

---

*此技能持续优化中，欢迎反馈改进建议。*