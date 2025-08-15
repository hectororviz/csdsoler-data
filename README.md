# sheets-to-json

Convierte hojas de **Google Sheets** en **JSON estático** y lo publica en **GitHub Pages** para que tu app Flutter lo descargue rápido (CDN + ETag).

## Config rápida

1. Crea un repo y subí estos archivos.
2. En **Settings → Pages**, elegí **GitHub Actions** como Source.
3. En **Settings → Actions → Variables**, crea `SHEET_ID` con: `1Sia7krk2Mts6w-H1zvG88jWIQhpm5zUHf_COXI2Ab9s`.
4. Los GIDs ya están configurados en `scripts/fetch_and_build.py` para: general, sub-9, sub-11, sub-14, sub-17, primera, damas, sabado, domingo, femenino, home.
5. Ejecuta el workflow en **Actions** o espera al cron (cada 10 min).

### URLs resultantes (ejemplo)
- `https://<usuario>.github.io/<repo>/data.json`
- `https://<usuario>.github.io/<repo>/home.json`
- `https://<usuario>.github.io/<repo>/sabado.json`
- etc.

## Notas
- Si querés agregar/quitar hojas, edita el dict `SHEETS` en `scripts/fetch_and_build.py`.
- Si no querés hardcodear el `SHEET_ID`, déjalo solo en la variable de Actions.
- El script intenta castear números automáticamente; ajustá `normalize_rows` si necesitás tipos estrictos.
