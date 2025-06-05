#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import platform

CONFIG_PATH = "/etc/proxychains4.conf"
BACKUP_PATH = "/etc/proxychains4.conf.bak"
DEPENDENCIES = ["tor", "proxychains4"]
INSTALL_PATH = "/usr/local/bin/mask"

def is_root():
    return os.geteuid() == 0

def auto_self_install():
    current_path = os.path.realpath(__file__)
    if current_path != INSTALL_PATH:
        print("[*] Installing mask globally to /usr/local/bin ...")
        if not is_root():
            print("[*] Root required. Re-running with sudo...")
            os.execvp("sudo", ["sudo", "python3"] + sys.argv)
        shutil.copy(current_path, INSTALL_PATH)
        os.chmod(INSTALL_PATH, 0o755)
        print(f"[+] Installed as {INSTALL_PATH}")
        print("[*] Relaunching as global command...")
        os.execv(INSTALL_PATH, ["mask"] + sys.argv[1:])

def run_command(cmd, check=True):
    print(f"[+] Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError as e:
        print(f"[!] Command failed: {e}")
        if check:
            sys.exit(1)

def show_banner():
    banner = r"""
 __  __           _    __ 
|  \/  |         | |  / /
| \  / | __ _ ___| |_/ /
| |\/| |/ _` / __| '  /
| |  | | (_| \__ \ |\ \ 
|_|  |_|\__,_|___/_| \_\   by nikhilvi_28 

  Automated Anonymity Toolkit for Kali Linux
     (Tor + Proxychains) — MASK
  Use responsibly — stay stealthy.
    """
    print(banner)

def check_os():
    if platform.system() != "Linux":
        print("[!] This script is intended for Linux systems only.")
        sys.exit(1)

def check_and_install_dependencies():
    for dep in DEPENDENCIES:
        if shutil.which(dep) is None:
            print(f"[*] Installing missing dependency: {dep}")
            run_command(f"apt update && apt install {dep} -y")
        else:
            print(f"[+] {dep} is already installed.")

def backup_config():
    if os.path.isfile(CONFIG_PATH):
        shutil.copy(CONFIG_PATH, BACKUP_PATH)
        print(f"[+] Backup created at {BACKUP_PATH}")

def configure_proxychains():
    if not os.path.isfile(CONFIG_PATH):
        print(f"[!] Config file not found: {CONFIG_PATH}")
        return

    backup_config()

    with open(CONFIG_PATH, "r") as file:
        lines = file.readlines()

    new_lines = []
    found_socks5 = False
    for line in lines:
        if "strict_chain" in line or "random_chain" in line:
            line = f"# {line.lstrip('#').strip()}\n"
        elif "dynamic_chain" in line:
            line = f"{line.lstrip('#')}"
        elif "proxy_dns" in line:
            line = f"{line.lstrip('#')}"
        elif line.strip().startswith("socks4") or line.strip().startswith("socks5"):
            if "socks5 127.0.0.1 9050" in line:
                found_socks5 = True
            continue
        new_lines.append(line)

    if not found_socks5:
        new_lines.append("socks5 127.0.0.1 9050\n")

    with open(CONFIG_PATH, "w") as file:
        file.writelines(new_lines)

    print("[+] Proxychains configuration updated for Tor.")

def install_all():
    if not is_root():
        print("[*] This operation requires root privileges. Re-running with sudo...")
        os.execvp("sudo", ["sudo"] + ["mask"] + sys.argv[1:])
    check_and_install_dependencies()
    configure_proxychains()
    start_tor()
    print("[+] Complete! Tor and Proxychains4 are ready.")

def start_tor():
    if not is_root():
        print("[*] This operation requires root privileges. Re-running with sudo...")
        os.execvp("sudo", ["sudo"] + ["mask"] + sys.argv[1:])
    run_command("systemctl start tor")
    run_command("systemctl enable tor")

def stop_tor():
    if not is_root():
        print("[*] This operation requires root privileges. Re-running with sudo...")
        os.execvp("sudo", ["sudo"] + ["mask"] + sys.argv[1:])
    run_command("systemctl stop tor")
    print("[+] Tor service stopped. You have exited Tor.")

def check_status():
    run_command("systemctl status tor", check=False)

def run_tool(tool_name):
    try:
        run_command(f"proxychains4 {tool_name}")
    except Exception as e:
        print(f"[!] Failed to run tool through proxychains: {e}")

def get_ip():
    run_tool("curl ipinfo.io/ip")

def restart_tor():
    if not is_root():
        print("[*] This operation requires root privileges. Re-running with sudo...")
        os.execvp("sudo", ["sudo"] + ["mask"] + sys.argv[1:])
    run_command("systemctl restart tor")
    print("[+] Tor restarted. New identity requested.")

def rotate_identity():
    import telnetlib
    try:
        password = input("Tor control password: ")
        tn = telnetlib.Telnet("127.0.0.1", 9051)
        tn.read_until(b"250 OK")
        tn.write(f'AUTHENTICATE "{password}"\n'.encode("ascii"))
        resp = tn.read_until(b"250 OK", 3)
        if b"250 OK" not in resp:
            print("[!] Authentication failed.")
            return
        tn.write(b"SIGNAL NEWNYM\n")
        if b"250 OK" in tn.read_until(b"250 OK", 3):
            print("[+] Tor identity rotated!")
        tn.write(b"QUIT\n")
        tn.close()
    except Exception as e:
        print(f"[!] Could not rotate Tor identity: {e}")

def help_menu():
    print("""
Usage:
    sudo mask install        # Auto install, configure, and start everything
    sudo mask start          # Start and enable Tor service
    sudo mask run <tool>     # Run any tool anonymously
    mask status              # Check Tor status
    sudo mask configure      # Configure Proxychains4 for Tor
    mask ip                  # Show Tor IP address
    sudo mask restart        # Restart Tor for new IP
    sudo mask exit           # Same as stop, exits Tor service
    mask rotate              # Rotate Tor identity (requires ControlPort config)
    """)

if __name__ == "__main__":
    auto_self_install()
    check_os()
    show_banner()

    if len(sys.argv) < 2:
        help_menu()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "install":
        install_all()
    elif command == "start":
        start_tor()
    elif command in ("exit"):
        stop_tor()
    elif command == "status":
        check_status()
    elif command == "configure":
        configure_proxychains()
    elif command == "run" and len(sys.argv) > 2:
        tool = ' '.join(sys.argv[2:])
        run_tool(tool)
    elif command == "ip":
        get_ip()
    elif command == "restart":
        restart_tor()
    elif command == "rotate":
        rotate_identity()
    else:
        help_menu()
