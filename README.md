# Flipper Bridge

**Flipper Bridge** is a Home Assistant custom integration that connects a **Flipper Zero** to Home Assistant via **USB serial** and allows you to send [Flipper CLI](https://docs.flipper.net/zero/development/cli) commands directly from Home Assistant.

This makes it easy to integrate Flipper Zero into automations, scripts, and dashboards — for example, triggering IR, Sub-GHz, GPIO, or other Flipper CLI features from Home Assistant.

## ✨ Features

* 🔌 USB serial connection to Flipper Zero
* 💬 Send arbitrary Flipper CLI commands from Home Assistant
* 🧠 Returns and logs Flipper CLI output
* ⚡ Local communication (no cloud)
* 🧪 Tested on [Home Assistant Green](https://www.home-assistant.io/green/)

## 📦 Installation (via HACS)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click **⋮ → Custom repositories**
4. Add this repository:

   ```
   https://github.com/markszabo/home-assistant-flipper-bridge
   ```

   Category: **Integration**
5. Install **Flipper Bridge**
6. Restart Home Assistant

## 🔧 Requirements

* Flipper Zero connected via USB
* Home Assistant with USB device access
  * For Docker: `/dev/ttyACM*` must be passed through

## ⚙️ Configuration

1. Go to:
   **Settings → Devices & Services → Add Integration**
2. Search for **Flipper Bridge**
3. Select the Flipper serial port (e.g. `/dev/ttyACM0`)
4. Set baud rate (default: `230400`)

## ▶️ Usage

### Send a CLI command (Developer Tools)

1. Go to **Developer Tools → Actions**
2. Select:

   ```
   flipper_bridge.send_cli
   ```
3. Enter the command you want to run (e.g. `help`)
4. See the response

### Use in an automation

```yaml
service: flipper_bridge.send_cli
data:
  command: subghz tx_from_file /ext/subghz/open.sub 1 0
```

## 📝 Notes

* Flipper CLI requires commands to end with `CRLF` (`\r\n`)
* CLI output may include ANSI color codes (these are stripped in Home Assistant)
* The first line of output may be the echoed command

## 🦾 AI usage

This was built with the help of AI (ChatGPT), but was reviewed and tested by humans.

## 🙌 Others

* If you want to manage IR remotes within HomeAssistant, this integration might be a better fit: [https://github.com/ClusterM/flipper_rc](https://github.com/ClusterM/flipper_rc)
