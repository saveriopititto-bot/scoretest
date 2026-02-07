# 📖 Guida alla Migrazione: Streamlit → Flet

Questa guida spiega in dettaglio come il codice Streamlit è stato convertito in Flet e fornisce pattern riutilizzabili per future migrazioni.

## 🔄 Pattern di Conversione Comuni

### 1. Session State → AppState

**Streamlit:**
```python
if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1
```

**Flet:**
```python
class AppState:
    def __init__(self, page):
        self.page = page
        self._counter = 0
    
    @property
    def counter(self):
        return self._counter
    
    @counter.setter
    def counter(self, value):
        self._counter = value
        # Opzionale: auto-update
        # self.page.update()
```

### 2. Layout e Containers

**Streamlit:**
```python
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.metric("Score", "752")

with col2:
    st.line_chart(data)

with col3:
    st.button("Sync")
```

**Flet:**
```python
ft.Row(
    controls=[
        # col1
        ft.Container(
            content=ft.Text("Score: 752"),
            expand=1,
        ),
        # col2
        ft.Container(
            content=ft.LineChart(...),
            expand=2,
        ),
        # col3
        ft.Container(
            content=ft.ElevatedButton("Sync"),
            expand=1,
        ),
    ],
)
```

### 3. Text e Markdown

**Streamlit:**
```python
st.title("Dashboard")
st.markdown("### Sottotitolo")
st.text("Testo normale")
st.write("Testo generico")
```

**Flet:**
```python
ft.Column(
    controls=[
        ft.Text(
            "Dashboard",
            size=32,
            weight=ft.FontWeight.BOLD,
        ),
        ft.Text(
            "Sottotitolo",
            size=20,
            weight=ft.FontWeight.W_500,
        ),
        ft.Text("Testo normale", size=14),
        ft.Text("Testo generico"),
    ]
)
```

### 4. Buttons e Callbacks

**Streamlit:**
```python
if st.button("Click Me"):
    st.write("Clicked!")
    st.session_state.clicked = True
```

**Flet:**
```python
def on_button_click(e):
    # Update UI
    text.value = "Clicked!"
    state.clicked = True
    page.update()

text = ft.Text("")
button = ft.ElevatedButton(
    "Click Me",
    on_click=on_button_click,
)
```

### 5. Forms e Input

**Streamlit:**
```python
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(f"Hello {name}, age {age}")
```

**Flet:**
```python
def on_submit(e):
    result.value = f"Hello {name_field.value}, age {age_field.value}"
    page.update()

name_field = ft.TextField(label="Name")
age_field = ft.TextField(label="Age", keyboard_type=ft.KeyboardType.NUMBER)
submit_btn = ft.ElevatedButton("Submit", on_click=on_submit)
result = ft.Text("")

form = ft.Column(
    controls=[name_field, age_field, submit_btn, result]
)
```

### 6. Selectbox e Dropdown

**Streamlit:**
```python
option = st.selectbox(
    "Choose option",
    ["Option 1", "Option 2", "Option 3"]
)
```

**Flet:**
```python
def on_change(e):
    print(f"Selected: {dropdown.value}")

dropdown = ft.Dropdown(
    label="Choose option",
    options=[
        ft.dropdown.Option("Option 1"),
        ft.dropdown.Option("Option 2"),
        ft.dropdown.Option("Option 3"),
    ],
    on_change=on_change,
)
```

### 7. Tabs

**Streamlit:**
```python
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.write("Content 1")

with tab2:
    st.write("Content 2")
```

**Flet:**
```python
tabs = ft.Tabs(
    selected_index=0,
    tabs=[
        ft.Tab(
            text="Tab 1",
            content=ft.Container(
                content=ft.Text("Content 1"),
                padding=10,
            ),
        ),
        ft.Tab(
            text="Tab 2",
            content=ft.Container(
                content=ft.Text("Content 2"),
                padding=10,
            ),
        ),
    ],
)
```

### 8. Spinner e Progress

**Streamlit:**
```python
with st.spinner("Loading..."):
    time.sleep(3)
    st.success("Done!")
```

**Flet:**
```python
def long_operation(e):
    # Mostra spinner
    progress = ft.ProgressRing()
    page.add(progress)
    page.update()
    
    # Operazione
    time.sleep(3)
    
    # Rimuovi spinner
    page.remove(progress)
    page.add(ft.Text("Done!", color=ft.colors.GREEN))
    page.update()
```

### 9. Popover/Expander

**Streamlit:**
```python
with st.expander("See details"):
    st.write("Hidden content")
```

**Flet:**
```python
# Opzione 1: ExpansionPanel
ft.ExpansionPanelList(
    controls=[
        ft.ExpansionPanel(
            header=ft.Text("See details"),
            content=ft.Container(
                content=ft.Text("Hidden content"),
                padding=10,
            ),
        ),
    ],
)

# Opzione 2: Dialog/AlertDialog
dialog = ft.AlertDialog(
    title=ft.Text("Details"),
    content=ft.Text("Hidden content"),
)
```

### 10. Sidebar

**Streamlit:**
```python
with st.sidebar:
    st.selectbox("Filter", ["All", "Recent"])
    st.slider("Days", 1, 90, 30)
```

**Flet:**
```python
# NavigationRail (sidebar verticale)
rail = ft.NavigationRail(
    selected_index=0,
    destinations=[
        ft.NavigationRailDestination(
            icon=ft.icons.DASHBOARD,
            label="Dashboard",
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.SETTINGS,
            label="Settings",
        ),
    ],
)

# Layout
ft.Row(
    controls=[
        rail,
        ft.VerticalDivider(width=1),
        ft.Container(expand=True),  # Main content
    ],
)
```

## 🎨 Styling Equivalences

### Colors

**Streamlit (CSS):**
```python
st.markdown("""
<style>
.custom-class {
    color: #00ff41;
    background: #1a1a1a;
}
</style>
""", unsafe_allow_html=True)
```

**Flet:**
```python
ft.Container(
    content=ft.Text("Text", color="#00ff41"),
    bgcolor="#1a1a1a",
)
```

### Borders

**Streamlit:**
```python
st.markdown("""
<div style="border: 2px solid #00ff41; border-radius: 10px; padding: 20px;">
    Content
</div>
""", unsafe_allow_html=True)
```

**Flet:**
```python
ft.Container(
    content=ft.Text("Content"),
    border=ft.border.all(2, "#00ff41"),
    border_radius=10,
    padding=20,
)
```

### Gradients

**Streamlit:**
```python
st.markdown("""
<div style="background: linear-gradient(to bottom right, #0a0a0a, #1a1a1a);">
    Content
</div>
""", unsafe_allow_html=True)
```

**Flet:**
```python
ft.Container(
    content=ft.Text("Content"),
    gradient=ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=["#0a0a0a", "#1a1a1a"],
    ),
)
```

## 🔧 Advanced Patterns

### Navigation tra Views

**Streamlit:**
```python
# Use query params or session state
if st.button("Go to Dashboard"):
    st.session_state.page = "dashboard"
    st.rerun()

# In app.py
if st.session_state.page == "dashboard":
    render_dashboard()
elif st.session_state.page == "settings":
    render_settings()
```

**Flet:**
```python
def navigate_to(view_name):
    page.controls.clear()
    
    if view_name == "dashboard":
        view = DashboardView(...)
    elif view_name == "settings":
        view = SettingsView(...)
    
    page.add(view.build())
    page.update()

# In button
ft.ElevatedButton(
    "Go to Dashboard",
    on_click=lambda e: navigate_to("dashboard"),
)
```

### Data Fetching Async

**Streamlit:**
```python
@st.cache_data
def fetch_data():
    return expensive_operation()

data = fetch_data()
st.write(data)
```

**Flet:**
```python
import asyncio

async def fetch_data_async():
    # Show loading
    loading = ft.ProgressRing()
    page.add(loading)
    page.update()
    
    # Fetch
    data = await expensive_operation_async()
    
    # Hide loading, show data
    page.remove(loading)
    page.add(ft.Text(str(data)))
    page.update()

# Trigger
ft.ElevatedButton(
    "Load Data",
    on_click=lambda e: asyncio.create_task(fetch_data_async()),
)
```

### Custom Components

**Streamlit:**
```python
import streamlit.components.v1 as components

html_string = """
<div id="custom-widget">
    <script>
        // Custom JS
    </script>
</div>
"""
components.html(html_string, height=300)
```

**Flet:**
```python
# Opzione 1: Web View (per HTML)
from flet import WebView

web = WebView(
    url="https://example.com",
    expand=True,
)

# Opzione 2: Custom Control
class MyCustomControl(ft.UserControl):
    def build(self):
        return ft.Container(
            content=ft.Text("Custom"),
            # ... custom logic
        )
```

## 🐛 Common Pitfalls

### 1. Forgot to call page.update()

```python
# ❌ WRONG - changes won't appear
text.value = "New value"

# ✅ CORRECT
text.value = "New value"
page.update()
```

### 2. Circular references

```python
# ❌ WRONG
def on_click(e):
    button.text = "Clicked"  # Reference before creation

button = ft.ElevatedButton("Click", on_click=on_click)

# ✅ CORRECT
button = ft.ElevatedButton("Click")

def on_click(e):
    button.text = "Clicked"
    page.update()

button.on_click = on_click
```

### 3. Not handling expand properly

```python
# ❌ WRONG - container won't fill space
ft.Container(content=ft.Text("Text"))

# ✅ CORRECT
ft.Container(
    content=ft.Text("Text"),
    expand=True,  # Takes available space
)
```

## 📚 Resources for Deep Dive

1. **Flet Controls Gallery**: https://flet.dev/docs/controls
2. **Layout Guide**: https://flet.dev/docs/controls/layout
3. **Responsive Design**: https://flet.dev/docs/guides/python/responsive-design
4. **Async Programming**: https://flet.dev/docs/guides/python/async-apps

## 💡 Best Practices

1. **Organize by Views**: Separa ogni "pagina" in una classe View
2. **Use State Management**: Centralizza lo stato in AppState
3. **Componentize**: Crea componenti riutilizzabili (Card, Button, ecc.)
4. **Lazy Loading**: Carica dati solo quando necessario
5. **Error Handling**: Gestisci eccezioni e mostra messaggi user-friendly
6. **Logging**: Usa logging per debug invece di print()
7. **Type Hints**: Usa typing per codice più maintainable

```python
from typing import Optional, List, Dict

class MyView:
    def __init__(self, page: ft.Page, data: Optional[List[Dict]] = None):
        self.page = page
        self.data = data or []
```

## 🎯 Next Steps

Dopo la migrazione base:

1. **Implementa grafici reali** (Matplotlib/Plotly)
2. **Aggiungi testing** (pytest + flet.testing)
3. **Ottimizza performance** (lazy loading, virtualization)
4. **Mobile adaptation** (responsive breakpoints)
5. **Offline support** (local storage)
6. **CI/CD** (GitHub Actions per build cross-platform)

---

**Domande?** Consulta la [documentazione ufficiale Flet](https://flet.dev/docs) o apri una issue su GitHub.
