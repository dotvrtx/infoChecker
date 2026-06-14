import locale
import os
import platform
import socket
import subprocess
import sys
import uuid


def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "locale": locale.getdefaultlocale(),
        "timezone": get_timezone_name(),
    }


def get_timezone_name():
    try:
        if sys.platform == "win32":
            tz_output = subprocess.check_output(["tzutil", "/g"], text=True, errors="ignore")
            return tz_output.strip()
        else:
            return os.environ.get("TZ", "unknown")
    except Exception:
        return "unknown"


def get_mac_addresses():
    macs = {}
    try:
        import psutil

        for if_name, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK or getattr(addr, "family", None) == socket.AF_PACKET:
                    if addr.address and addr.address != "00:00:00:00:00:00":
                        macs[if_name] = addr.address
    except Exception:
        pass

    if not macs:
        node = uuid.getnode()
        if (node >> 40) % 2 == 0:
            mac = ":".join(f"{(node >> ele) & 0xFF:02x}" for ele in range(40, -1, -8))
            macs["default"] = mac

    if not macs:
        # Windows fallback using ipconfig
        if sys.platform == "win32":
            try:
                output = subprocess.check_output(["ipconfig", "/all"], text=True, errors="ignore")
                for line in output.splitlines():
                    if "Physical Address" in line or "Physical Address" in line:
                        parts = line.split(":")
                        if len(parts) >= 2:
                            macs[f"iface_{len(macs)+1}"] = parts[1].strip().replace("-", ":")
            except Exception:
                pass

    return macs


def get_ip_addresses():
    ip_info = {"ipv4": {}, "ipv6": {}}
    try:
        import psutil

        for if_name, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ip_info["ipv4"][if_name] = addr.address
                elif addr.family == socket.AF_INET6:
                    ip_info["ipv6"][if_name] = addr.address.split("%")[0]
    except Exception:
        pass

    if not ip_info["ipv4"] and not ip_info["ipv6"]:
        try:
            hostname = socket.gethostname()
            for info in socket.getaddrinfo(hostname, None):
                family = info[0]
                addr = info[4][0]
                if family == socket.AF_INET:
                    ip_info["ipv4"]["resolved"] = addr
                elif family == socket.AF_INET6:
                    ip_info["ipv6"]["resolved"] = addr
        except Exception:
            pass

    # Add primary local address if possible
    if not ip_info["ipv4"].get("local"):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_info["ipv4"]["local"] = s.getsockname()[0]
            s.close()
        except Exception:
            pass

    return ip_info


def get_browser_like_info():
    system = platform.system()
    release = platform.release()
    architecture = platform.machine()

    user_agent = (
        f"Mozilla/5.0 ({system} {release}; {architecture}) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) Python/{platform.python_version()}"
    )
    language = locale.getdefaultlocale()[0] or "en-US"

    return {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": language.replace("_", "-"),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }


def print_pair(key, value, indent=0):
    prefix = " " * indent
    print(f"{prefix}{key}: {value}")


def print_section(title, content_func):
    print(f"{title}")
    print("-" * len(title))
    content_func()
    print()


def print_dict(title, data, indent=2):
    if not data:
        print_pair(title, "(none)")
        return

    print(f"{title}")
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print_pair(sub_key, sub_value, indent=4)
        else:
            print_pair(key, value, indent=2)


def main():
    print_section("System Information", lambda: print_dict("", get_system_info(), indent=2))
    print_section("MAC Addresses", lambda: print_dict("", get_mac_addresses(), indent=2))
    print_section("IP Addresses", lambda: print_dict("", get_ip_addresses(), indent=2))
    print_section("Browser-like Headers", lambda: print_dict("", get_browser_like_info(), indent=2))


if __name__ == "__main__":
    main()
