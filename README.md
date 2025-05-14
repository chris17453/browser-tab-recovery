# Browser Tab Recovery

A Python utility for recovering tabs and browsing history from Chrome and Vivaldi browsers on Linux systems.

## Features

- Recovers recently visited URLs from browser history
- Works with both Google Chrome and Vivaldi browsers
- Automatically detects browser installations (both standard and Flatpak)
- Lists available session files
- Command-line options for browser selection and time range

## Requirements

- Python 3.6+
- Fedora/CentOS or other Linux distribution
- Chrome and/or Vivaldi browser installed

## Installation

1. Clone this repository or download the script:

```bash
git clone https://github.com/chris17453/browser-tab-recovery.git
cd browser-tab-recovery
```your

2. Make the script executable:

```bash
chmod +x recover.py
```

## Usage

### Basic Usage

Run the script without arguments to check both Chrome and Vivaldi for tabs from the last 24 hours:

```bash
./recover.py
```

### Command-line Options

Specify which browser to check:

```bash
# Check only Chrome
./recover.py --browser chrome

# Check only Vivaldi
./recover.py --browser vivaldi
```

Look back more than one day:

```bash
# Look back 7 days
./recover.py --days 7
```

Combine options:

```bash
# Check Chrome tabs from the last 3 days
./recover.py --browser chrome --days 3
```

## How It Works

The script:

1. Identifies browser data directories for Chrome and Vivaldi
2. Lists session files that might contain tab information
3. Creates a temporary copy of the browser's history database
4. Queries the database for recently visited URLs
5. Displays the results sorted by most recent first

## Notes

- For best results, close the browser before running the script
- The script does not modify any browser data (read-only operation)
- Session files are binary and cannot be easily parsed, but the script will show if they exist
- The history database provides the most reliable method of recovering recent browsing activity

## License

This project is licensed under the BSD 3-Clause License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.