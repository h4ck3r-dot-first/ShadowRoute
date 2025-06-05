# MASK

**MASK** is an automated anonymity toolkit for Kali Linux and other Linux distributions. It seamlessly combines [Tor](https://www.torproject.org/) and [Proxychains4](https://github.com/haad/proxychains) to route your network traffic through the Tor network, making your online activities anonymous with minimal effort.

---

## ✨ Features

- **Automatic installation & configuration** of Tor and Proxychains4.
- One-command setup and usage.
- Easily run any tool (nmap, curl, sqlmap, etc.) anonymously via Tor.
- Automatic global installation: just run once, and you can use `mask` from anywhere.
- Rotate Tor identity (if ControlPort is enabled).
- See your Tor IP, check Tor status, and manage services easily.

---

## 🚀 How It Works

MASK configures your system to use Tor as a SOCKS5 proxy and sets up Proxychains4 to route any tool or command through Tor. You can then run any supported command anonymously, without manually setting up proxies.

---

## 🔧 Installation

1. **Download the script**

   ```
   wget https://raw.githubusercontent.com/your-repo/mask/main/mask.py
   chmod +x mask.py
   ```

2. **Run once to auto-install globally**

   ```
   python3 mask.py install
   ```

   - Or simply run any command (e.g., `python3 mask.py status`), and the script will install itself as `/usr/local/bin/mask`.

3. **After installation, use `mask` globally:**

   ```
   mask <command>
   ```

---

## 🕶️ Usage

### Quick Start

- **Install Tor & Proxychains4 and configure everything**
  ```
  sudo mask install
  ```

- **Start Tor service**
  ```
  sudo mask start
  ```

- **Run any tool anonymously**
  ```
  mask run <your_tool> [arguments...]
  ```
  _Examples:_
  ```
  mask run curl https://ifconfig.me
  mask run nmap -sT 1.1.1.1
  mask run sqlmap -u "http://target/vuln.php?id=1"
  ```

- **Check your Tor IP**
  ```
  mask ip
  ```

- **Check Tor status**
  ```
  mask status
  ```

- **Restart Tor for a new identity**
  ```
  sudo mask restart
  ```

- **Rotate Tor identity (requires Tor ControlPort setup)**
  ```
  mask rotate
  ```

- **Stop Tor service**
  ```
  sudo mask exit
  ```

---

## ℹ️ Notes

- Some commands (like `install`, `start`, `restart`, `exit`) require `sudo` because they interact with system services.
- For `mask run <tool>`, root is needed only if the tool itself needs root.
- To rotate identity, you must configure Tor's `ControlPort` and set a password in `/etc/tor/torrc`.

---

## ⚠️ Disclaimer

This tool is for **educational and legal use only**. Misuse may violate laws or terms of service. The author is not responsible for any illegal activity performed using this tool.

---

## 🛠️ Uninstall

Simply remove the file:
```
sudo rm /usr/local/bin/mask
```

---

## 🙋 Support

For bugs or feature requests, open an issue on the GitHub repository.

---
