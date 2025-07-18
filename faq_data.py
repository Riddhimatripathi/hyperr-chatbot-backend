# faq_data.py

faq_list = [
    {
        "question": "what is hyperrcompute",
        "answer": (
            "Hyperrcompute is a decentralized GPU computing network that allows users "
            "to share their idle GPU power and earn credits or tokens in return. "
            "It is like a distributed cloud GPU platform, enabling faster ML, AI, and rendering tasks."
        )
    },
    {
        "question": "how to install hyperrcompute on windows",
        "answer": (
            "To install Hyperrcompute on Windows:\n"
            "1. Open PowerShell as Administrator\n"
            "2. Run: `wsl --install`\n"
            "3. Restart your system\n"
            "4. Open Microsoft Store and install Ubuntu\n"
            "5. Open Ubuntu terminal and run:\n"
            "   `sudo apt update && sudo apt install curl git`\n"
            "6. Install NVM:\n"
            "   `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash`\n"
            "7. Reload terminal: `source ~/.bashrc`\n"
            "8. Install Node.js: `nvm install 18 && nvm use 18`\n"
            "9. Install Hyperrcompute:\n"
            "   `npm i hyperrcompute@0.0.12 -g`\n"
        )
    },
    {
        "question": "how to install hyperrcompute on linux",
        "answer": (
            "To install Hyperrcompute on Linux:\n"
            "1. Open your terminal\n"
            "2. Install Node.js v18+ using NVM:\n"
            "   `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash`\n"
            "   `source ~/.bashrc`\n"
            "   `nvm install 18`\n"
            "3. Install Hyperrcompute globally:\n"
            "   `npm i hyperrcompute@0.0.12 -g`"
        )
    },
    {
        "question": "how to earn from hyperrcompute",
        "answer": (
            "You earn by contributing your GPU to the Hyperrcompute network.\n"
            "Steps to earn:\n"
            "1. Install Hyperrcompute and log in with your user ID.\n"
            "2. Use live mode to contribute:\n"
            "   `hyperrcompute --live --user <your_user_id>`\n"
            "3. Keep your machine running while jobs are being assigned.\n"
            "4. You will be rewarded based on GPU contribution time and load."
        )
    },
    {
        "question": "how to check my earnings",
        "answer": (
            "To check your earnings:\n"
            "1. Visit: `https://hyperrcompute.network/dashboard`\n"
            "2. Log in with your user credentials.\n"
            "3. View usage stats, earnings, and GPU contribution logs."
        )
    },
    {
        "question": "how to update hyperrcompute",
        "answer": (
            "To update to the latest version:\n"
            "`npm install -g hyperrcompute@latest`\n"
            "Make sure your Node.js version is at least 18."
        )
    },
    {
        "question": "hyperrcompute not recognized as command",
        "answer": (
            "This usually happens if global npm packages are not added to PATH.\n"
            "Try running:\n"
            "`export PATH=$PATH:$(npm bin -g)`\n"
            "Also confirm that Node.js and npm are correctly installed using:\n"
            "`node -v` and `npm -v`"
        )
    },
    {
        "question": "how to run in silent mode",
        "answer": (
            "To run Hyperrcompute in silent mode (no terminal output):\n"
            "`hyperrcompute --live --user <your_id> > /dev/null 2>&1 &`\n"
            "This will run it in background on Linux/macOS. On Windows, use PowerShell background execution."
        )
    },
    {
        "question": "what gpu is best for hyperrcompute",
        "answer": (
            "NVIDIA GPUs are preferred for maximum compatibility.\n"
            "Recommended GPUs:\n"
            "- RTX 3060 or higher for solid performance\n"
            "- RTX 4090 for enterprise-level contribution\n"
            "- Ensure your drivers are updated and CUDA is supported"
        )
    },
    {
        "question": "is my data secure on hyperrcompute",
        "answer": (
            "Yes, your data is safe. Hyperrcompute only executes containerized or isolated jobs.\n"
            "It does not access personal files or interfere with your system.\n"
            "You control when to stop or pause contributions."
        )
    },
    {
        "question": "how to stop hyperrcompute",
        "answer": (
            "To stop a running Hyperrcompute session:\n"
            "- Press `Ctrl+C` in the terminal if it's running interactively\n"
            "- Or kill the background process using `ps aux | grep hyperrcompute` and `kill <PID>`"
        )
    },
    {
        "question": "how to uninstall hyperrcompute",
        "answer": (
            "To uninstall Hyperrcompute:\n"
            "`npm uninstall -g hyperrcompute`\n"
            "Also remove config files (optional):\n"
            "`rm -rf ~/.hyperrcompute`"
        )
    },
    {
        "question": "how to contact hyperrcompute support",
        "answer": (
            "You can contact support via:\n"
            "- Email: support@hyperrcompute.network\n"
            "- Discord: https://discord.gg/hyperrcompute\n"
            "- Website chat: https://hyperrcompute.network"
        )
    },
    {
        "question": "where are hyperrcompute logs stored",
        "answer": (
            "Logs are stored in your home directory:\n"
            "Linux/macOS: `~/.hyperrcompute/logs`\n"
            "Windows (WSL): `/home/<user>/.hyperrcompute/logs`"
        )
    },
    {
        "question": "how to run multiple gpu nodes",
        "answer": (
            "To run multiple GPU nodes:\n"
            "1. Set up separate Docker containers or VMs.\n"
            "2. Install Hyperrcompute inside each one.\n"
            "3. Assign different user IDs or machine tags to track performance."
        )
    }
]
