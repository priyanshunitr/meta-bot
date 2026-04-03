# 📘 Meta Setup Guide (Instagram Comment Automation)

## 1. 🧩 Meta App Creation

Create an app from **Meta for Developers**:
- **App Type:** Business
- **Add product:** Instagram Graph API

*Note: Adding the product alone is not enough — permissions and linking are required.*

## 2. 🔐 Permissions (Scopes)

When generating access tokens, ensure the following permissions are granted:

**Instagram**
- `instagram_basic`
- `instagram_manage_comments`
- `instagram_manage_messages` *(optional, for DMs)*

**Facebook Page**
- `pages_show_list`
- `pages_read_engagement`

## 3. 🔗 Account Linking (Critical Requirement)

Your setup must follow this chain:
**Instagram Account → Facebook Page → Access Token**

**Requirements:**
- Instagram account must be a **Business** OR **Creator** account.
- Instagram must be linked to a **Facebook Page**.

### 📍 Where to link
In Facebook Page settings:
`Settings → Linked Accounts → Instagram`

### ⚠️ Common Issues
If not linked properly:
- Instagram data will not be accessible via API.
- API may return: "Missing fields" or "Object does not exist" errors.

## 4. 🔑 Access Token Flow

**Important concept:** There are multiple token types:

| Token Type | Purpose |
| ---------- | ------- |
| **User Token** | Represents your Facebook account |
| **Page Token** | Represents your Facebook Page |
| **App Token**  | Internal app usage |

**Required for this project:**
✅ **Page Access Token**

**Token flow:**
`User Token → Fetch Pages → Get Page Token → Use Page Token`

### ⚠️ Important Notes
- Tokens must be generated after permissions are granted.
- If permissions change → regenerate token.
- If Instagram is linked later → regenerate token.

## 5. 🌐 Webhook Setup

Configure webhook in your Meta App:

**Required fields:**
- **Callback URL:** your backend endpoint
- **Verify Token:** your custom string

**Subscribe to:**
- `comments` ✅ *(required for this project)*

**Verification signal:**
- Meta sends a verification request.
- Your server must respond correctly.
- After setup, events will start flowing.

## 6. 📩 Webhook Behavior

Meta webhooks follow an **At-least-once delivery model**.
This means:
- Duplicate events may occur.
- Events may arrive multiple times.
- Delivery is reliable but not unique.

## 7. 🔄 Event Types

For Instagram comment automation:
- **New comment:** triggers webhook.
- **Replies** *(including your bot replies)*: also trigger webhook.

### ⚠️ Important implication
Your system must distinguish between:
1. Top-level comments
2. Replies to comments

## 8. 🧠 Understanding `me`

In Meta APIs, `me` refers to the entity tied to the access token.

With **Page Token**:
`me` = Facebook Page

**Important:** `me` is NOT:
- Instagram account ID
- Comment ID
- Media ID

## 9. 🚨 Common Errors & Causes

❌ **“Unsupported post request (me)”**
- **Cause:** Using `me` where a specific object ID is required.

❌ **“Object does not exist”**
- **Cause:**
  - Instagram not linked to Page
  - Wrong token used
  - Missing permissions

❌ **Empty Page List**
- **Cause:**
  - Missing `pages_show_list`
  - Not admin of the page
  - Wrong Facebook account used

## 10. 🧩 System Relationship Model

```text
Facebook User
   ↓
Facebook Page
   ↓
Instagram Business Account
   ↓
Media (posts)
   ↓
Comments
   ↓
Replies
```

## 11. 🚀 Development vs Production

| Mode | Access |
| ---- | ------ |
| **Development** | Only app admins/testers |
| **Production** | Public users |

**Important:** App Review is NOT required for development/testing. Required only when going public.

## 🎯 Key Takeaways
- Meta APIs are relationship-based.
- Access depends on:
  - Correct linking
  - Correct token
  - Correct permissions
- Webhooks are not guaranteed once.
- Always verify the full chain: `Instagram ↔ Page ↔ Token`


# 📡 Meta Graph API – Endpoint Cheat Sheet

## 🔑 Identity & Tokens

### 🔹 `/me`
👉 **Returns the identity tied to your access token**
- With **User Token** → your Facebook profile
- With **Page Token** → your Facebook Page

### 🔹 `/me/accounts`
👉 **Lists all Facebook Pages you have access to**

**Returns:**
- Page IDs
- Page names
- Page Access Tokens *(important)*

## 📄 Page → Instagram Mapping

### 🔹 `/{page-id}?fields=instagram_business_account`
👉 **Gets the Instagram account linked to a Page**

**Returns:**
- Instagram Business Account ID

## 📸 Instagram Account

### 🔹 `/{ig-user-id}`
👉 **Basic info about the Instagram account**

**Used to:**
- Verify access
- Get username / metadata

### 🔹 `/{ig-user-id}?fields=...`
👉 **Fetch specific Instagram data**

**Examples of data:**
- `username`
- profile info

## 🖼️ Media (Posts)

### 🔹 `/{ig-user-id}/media`
👉 **Lists posts (media) of the Instagram account**

**Returns:**
- Media IDs *(important for comments)*

### 🔹 `/{media-id}`
👉 **Details of a specific post**

## 💬 Comments

### 🔹 `/{media-id}/comments`
👉 **Fetch comments on a post**

**Returns:**
- Comment IDs
- Text
- User info

### 🔹 `/{comment-id}`
👉 **Get details of a specific comment**

## 💬 Replies (YOUR MAIN ACTION)

### 🔹 `/{comment-id}/replies`
👉 **Reply to a comment**

- This is what your bot uses
- Requires comment ID *(NOT `me`)*

## 📩 Messaging (Optional / Future)

### 🔹 `/me/messages`
👉 **Send messages (Messenger / Instagram DM context)**

## 🔔 Webhooks (Event Source)

*Not a GET endpoint, but important:*
Meta sends `POST` requests to your webhook when events happen.

**Examples:**
- New comment
- New message
- Reply created

## 🧠 Relationship Map (IMPORTANT)

```text
/me → Page
Page → Instagram Account
Instagram → Media (posts)
Media → Comments
Comments → Replies
```

## 🚨 Common Mistakes (you already hit these 😄)

❌ **Using `/me` for actions**
- Works only for identity
- Not for comments/replies

❌ **Skipping Page layer**
- Instagram is always accessed via Page

❌ **Wrong ID type**

| Action | Required ID |
| ------ | ----------- |
| Get page | Page ID |
| Get IG | IG User ID |
| Get post | Media ID |
| Reply | Comment ID |

## 🎯 Minimal endpoints you ACTUALLY used

For your system:
- `/me/accounts`
- `/{page-id}?fields=instagram_business_account`
- `/{ig-user-id}`
- `/{comment-id}/replies`

## ⚡ One-line mental model

**Every action in Meta = “object ID + edge”**

**Example:**
- `comment-id` + `/replies` → reply action
- `media-id` + `/comments` → get comments