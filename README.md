# Virtual Window Sensor für Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/tgast/home-assistant-virtual-window-sensor.svg)](https://github.com/tgast/home-assistant-virtual-window-sensor/releases)
[![License](https://img.shields.io/github/license/tgast/home-assistant-virtual-window-sensor.svg)](LICENSE)

Eine Home Assistant Custom Integration, die virtuelle Fenstersensoren basierend auf Temperaturänderungen erstellt. Ideal für die automatische Heizungssteuerung in Räumen ohne physische Fenstersensoren.

## 🎯 Warum diese Integration?

Physische Fenstersensoren sind teuer und nicht in jedem Raum praktikabel. Diese Integration nutzt vorhandene Temperatursensoren, um automatisch zu erkennen, wann ein Fenster geöffnet wird - durch den charakteristischen schnellen Temperaturabfall beim Lüften.

**Anwendungsfälle:**
- 🔥 Automatisches Abschalten der Heizung beim Lüften
- 💰 Energiesparen durch intelligente Heizungssteuerung
- 📱 Benachrichtigungen bei vergessenen offenen Fenstern
- 🏠 Smart Home Automationen basierend auf Fensterstatus

## ✨ Features

- ✅ **Automatische Fenstererkennung** durch Temperaturüberwachung
- ✅ **Einfache UI-Konfiguration** - kein YAML erforderlich
- ✅ **Unbegrenzt viele Sensoren** - für jeden Raum einen eigenen Sensor
- ✅ **Konfigurierbare Parameter** - Schwellenwerte individuell anpassbar
- ✅ **Mehrsprachig** - Deutsch und Englisch verfügbar
- ✅ **HACS-kompatibel** - Einfache Installation und Updates
- ✅ **Detaillierte Attribute** - Für Debugging und Monitoring

## 🔧 Wie funktioniert es?

Die Integration überwacht kontinuierlich einen Temperatursensor und erkennt charakteristische Temperaturmuster beim Öffnen eines Fensters:

1. **Temperaturverlauf speichern**: Die letzten Temperaturwerte werden mit Zeitstempeln gespeichert
2. **Vergleich**: Bei jeder Änderung wird die aktuelle Temperatur mit der Temperatur vor X Sekunden verglichen
3. **Erkennung**: Wenn die Temperatur um mehr als den Schwellenwert gefallen ist, wird das Fenster als "offen" erkannt
4. **Rücksetzen**: Sobald die Temperatur stabil ist, wird der Sensor automatisch auf "geschlossen" gesetzt

### Beispiel

```
Zeit:        0s     10s     20s     30s
Temperatur: 21.5°C → 21.4°C → 21.0°C → 20.8°C

Temperaturabfall nach 30s: 21.5°C - 20.8°C = 0.7°C
Schwellenwert: 0.3°C
→ Fenster wird als OFFEN erkannt ✓
```

## 📦 Installation

### Über HACS (empfohlen)

1. Öffne **HACS** in Home Assistant
2. Klicke auf **Integrationen**
3. Klicke auf die **drei Punkte** (⋮) oben rechts
4. Wähle **Benutzerdefinierte Repositories**
5. Füge hinzu:
   - **Repository**: `https://github.com/tgast/home-assistant-virtual-window-sensor`
   - **Kategorie**: `Integration`
6. Klicke auf **Hinzufügen**
7. Suche nach "Virtual Window Sensor" und klicke auf **Download**
8. **Starte Home Assistant neu**

### Manuelle Installation

1. Lade die [neueste Version](https://github.com/tgast/home-assistant-virtual-window-sensor/releases) herunter
2. Entpacke das Archiv
3. Kopiere den Ordner `custom_components/virtual_window_sensor` in dein Home Assistant `config/custom_components/` Verzeichnis
4. Starte Home Assistant neu

## ⚙️ Konfiguration

### Erstmalige Einrichtung

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Klicke auf **+ Integration hinzufügen**
3. Suche nach **Virtual Window Sensor**
4. Folge dem Konfigurationsassistenten:

#### Parameter

| Parameter | Standard | Bereich | Beschreibung |
|-----------|----------|---------|--------------|
| **Name** | - | - | Name für den virtuellen Sensor (z.B. "Fenster Wohnzimmer") |
| **Temperatursensor** | - | - | Der zu überwachende Temperatursensor |
| **Temperaturschwelle** | 0.3°C | 0.1 - 5.0°C | Minimaler Temperaturabfall für "Fenster offen" |
| **Zeitfenster** | 30s | 10 - 300s | Zeitraum über den gemessen wird |

### Empfohlene Einstellungen nach Raumtyp

**Wohnzimmer / Große Räume:**
- Temperaturschwelle: `0.4°C`
- Zeitfenster: `25s`

**Badezimmer / Kleine Räume:**
- Temperaturschwelle: `0.5°C`
- Zeitfenster: `40s`

**Schlafzimmer:**
- Temperaturschwelle: `0.3°C`
- Zeitfenster: `35s`

**Küche (hohe Temperaturschwankungen):**
- Temperaturschwelle: `0.6°C`
- Zeitfenster: `20s`

### Mehrere Räume einrichten

Wiederhole einfach die Konfiguration für jeden Raum mit dem entsprechenden Temperatursensor. Jeder virtuelle Sensor arbeitet völlig unabhängig.

**Beispiel-Setup:**
```
binary_sensor.fenster_wohnzimmer (sensor.temperatur_wohnzimmer)
binary_sensor.fenster_schlafzimmer (sensor.temperatur_schlafzimmer)
binary_sensor.fenster_kueche (sensor.temperatur_kueche)
binary_sensor.fenster_bad (sensor.temperatur_bad)
```

### Parameter später anpassen

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Finde "Virtual Window Sensor"
3. Klicke auf **Konfigurieren** beim gewünschten Sensor
4. Passe die Werte an
5. Speichern

## 🚀 Verwendung

Nach der Konfiguration verhält sich der Sensor wie ein normaler Fenstersensor:

- **Entity ID**: `binary_sensor.fenster_[name]`
- **Device Class**: `window`
- **Zustände**: `on` (offen) / `off` (geschlossen)

### Attribute

Der Sensor stellt zusätzliche Informationen bereit:

```yaml
temperature: 20.8              # Aktuelle Temperatur
previous_temperature: 21.5      # Temperatur vor X Sekunden
calculated_drop: 0.7           # Berechneter Temperaturabfall
temperature_drop: 0.3          # Konfigurierte Schwelle
time_window: 30                # Konfiguriertes Zeitfenster
```

## 💡 Beispiel-Automationen

### Heizung ausschalten bei offenem Fenster

```yaml
automation:
  - alias: "Heizung aus wenn Fenster offen"
    trigger:
      - platform: state
        entity_id: binary_sensor.fenster_wohnzimmer
        to: "on"
        for: "00:01:00"  # 1 Minute Verzögerung
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.wohnzimmer
        data:
          hvac_mode: "off"
      - service: notify.mobile_app
        data:
          title: "Heizung ausgeschaltet"
          message: "Fenster im Wohnzimmer ist offen - Heizung wurde ausgeschaltet"
```

### Heizung wieder einschalten

```yaml
automation:
  - alias: "Heizung an wenn Fenster geschlossen"
    trigger:
      - platform: state
        entity_id: binary_sensor.fenster_wohnzimmer
        to: "off"
        for: "00:05:00"  # 5 Minuten geschlossen
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.wohnzimmer
        data:
          hvac_mode: "heat"
```

### Benachrichtigung bei lang offenem Fenster

```yaml
automation:
  - alias: "Warnung - Fenster lange offen"
    trigger:
      - platform: state
        entity_id: binary_sensor.fenster_schlafzimmer
        to: "on"
        for: "00:30:00"  # 30 Minuten
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Fenster offen"
          message: "Fenster im Schlafzimmer ist seit 30 Minuten offen!"
          data:
            priority: high
```

### Dashboard Card

```yaml
type: entities
title: Fensterstatus
entities:
  - entity: binary_sensor.fenster_wohnzimmer
    name: Wohnzimmer
  - entity: binary_sensor.fenster_schlafzimmer
    name: Schlafzimmer
  - entity: binary_sensor.fenster_kueche
    name: Küche
  - entity: binary_sensor.fenster_bad
    name: Badezimmer
show_header_toggle: false
```

## 🔍 Fehlersuche

### Der Sensor reagiert nicht auf geöffnete Fenster

**Mögliche Ursachen:**
- Temperaturschwelle zu hoch → Verringere auf 0.2°C
- Zeitfenster zu kurz → Erhöhe auf 45s
- Temperatursensor aktualisiert zu langsam → Prüfe Update-Intervall des Sensors

**Lösung:**
```yaml
# Aktiviere Debug-Logging
logger:
  default: warning
  logs:
    custom_components.virtual_window_sensor: debug
```

Dann in **Einstellungen → System → Protokolle** die Debug-Ausgaben prüfen.

### Zu viele Fehlalarme

**Mögliche Ursachen:**
- Temperaturschwelle zu niedrig
- Normale Temperaturschwankungen im Raum
- Heizung schaltet sich ein/aus

**Lösungen:**
- Erhöhe die Temperaturschwelle auf 0.5°C oder mehr
- Verringere das Zeitfenster auf 20s
- Platziere den Temperatursensor weiter von Heizung/Klimaanlage entfernt

### Sensor zeigt immer "off"

**Prüfe:**
1. Ist der Temperatursensor aktiv?
   ```
   Entwicklerwerkzeuge → Zustände → Suche nach dem Temperatursensor
   ```
2. Liefert der Sensor Werte?
3. Teste mit sehr niedrigen Werten:
   - Temperaturschwelle: 0.1°C
   - Zeitfenster: 60s

## 🛠️ Technische Details

### Funktionsweise

Die Integration verwendet eine **Deque** (Double-ended Queue) um die letzten 100 Temperaturmesswerte mit Zeitstempeln zu speichern:

```python
[(timestamp1, temp1), (timestamp2, temp2), ..., (timestamp100, temp100)]
```

Bei jeder Temperaturänderung:
1. Neue Messung wird hinzugefügt
2. Alte Messungen (älter als Zeitfenster + 60s) werden entfernt
3. Temperatur von vor X Sekunden wird gesucht (±10s Toleranz)
4. Differenz wird berechnet
5. Status wird aktualisiert

### Voraussetzungen

- **Home Assistant**: Version 2024.1.0 oder neuer
- **Temperatursensor**: Beliebiger Sensor mit Device Class `temperature`
- **Update-Intervall**: Mindestens alle 30 Sekunden (besser: alle 10-15s)

### Performance

- **CPU-Last**: Minimal (nur bei Temperaturänderungen)
- **Speicher**: ~1 KB pro Sensor (100 Messwerte à 10 Bytes)
- **Netzwerk**: Keine externe Kommunikation

## 🤝 Beitragen

Contributions sind willkommen! 

- 🐛 **Bug Reports**: [Issues](https://github.com/tgast/home-assistant-virtual-window-sensor/issues)
- 💡 **Feature Requests**: [Issues](https://github.com/tgast/home-assistant-virtual-window-sensor/issues)
- 🔧 **Pull Requests**: Gerne! Siehe [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 Changelog

### Version 1.0.0 (2024-11-29)
- 🎉 Erste Veröffentlichung
- ✅ UI-Konfiguration
- ✅ Mehrsprachige Unterstützung (DE/EN)
- ✅ Konfigurierbare Parameter
- ✅ HACS-Kompatibilität

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE)

## 🙏 Danksagungen

- Home Assistant Community für Inspiration und Support
- Alle Contributors und Tester

## 💬 Support & Community

- **Fragen?** → [GitHub Discussions](https://github.com/tgast/home-assistant-virtual-window-sensor/discussions)
- **Probleme?** → [GitHub Issues](https://github.com/tgast/home-assistant-virtual-window-sensor/issues)
- **Home Assistant Forum**: [Community Thread](https://community.home-assistant.io/)

---

**Entwickelt mit ❤️ für die Home Assistant Community**

⭐ **Gefällt dir diese Integration?** Gib dem Projekt einen Star auf GitHub!
