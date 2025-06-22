# Router Restart Automation

This script automates router restarts on a specified schedule using Selenium WebDriver.

## Prerequisites

### System Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y python3 python3-pip unzip wget curl xvfb
```

### Create Virtual Environment for Python (OPTIONAL)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r scripts/requirement.txt
```

### Chrome Browser and ChromeDriver

```bash
# Install Chrome Browser
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y

# Install ChromeDriver (version 136.0.7103.94)
wget https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.94/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
sudo cp chrome-linux64/chrome /usr/local/bin
sudo chmod +x /usr/local/bin/chrome
```

## Environment Setup

1. Create a `.env` file in the `scripts/` directory:

```bash
touch scripts/.env
```

2. Add your router credentials and Discord webhook to the `.env` file:

```plaintext
AIRTEL_ROUTER_USERNAME=your_router_username
AIRTEL_ROUTER_PASSWORD=your_router_password
TPLINK_ROUTER_PASSWORD=your_tplink_password
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

⚠️ **Important**: Never commit your `.env` file to version control. It is already included in `.gitignore`.

## Running the Script

```bash
python3 scripts/Airtel-Router-reboot.py
python3 scripts/TpLink-Router-reboot.py
```

## Automatically Running as Cronjob
```bash
# Add to System CronJobs
crontab -e

# TpLink Router Restart Automation
0 4 * * * /home/hr/github-repo/Router-Restart-Automation/scripts/venv/bin/python3 /home/hr/github-repo/Router-Restart-Automation/scripts/TpLink-Router-reboot.py >> /home/hr/github-repo/Router-Restart-Automation/scripts/TpLink-Router-reboot.log 2>&1

# Airtel Router Restart Automation
10 4 * * * /home/hr/github-repo/Router-Restart-Automation/scripts/venv/bin/python3 /home/hr/github-repo/Router-Restart-Automation/scripts/Airtel-Router-reboot.py >> /home/hr/github-repo/Router-Restart-Automation/scripts/Airtel-Router-reboot.log 2>&1

# Verify using 
crontab -l
```

## Script Output

The script will generate screenshots at each step for verification in below patten:
- `1-*.png`
- `2-*.png`

## Error Handling

If any errors occur during execution, the script will:
1. Save an error screenshot
2. Print an error message
3. Close the browser
4. Exit with an error status



