---
name: "source-command-add-todo"
description: "Add a task to the tracker. Use when the user says \"add a todo\", \"track this\", \"remind me to\", or similar."
---

# source-command-add-todo

Use this skill when the user asks to run the migrated source command `add-todo`.

## Command Template

# Add Todo

1. Read `tasks/todo.md`.
2. Append the new item under **Active** using the format:
   ```
   - [ ] <task description>
   ```
3. Confirm to the user what was added.
