# 🚀 Guida Deployment - sCore Flet

Guida completa per deployare l'applicazione su diverse piattaforme.

## 📋 Pre-requisiti

- Python 3.8+
- Flet CLI installato: `pip install flet`
- Account sviluppatore (per mobile)

## 💻 Desktop Application

### Windows

```bash
# Build executable Windows
flet pack main.py \
  --name "sCore" \
  --icon assets/favicon.png \
  --product-name "sCore 4.0" \
  --product-version "1.0.0" \
  --file-description "Running Performance Analytics" \
  --copyright "© 2024 sCore"

# Output: dist/sCore.exe
```

**Distribuzione:**
- Crea installer con [Inno Setup](https://jrsoftware.org/isinfo.php)
- O distribuisci direttamente l'exe (~ 50MB)

### macOS

```bash
# Build per macOS
flet pack main.py \
  --name "sCore" \
  --icon assets/favicon.png

# Output: dist/sCore.app
```

**Code Signing (opzionale ma raccomandato):**

```bash
# Firma l'app
codesign --deep --force --sign "Developer ID Application: Your Name" dist/sCore.app

# Notarizza per Gatekeeper
xcrun notarytool submit dist/sCore.app.zip \
  --apple-id your@email.com \
  --password app-specific-password \
  --team-id YOUR_TEAM_ID
```

### Linux

```bash
# Build per Linux
flet pack main.py --name "sCore"

# Output: dist/sCore (binary)
```

**Crea .deb package:**

```bash
# Usa fpm
gem install fpm

fpm -s dir -t deb -n score \
  -v 1.0.0 \
  --prefix /opt/score \
  dist/sCore=/opt/score/sCore
```

## 🌐 Web Application

### Build Static Web App

```bash
# Build web app
flet build web

# Output: build/web/
```

**Struttura output:**
```
build/web/
├── index.html
├── main.dart.js
├── flutter_service_worker.js
├── manifest.json
└── assets/
```

### Deploy su Netlify

```bash
# Installa Netlify CLI
npm install -g netlify-cli

# Deploy
cd build/web
netlify deploy --prod

# Segui le istruzioni interattive
```

**Netlify config** (netlify.toml):

```toml
[build]
  publish = "build/web"
  command = "flet build web"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Deploy su Vercel

```bash
# Installa Vercel CLI
npm install -g vercel

# Deploy
cd build/web
vercel --prod
```

**vercel.json:**

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Deploy su GitHub Pages

```bash
# Build
flet build web

# Deploy
cd build/web
git init
git add .
git commit -m "Deploy sCore"
git branch -M gh-pages
git remote add origin https://github.com/username/score.git
git push -f origin gh-pages
```

**GitHub Actions** (.github/workflows/deploy.yml):

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install flet
        pip install -r requirements.txt
    
    - name: Build web
      run: flet build web
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./build/web
```

## 📱 Mobile Applications

### Android (APK)

**Requisiti:**
- Android SDK
- Java JDK 11+

```bash
# Build APK
flet build apk

# Output: build/app/outputs/flutter-apk/app-release.apk
```

**Firma APK per Google Play:**

```bash
# Genera keystore (una volta)
keytool -genkey -v -keystore score-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias score

# Build signed APK
flet build apk --release \
  --build-name 1.0.0 \
  --build-number 1
```

**Upload su Google Play:**

1. Vai su [Google Play Console](https://play.google.com/console)
2. Crea nuova app
3. Upload APK in "Testing" → "Internal testing"
4. Completa listing (screenshot, descrizione)
5. Submit per review

### Android (AAB - consigliato per Play Store)

```bash
# Build App Bundle
flet build aab

# Output: build/app/outputs/bundle/release/app-release.aab
```

### iOS (IPA)

**Requisiti:**
- macOS
- Xcode
- Apple Developer Account ($99/anno)

```bash
# Build IPA
flet build ipa

# Output: build/ios/ipa/sCore.ipa
```

**Code Signing:**

1. Apri Xcode
2. Carica certificati da Apple Developer
3. Configura provisioning profiles
4. Build → Archive → Distribute

**Upload su App Store:**

1. Usa Xcode o Application Loader
2. Completa metadata in App Store Connect
3. Submit per review

## 🔐 Environment Variables

### Desktop

Crea file `.env` nella stessa directory dell'eseguibile:

```bash
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

### Web

**Netlify:**

```bash
netlify env:set STRAVA_CLIENT_ID your_id
netlify env:set STRAVA_CLIENT_SECRET your_secret
```

**Vercel:**

```bash
vercel env add STRAVA_CLIENT_ID
vercel env add STRAVA_CLIENT_SECRET
```

### Mobile

Usa file `env.yaml` e build-time injection:

```yaml
# env.yaml
strava:
  client_id: YOUR_ID
  client_secret: YOUR_SECRET
```

Build con:

```bash
flet build apk --dart-define-from-file=env.yaml
```

## 📊 Analytics e Monitoring

### Google Analytics (Web)

Aggiungi in `build/web/index.html`:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Sentry (Error Tracking)

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0,
    environment="production",
)
```

## 🔄 CI/CD Pipeline

### GitHub Actions - Multi-platform

```yaml
name: Build Multi-Platform

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Build Windows
        run: |
          pip install flet
          flet pack main.py --name sCore
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: sCore-Windows
          path: dist/sCore.exe

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Build macOS
        run: |
          pip install flet
          flet pack main.py --name sCore
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: sCore-macOS
          path: dist/sCore.app

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Build Linux
        run: |
          pip install flet
          flet pack main.py --name sCore
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: sCore-Linux
          path: dist/sCore

  release:
    needs: [build-windows, build-macos, build-linux]
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            sCore-Windows/sCore.exe
            sCore-macOS/sCore.app
            sCore-Linux/sCore
```

## 📦 Update Mechanism

### Desktop Auto-Update

Usa [PyUpdater](https://github.com/Digital-Sapien/PyUpdater):

```python
from pyupdater.client import Client

client = Client(ClientConfig())
app_update = client.update_check('sCore', '1.0.0')

if app_update:
    app_update.download()
    app_update.extract_restart()
```

### Web Auto-Update

Service Worker + Cache:

```javascript
// service-worker.js
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

## 🧪 Testing Production Build

```bash
# Test web build localmente
cd build/web
python -m http.server 8000

# Test desktop build
./dist/sCore  # Linux/macOS
dist\sCore.exe  # Windows
```

## 📝 Checklist Pre-Release

- [ ] Versione aggiornata in config.py
- [ ] Changelog documentato
- [ ] Test su tutte le piattaforme target
- [ ] Secrets configurati correttamente
- [ ] Analytics setup
- [ ] Error tracking attivo
- [ ] Backup database
- [ ] Documentazione aggiornata
- [ ] Screenshot per store
- [ ] Privacy policy aggiornata
- [ ] Terms of service aggiornati

## 🔒 Security Best Practices

1. **Non hardcodare secrets** nel codice
2. **Usa HTTPS** per tutte le API calls
3. **Valida input** utente lato client e server
4. **Rate limiting** per API endpoints
5. **Encrypt sensitive data** a riposo
6. **Regular security audits**

## 📈 Performance Optimization

### Web

```bash
# Minify assets
flet build web --web-renderer canvaskit --release

# Enable gzip compression (Nginx)
gzip on;
gzip_types text/css application/javascript;
```

### Desktop

```bash
# Reduce bundle size
flet pack --exclude-packages matplotlib,scipy
```

## 🎯 Post-Deployment

1. **Monitor logs** per errori
2. **Track metrics** (DAU, MAU, engagement)
3. **Collect feedback** utenti
4. **Pianifica updates** regolari
5. **Backup** regolare del database

---

**Domande?** Apri una issue su GitHub o contatta il supporto.
