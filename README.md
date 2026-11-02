# Cangyun Design Anything

面向 Codex 与 Claude Code 的设计工作流 skill 骨架，等待填充内容。目前尚未实现具体设计能力，也未安装到本机的 skill 目录。

## 从这里开始

编辑 [SKILL.md](SKILL.md)，补充适用场景、输入、工作流程和交付标准，再把顶部 `description` 改成准确的能力与触发条件。各处 `TODO` 注释是刻意保留的填写提示，完成后可删除。同步更新 [agents/openai.yaml](agents/openai.yaml) 中的展示文案。

```text
cangyun-design-anything/
├── SKILL.md              # 两种工具共用的 skill 入口
├── agents/openai.yaml    # Codex 的可选展示元数据
├── references/           # 按需读取的参考资料
├── scripts/              # 后续需要时添加的辅助脚本
├── assets/               # 模板、图片等输出素材
├── README.md
└── .gitignore
```

三个资源目录暂用 `.gitkeep` 保留；没有实际用途的目录可删除。添加资源后，在 `SKILL.md` 中写明相对路径及使用条件。

## 兼容方式

`SKILL.md` 只使用通用的 `name`、`description` YAML 字段和 Markdown 正文，两种工具读取同一份内容。Codex 的展示配置单独放在 `agents/openai.yaml`；共享正文暂不依赖特定产品的工具名、参数替换语法或本机绝对路径。

安装位置参考 [Codex 官方文档](https://learn.chatgpt.com/docs/customization/overview#skills)和 [Claude Code 官方文档](https://code.claude.com/docs/en/skills)：

| 工具 | 个人安装目录 | 项目安装目录 |
| --- | --- | --- |
| Codex | `~/.agents/skills/cangyun-design-anything/` | `.agents/skills/cangyun-design-anything/` |
| Claude Code | `~/.claude/skills/cangyun-design-anything/` | `.claude/skills/cangyun-design-anything/` |

## 内容完善后的本地安装

在 macOS / Linux 上，可把这个工作副本链接到两个个人安装目录，让后续编辑保持同步。下面的命令仅在目标不存在时创建链接，保留已有目录或链接。

```sh
skill_repo="$HOME/projects/skill-repos/cangyun-design-anything"
for skill_root in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
  mkdir -p "$skill_root"
  skill_target="$skill_root/cangyun-design-anything"
  if [ ! -e "$skill_target" ] && [ ! -L "$skill_target" ]; then
    ln -s "$skill_repo" "$skill_target"
  fi
done
```

也可以把整个 skill 目录复制到所选安装位置。安装后，在对应工具的新会话中确认该 skill 已被发现，并用真实任务验证流程与交付物。
