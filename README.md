# RestBox ⚡

> **Gruvbox Dark & Multi-Theme API Client & cURL Executor**  
> A lightweight, zero-dependency, browser-native API client and cURL command runner with a developer-first terminal aesthetic.

---

<p align="center">
  <img src="img/Screenshot%202026-09-21%20161203.png" alt="RestBox Gruvbox Dark - Executed Request & Response Viewer" width="100%">
</p>

---

## 📖 Overview

**RestBox** is a standalone, single-file API client designed for developers who love the retro, high-contrast aesthetic of **Gruvbox** and modern terminal color schemes. RestBox runs directly in your browser without requiring installation, Node.js runtimes, backend servers, or account sign-ups.

Whether you need to quickly test an endpoint, import a complex `curl` command from documentation, inspect responses, upload files via multipart form-data, or generate production-ready code snippets, RestBox provides a fluid, responsive, and keyboard-driven workflow.

---

## ✨ Key Features

### 🗂️ Multi-Tab Workspace
- **Concurrent Request Tabs**: Work on multiple API endpoints simultaneously.
- **Inline Tab Renaming**: Double-click any tab title to rename it with an in-place input.
- **Automatic Title Derivation**: Unnamed tabs automatically derive concise, readable names from the URL path.
- **Tab State Persistence**: Request method, headers, parameters, authentication, body, and response data are preserved when switching tabs.

<p align="center">
  <img src="img/Screenshot%202026-09-21%20161300.png" alt="RestBox - Initial Workspace & Request Builder" width="100%">
</p>

### 📜 First-Class cURL Integration
- **Smart cURL Importer**: Paste any `curl` command into the URL bar or modal. Supports:
  - Methods: `-X POST`, `-XPOST`, `--request PUT`, `-I`, `--head`.
  - Headers: `-H "Content-Type: application/json"`, `-H'Authorization: Bearer ...'`, `-A` (User-Agent), `-e` (Referer), `-b` (Cookie).
  - Data / Body: `-d`, `--data`, `--data-raw`, `--data-binary`, `--data-urlencode`, and multiple `-d` concatenation.
  - Multipart Form & Files: `-F "file=@/path/to/image.png"`, `-F "user=admin"`.
  - Basic Auth: `-u "username:password"`.
  - Protocol Fallback: Automatically handles `localhost:port` or URLs without explicit schemes.
- **Query Parameter Sync**: Automatically extracts query parameters from imported cURL URLs directly into the Params table.
- **Live cURL Generation**: Real-time cURL preview updated continuously as you modify headers, parameters, auth, or body.
- **One-Click Copy**: Copy the active request as a clean, multi-line cURL command ready for your terminal.

### 📤 Form-Data with File Upload
- **Dual Field Types**: Toggle each form-data row between **Text** and **File** mode.
- **File Picker & Preview Widget**:
  - Native file upload dialog with Gruvbox-styled trigger buttons.
  - Interactive file badges displaying `📄 filename.ext (size)` with instant remove (`✕`) and replace (`Ganti...`) buttons.
- **Multipart Upload Execution**: Files are sent as true binary `Blob` / `File` objects through the browser's `FormData` API.
- **Automatic Boundary Handling**: Manual `Content-Type` headers are safely omitted on multipart requests, allowing the browser to generate valid boundary strings (`multipart/form-data; boundary=----WebKitFormBoundary...`).

### ✍️ Smart Request Body Editor
- **Live Syntax Highlighting**: Real-time token highlighting for JSON:
  - Keys (`var(--aqua)`)
  - Strings (`var(--green)`)
  - Numbers (`var(--purple)`)
  - Booleans (`var(--orange)`)
  - Null (`var(--gray)`)
  - Brackets & Punctuation (`var(--fg4)`)
  - Embedded Environment Variables `{{variable}}` (`var(--yellow)`)
- **Auto-Closing Double Quotes (`"`)**:
  - Typing `"` inserts a matching pair `""` with the cursor placed in between.
  - Selecting text and typing `"` wraps the selected text in quotes.
  - Typing `"` before an existing quote steps over it without creating duplicate characters.
  - Backspace between empty quotes deletes both quotes.
- **Smart Brackets & Indentation**:
  - Auto-closes `{}` and `[]` with selection wrapping and step-over support.
  - Pressing `Enter` inside `{}` creates an indented block with 2-space indentation.
  - Pressing `Tab` inserts 2 spaces without losing editor focus.
- **Synchronized Line Numbers Gutter**: Left-side line numbers that scroll in lockstep with the text area.
- **JSON Beautifier**: One-click formatting with live validation feedback (`✓ Valid JSON` / `✗ Invalid JSON`).

### 🎨 Custom Color Themes & Customizer
- **7 Curated Built-in Presets**:
  1. **Gruvbox Dark** *(Default authentic warm retro dark)*
  2. **Gruvbox Light** *(Sun-bleached paper daylight theme)*
  3. **Tokyo Night** *(Cyberpunk neon indigo terminal)*
  4. **Catppuccin Mocha** *(Soothing pastel dark palette)*
  5. **Nord Arctic** *(Minimalist cool arctic blue palette)*
  6. **Dracula** *(Vampire high-contrast purple/pink palette)*
  7. **Monokai Pro** *(Vibrant warm high-contrast palette)*
- **Interactive Theme Builder**:
  - Live color pickers and hex inputs for Backgrounds, Surfaces, Inputs, Cards, Borders, Typography, and HTTP Method Badges.
  - 10 one-click Quick Accent chips (Orange, Amber, Green, Teal, Tokyo Blue, Nord Frost, Mauve, Pink, Rose, Red).
  - Live preview card reflecting UI changes in real time.
- **Export & Import**:
  - **Export JSON**: Save theme configurations to share with others or include in dotfiles.
  - **Import JSON**: Apply any RestBox theme JSON with one click.
- **Local Storage Persistence**: Active theme selection and custom colors persist across browser refreshes.

<p align="center">
  <img src="img/Screenshot%202026-09-21%20161427.png" alt="RestBox - Theme Customizer Modal & Presets" width="100%">
</p>

<p align="center">
  <img src="img/Screenshot%202026-09-21%20161449.png" alt="RestBox - Gruvbox Light Theme In Action" width="100%">
</p>

### 🔑 Authentication & Environment Variables
- **Authentication Modes**:
  - **No Auth**: Standard unauthenticated request.
  - **Bearer Token**: Automatically injects `Authorization: Bearer <token>`.
  - **Basic Auth**: Automatically base64-encodes username and password.
  - **API Key**: Inject custom key-value pairs into either the Request Headers or Query Parameters.
- **Dynamic Variables**:
  - Define key-value pairs in the **Variables** sidebar panel.
  - Use `{{variable_name}}` syntax in URLs, Headers, Body, or Auth fields.
  - Safely handles variable interpolation without percent-encoding corruption.

### 📊 Comprehensive Response Viewer
- **View Modes**:
  - **Pretty**: Formatted, syntax-colored JSON tree.
  - **Raw**: Verbatim raw response text.
  - **Preview**: Native image renderer for binary images (PNG, JPEG, GIF, WebP, SVG) and sandboxed iframe viewer for HTML.
- **Safe In-Response Search**: Search keywords highlighted with `<mark>` tags using a `TreeWalker` that preserves syntax-highlighting spans and protects against HTML injection.
- **Response Metadata**: Status badge (color-coded for 2xx, 3xx, 4xx, 5xx, ERR), roundtrip response latency (ms), and payload size.
- **Download Response**: Save response bodies with automatic file extension detection (`.json`, `.html`, `.png`, `.jpg`, etc.).

### 💻 Multi-Language Code Snippets
Export any configured request to production-ready code:
- **cURL**: Multi-line terminal command.
- **JavaScript**: Modern `fetch()` with `async/await` and proper `JSON.stringify` handling.
- **Python**: Python 3 `requests` library with typed dictionaries, boolean conversions, and file uploads.
- **PHP**: Native `curl_init` and `curl_setopt_array` with `CURLOPT_POSTFIELDS`.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + Enter` / `Cmd + Enter` | Send current request |
| `Enter` *(inside URL bar)* | Send current request |
| `Alt + N` | Open new request tab |
| `Alt + W` | Close active request tab |
| `Ctrl + B` / `Cmd + B` | Toggle sidebar (History / Presets / Variables) |
| `Double-Click Tab` | Rename active tab |
| `Tab` *(inside Body editor)* | Insert 2 spaces |
| `"` / `{` / `[` *(inside Body editor)* | Auto-close pair or wrap selected text |

---

## 🚀 Getting Started

RestBox requires no installation, dependencies, or build step.

### Quick Start (Direct File)
1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-username/restbox.git
   cd restbox
   ```
2. Double-click or open `restbox/index.html` in any modern browser (Chrome, Firefox, Edge, Safari, Brave, Arc).

### Local Server (Optional)
If you prefer running RestBox from a local web server:

**Using Node.js:**
```bash
npx serve restbox
```

**Using Python:**
```bash
python -m http.server 8000 -d restbox
```

**Using Bun:**
```bash
bun x serve restbox
```

Then visit `http://localhost:8000` (or the port specified).

---

## 🌐 Handling CORS (Cross-Origin Resource Sharing)

Browser security prevents web pages from making HTTP requests to different domains unless the destination server includes permissive CORS headers (`Access-Control-Allow-Origin`).

If an API returns a CORS error:
1. **Enable CORS Proxy**: Check the **Enable CORS Proxy** toggle beneath the URL bar. Requests will be routed through a public CORS proxy.
2. **Backend Development**: For local development (`localhost:3000`, etc.), ensure your backend server enables CORS middleware:
   - **Express.js**: `app.use(require('cors')());`
   - **FastAPI / Python**: `app.add_middleware(CORSMiddleware, allow_origins=["*"])`
   - **Laravel / Django / Spring**: Enable standard CORS middleware.

---

## 📁 Project Structure

```
restbox/
├── img/                # Application screenshots & assets
├── restbox/
│   └── index.html      # Complete standalone web application (HTML, CSS, JS)
└── README.md           # Project documentation
```

---

## 🛠️ Built With

- **HTML5 & CSS3**: Pure CSS custom properties (variables), CSS Grid, and Flexbox.
- **Vanilla JavaScript (ES6+)**: Zero external libraries or heavy frameworks.
- **Gruvbox Palette**: Original retro color scheme by Pavel Pertsev (morhetz).

---

## 📄 License

Distributed under the **MIT License**. Free for personal and commercial use.
