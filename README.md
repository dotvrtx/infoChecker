# System Information Collector

A lightweight Python utility that gathers and displays system, network, and browser-like environment information. The script is designed to work across multiple operating systems and includes fallback mechanisms when certain libraries or APIs are unavailable.

## Features

### System Information

Collects:

* Hostname
* Operating system
* OS release and version
* CPU architecture
* Processor information
* Python version
* System locale
* Timezone

### Network Information

#### MAC Addresses

Attempts to retrieve MAC addresses from all available network interfaces using:

1. `psutil` (preferred method)
2. `uuid.getnode()` fallback
3. Windows `ipconfig /all` fallback

#### IP Addresses

Collects:

* IPv4 addresses
* IPv6 addresses
* Primary local network address

Uses:

1. `psutil.net_if_addrs()`
2. Hostname resolution fallback
3. UDP socket method for determining the primary local IP

### Browser-like Headers

Generates a set of HTTP headers that resemble those sent by a web browser, including:

* User-Agent
* Accept
* Accept-Language
* Accept-Encoding
* Connection
* Cache-Control
* Upgrade-Insecure-Requests

These values are generated dynamically based on the host system.

---

## Requirements

### Python Version

Python 3.7+

### Optional Dependency

For complete network interface information:

```bash
pip install psutil
```

Without `psutil`, the script will attempt to use built-in fallback methods where possible.

---

## Installation

Clone or download the script:

```bash
git clone https://github.com/yourusername/system-info-collector.git
cd system-info-collector
```

Install optional dependencies:

```bash
pip install psutil
```

---

## Usage

Run the script directly:

```bash
python device_info.py
```


Main components:

| Function                  | Description                                      |
| ------------------------- | ------------------------------------------------ |
| `get_system_info()`       | Collects operating system and Python information |
| `get_timezone_name()`     | Determines the system timezone                   |
| `get_mac_addresses()`     | Retrieves MAC addresses from network interfaces  |
| `get_ip_addresses()`      | Retrieves IPv4 and IPv6 addresses                |
| `get_browser_like_info()` | Generates browser-style HTTP headers             |
| `print_dict()`            | Formats dictionary output                        |
| `print_section()`         | Prints titled output sections                    |
| `main()`                  | Entry point of the application                   |

---

## Cross-Platform Support

| Platform | Supported |
| -------- | --------- |
| Windows  | ✅         |
| Linux    | ✅         |
| macOS    | ✅         |

Some timezone and network interface methods may vary depending on the operating system.

---

## Notes

* The script only collects information available on the local machine.
* No data is transmitted over the network.
* All information is displayed locally in the console.
* Installing `psutil` improves network interface detection accuracy.

---

## License

This project is released under the MIT License. Feel free to modify and distribute it.
