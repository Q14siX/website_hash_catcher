[![Version](https://img.shields.io/github/v/release/Q14siX/website_hash_catcher)](https://github.com/Q14siX/website_hash_catcher/releases)
![Downloads](https://img.shields.io/github/downloads/Q14siX/website_hash_catcher/total)
![Contributors](https://img.shields.io/github/contributors/Q14siX/website_hash_catcher)

# Website Hash Catcher 🔍

![Website Hash Catcher](https://raw.githubusercontent.com/Q14siX/website_hash_catcher/main/logo.png)

**Website Hash Catcher** ist eine Home Assistant Integration, die regelmäßig den Hash-Wert einer angegebenen Webseite berechnet und überwacht. Dies kann nützlich sein, um **Webseitenänderungen** zu erkennen oder sicherzustellen, dass eine Webseite **unverändert** bleibt.

## 🌟 Funktionen
- Überwacht eine Webseite und berechnet deren **Hash-Wert**.
- Unterstützt verschiedene **Hash-Algorithmen**:
  - SHA-512
  - SHA-256
  - SHA-1
  - MD5
- **Automatische Aktualisierung** in einem einstellbaren Intervall.
- Integration über **HACS** für einfache Installation.

## 📥 Installation

### 1️⃣ **Hinzufügen zu HACS**
1. **Gehe zu Home Assistant** > **HACS** > **Integrationen**.
2. Öffne die **Benutzerdefinierten Repositories** und füge hinzu:
   ```
   https://github.com/Q14siX/website_hash_catcher
   ```
3. Wähle **Integration** als Kategorie und speichere.

### 2️⃣ **Installation der Integration**
1. Nach dem Hinzufügen des Repositories in HACS, installiere die **Website Hash Catcher** Integration.
2. **Neustart von Home Assistant** erforderlich.

## ⚙️ Konfiguration
1. **Gehe zu `Einstellungen → Geräte & Dienste → Integration hinzufügen`.**
2. Suche nach **Website Hash Catcher** und wähle sie aus.
3. Gib die **URL der Webseite** ein, die überwacht werden soll.
4. Wähle den gewünschten **Hash-Algorithmus**.
5. Stelle das **Update-Intervall** ein.

## 📊 Nutzung
Nach der Installation findest du die Sensor-Entität unter `sensor.website_hash_catcher`.  
Nutze diesen Sensor in **Automationen** oder **Lovelace Dashboards**, um Änderungen zu überwachen.

### **Beispiel für eine Automation:**
```yaml
alias: "Benachrichtigung bei Website-Änderung"
trigger:
  - platform: state
    entity_id: sensor.website_hash_catcher
action:
  - service: notify.notify
    data:
      title: "Website geändert!"
      message: "Der Hash-Wert der Webseite hat sich geändert!"
```

## 🖼️ Logo & Icon
Das folgende Bild wird als Icon und Image für die Integration verwendet:

![Website Hash Catcher](https://raw.githubusercontent.com/Q14siX/website_hash_catcher/main/logo.png)

## 👨‍💻 Entwickler
- **GitHub:** [Q14siX](https://github.com/Q14siX)
- **Lizenz:** MIT

---
🔧 **Website Hash Catcher** ist eine einfache Möglichkeit, Webseiten auf **ungewollte Änderungen** zu überwachen!
