# Router Scheduled Restart Automation

This script automates restart router in specified schedule using Selenium WebDriver.

## Prerequisites

### System Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y python3 python3-pip unzip wget curl xvfb
```

### Create Virtual Enviroment for Python (OPTIONAL)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

### Python Dependencies

```bash
# Install Python packages
pip3 install selenium
pip install python-dotenv
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

1. Create a `.env` file in the project root directory:

```bash
touch .env
```

2. Add your Naukri.com credentials to the `.env` file:

```plaintext
AIRTEL_ROUTER_USERNAME=your.email@example.com
AIRTEL_ROUTER_PASSWORD=your_password
```

⚠️ **Important**: Never commit your `.env` file to version control. Add it to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

## Running the Script

```bash
python3 <SCRIPT_NAME>.py
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



