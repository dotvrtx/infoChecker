# infoChecker

A cross-platform Python utility that collects and displays detailed system and network information, including hardware details, IP addresses, MAC addresses, locale settings, timezone information, and browser-like HTTP headers.

## Features

### System Information

* Hostname
* Operating System
* OS Release & Version
* CPU Architecture
* Processor Information
* Python Version
* Locale Settings
* Timezone

### Network Information

* MAC Addresses from all available interfaces
* IPv4 Addresses
* IPv6 Addresses
* Primary Local Network Address

### Browser Header Generation

Generates realistic browser-style HTTP request headers including:

* User-Agent
* Accept
* Accept-Language
* Accept-Encoding
* Cache-Control
* Connection Settings

### Cross-Platform Support

* Windows
* Linux
* macOS

## Installation

Clone the repository:

```bash
git clone https://github.com/dotvrtx/infoChecker.git
cd infoChecker
```

Install optional dependencies:

```bash
pip install psutil
```

> `psutil` is optional but recommended for accurate network interface detection.

## Usage

Run the script:

```bash
python device_info.py
```



## Dependencies
* Python
### Optional

* psutil

Install:

```bash
pip install psutil
```

## Project Structure

```text
device_info.py
```

## How It Works

The application gathers information using:

* Python's built-in `platform` module
* Network socket APIs
* System environment variables
* `psutil` (when available)
* Platform-specific commands such as:

  * `tzutil` (Windows)
  * `ipconfig` (Windows fallback)

Fallback methods are included to ensure the tool continues working even when optional dependencies are unavailable.

## Privacy

This tool:

* Does not send data to external servers
* Does not store collected information
* Displays information locally in the terminal only

