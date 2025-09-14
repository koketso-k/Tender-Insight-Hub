Team Workspaces Module

Overview
The Workspaces module enables team collaboration around tenders.  
A workspace acts as a shared space where members can:
- Link tenders or external resources ("Project Links")
- Share notes with collaborators
- Manage workspace membership (Owner, Editor, Viewer)

Entities
Workspace
- `id`: UUID
- `name`: string
- `description`: optional text
- `created_by`: user_id
- `created_at`, `updated_at`

Membership
- `id`
- `workspace_id` (FK → Workspace)
- `user_id` (FK → User)
- `role`: enum(`owner`, `editor`, `viewer`)

Note
- `id`
- `workspace_id` (FK → Workspace)
- `title`
- `content` (text/markdown)
- `created_by`
- `updated_at`

Project Link
- `id`
- `workspace_id` (FK → Workspace)
- `link_type`: enum(`tender`, `url`, `document`)
- `reference`: string (tender_id, URL, or file path)
- `added_by`
- `created_at`

API Endpoints
Workspaces
- `POST /workspaces` → Create
- `GET /workspaces` → List user workspaces
- `GET /workspaces/{id}` → Details
- `PUT /workspaces/{id}` → Update
- `DELETE /workspaces/{id}` → Delete

Members
- `POST /workspaces/{id}/members`
- `GET /workspaces/{id}/members`
- `DELETE /workspaces/{id}/members/{user_id}`

Notes
- `POST /workspaces/{id}/notes`
- `GET /workspaces/{id}/notes`
- `PUT /workspaces/{id}/notes/{note_id}`
- `DELETE /workspaces/{id}/notes/{note_id}`

Project Links
- `POST /workspaces/{id}/links`
- `GET /workspaces/{id}/links`
- `DELETE /workspaces/{id}/links/{link_id}`

Permissions
- **Owner**: full access (edit, delete, manage members)
- **Editor**: can add/edit notes & links
- **Viewer**: read-only access
