# ⚡ Quick Reference - sCore Flet

Comandi e snippet più usati per lavorare con il progetto.

## 🚀 Start Commands

```bash
# Sviluppo locale
python main.py

# Con hot reload (flet in watch mode)
flet run main.py --web

# Specifica porta
flet run main.py --port 8080
```

## 🔧 Build Commands

```bash
# Desktop Windows
flet pack main.py --name sCore --icon assets/favicon.png

# Desktop macOS
flet pack main.py --name sCore --icon assets/favicon.png

# Desktop Linux
flet pack main.py --name sCore

# Web
flet build web

# Android APK
flet build apk

# iOS
flet build ipa
```

## 📦 Dependencies

```bash
# Installa tutte
pip install -r requirements.txt

# Aggiorna Flet
pip install --upgrade flet

# Aggiungi nuova libreria
pip install package_name
pip freeze > requirements.txt
```

## 🎨 Common UI Patterns

### Bottone con azione

```python
def on_click(e):
    print("Clicked!")
    page.update()

btn = ft.ElevatedButton("Click Me", on_click=on_click)
```

### Input con validazione

```python
def on_change(e):
    if len(email.value) > 0 and "@" in email.value:
        email.error_text = None
    else:
        email.error_text = "Email non valida"
    page.update()

email = ft.TextField(
    label="Email",
    on_change=on_change,
)
```

### Dialog modale

```python
def close_dialog(e):
    dialog.open = False
    page.update()

dialog = ft.AlertDialog(
    title=ft.Text("Conferma"),
    content=ft.Text("Sei sicuro?"),
    actions=[
        ft.TextButton("Annulla", on_click=close_dialog),
        ft.TextButton("OK", on_click=close_dialog),
    ],
)

page.dialog = dialog
dialog.open = True
page.update()
```

### Loading spinner

```python
# Mostra
progress = ft.ProgressRing()
page.add(progress)
page.update()

# Operazione lunga
import time
time.sleep(2)

# Nascondi
page.remove(progress)
page.update()
```

### Snackbar notifica

```python
page.snack_bar = ft.SnackBar(
    content=ft.Text("Operazione completata!"),
    bgcolor=ft.colors.GREEN,
)
page.snack_bar.open = True
page.update()
```

## 🎯 State Management

```python
# Get state
value = state.counter

# Set state
state.counter = 10

# Update UI
page.update()
```

## 🔄 Navigation

```python
# Naviga a view
navigate_to("dashboard")

# Con parametri
def navigate_to(view_name, **params):
    state.current_params = params
    # ... build view
```

## 📊 Data Handling

### Load from DB

```python
# Sync
data = db_svc.get_history(athlete_id)

# Async
async def load_data():
    data = await db_svc.get_history_async(athlete_id)
    # Update UI
    page.update()
```

### Update UI with data

```python
df = pd.DataFrame(data)
table = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Data")),
        ft.DataColumn(ft.Text("Score")),
    ],
    rows=[
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(row['Data']))),
                ft.DataCell(ft.Text(str(row['SCORE']))),
            ]
        ) for _, row in df.iterrows()
    ],
)
```

## 🐛 Debugging

### Enable debug logs

```python
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("sCore")
logger.debug("Debug message")
```

### Print state

```python
print(f"State: {vars(state)}")
```

### Inspect page

```python
print(f"Controls: {len(page.controls)}")
print(f"Route: {page.route}")
```

## 🎨 Styling Quick Ref

### Colors

```python
# Named colors
ft.colors.RED
ft.colors.BLUE_500

# Hex colors
"#00ff41"
"#FF6B6B"

# With opacity
ft.colors.with_opacity(0.5, ft.colors.RED)
```

### Fonts

```python
ft.FontWeight.BOLD
ft.FontWeight.W_500
ft.FontWeight.NORMAL
```

### Alignment

```python
# Container alignment
alignment=ft.alignment.center
alignment=ft.alignment.top_left

# Row/Column alignment
alignment=ft.MainAxisAlignment.CENTER
alignment=ft.MainAxisAlignment.SPACE_BETWEEN
```

### Padding/Margin

```python
# Uniform
padding=20

# Symmetric
padding=ft.padding.symmetric(horizontal=20, vertical=10)

# All sides
padding=ft.padding.all(20)

# Specific sides
padding=ft.padding.only(left=20, top=10)
```

## 📱 Responsive Design

```python
def build_responsive():
    if page.width > 1200:
        return desktop_layout()
    elif page.width > 600:
        return tablet_layout()
    else:
        return mobile_layout()

page.on_resize = lambda e: page.update()
```

## 🔐 Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

STRAVA_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
```

## 📝 Common Issues & Fixes

### UI non si aggiorna

```python
# ❌ WRONG
text.value = "New"

# ✅ CORRECT
text.value = "New"
page.update()
```

### Controllo non visibile

```python
# Check visibility
control.visible = True
page.update()

# Check expand
container.expand = True
page.update()
```

### Error: Control already has parent

```python
# ❌ WRONG - riusa stesso control
page.add(text)
page.add(text)  # Error!

# ✅ CORRECT - crea nuovo
page.add(ft.Text("Text 1"))
page.add(ft.Text("Text 2"))
```

### Memory leak con callbacks

```python
# ❌ WRONG - circular reference
def create_button():
    btn = ft.ElevatedButton("Click")
    btn.on_click = lambda e: btn.text = "Clicked"
    return btn

# ✅ CORRECT
def create_button():
    def on_click(e):
        e.control.text = "Clicked"
        page.update()
    
    return ft.ElevatedButton("Click", on_click=on_click)
```

## 🧪 Testing

```python
# Unit test
import pytest

def test_state():
    state = AppState(None)
    state.counter = 5
    assert state.counter == 5

# UI test (flet.testing)
from flet.testing import AppTest

def test_app():
    app = AppTest(main)
    app.start()
    
    # Simula click
    button = app.get_control("my_button")
    button.click()
    
    assert app.get_control("result").value == "Clicked"
```

## 📚 Useful Links

- [Flet Docs](https://flet.dev/docs)
- [Flet Controls](https://flet.dev/docs/controls)
- [Flutter Colors](https://api.flutter.dev/flutter/material/Colors-class.html)
- [Material Icons](https://fonts.google.com/icons)

## 💡 Tips & Tricks

1. **Use ref for dynamic updates**
```python
counter = ft.Ref[ft.Text]()
page.add(ft.Text("0", ref=counter))
# Later:
counter.current.value = "5"
page.update()
```

2. **Batch updates**
```python
# Instead of multiple page.update()
with page:
    text1.value = "A"
    text2.value = "B"
    text3.value = "C"
# Auto-updates at end of with block
```

3. **Custom theme**
```python
page.theme = ft.Theme(
    color_scheme_seed=ft.colors.GREEN,
    use_material3=True,
)
```

4. **Keyboard shortcuts**
```python
page.on_keyboard_event = lambda e: (
    print(f"Key: {e.key}, Ctrl: {e.ctrl}")
)
```

5. **Lazy loading**
```python
# Load only visible items
visible_items = items[page.scroll_position:page.scroll_position+20]
```

---

**Pro tip**: Tieni questo file aperto mentre sviluppi per riferimento rapido!
