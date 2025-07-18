const FAQs = [
  {
    question: "what is hyperrcompute",
    description: "Hyperrcompute is a decentralized GPU marketplace that allows peer-to-peer GPU sharing. You can rent or offer compute power without centralized control.",
    commands: []
  },
  {
    question: "how to install hyperrcompute on windows",
    description: "To install Hyperrcompute on Windows, follow these steps:",
    commands: [
      "wsl --install", // Run in PowerShell as Administrator
      "Install Ubuntu from Microsoft Store",
      "Install Docker Desktop and enable WSL2 integration",
      "Install Node.js v18+ using nvm",
      "npm i hyperrcompute@0.0.12 -g"
    ]
  },
  {
    question: "how to install hyperrcompute on linux",
    description: "To install Hyperrcompute on a Linux system:",
    commands: [
      "sudo apt update && sudo apt upgrade -y",
      "sudo apt install docker.io docker-compose",
      "sudo usermod -aG docker $USER",
      "Install Node.js v18+ using nvm",
      "npm i hyperrcompute@0.0.12 -g"
    ]
  },
  {
    question: "how to install hyperrcompute on mac",
    description: "To install Hyperrcompute on macOS:",
    commands: [
      "Install Docker Desktop for Mac",
      "Install Node.js v18+ using nvm",
      "npm i hyperrcompute@0.0.12 -g"
    ]
  },
  {
    question: "how to earn from hyperrcompute",
    description: "You earn by sharing your GPU. Once you install and set up Hyperrcompute, you can run it in 'live' mode and accept jobs.",
    commands: [
      "hyperrcompute --image <YOUR_DOCKER_IMAGE> --live --connector <CONNECTION_STRING> --userId <YOUR_USER_ID>"
    ]
  },
  {
    question: "how to run a gpu job",
    description: "To run a job on a GPU node using live mode:",
    commands: [
      "hyperrcompute --image <DOCKER_IMAGE> --hours 1 --minutes 30 --force --live --connector <CONNECTOR_KEY> --userId <USER_ID>"
    ]
  },
  {
    question: "how to connect to existing gpu server",
    description: "To connect to a running GPU session remotely:",
    commands: [
      'hyperrcompute --connect "<CONNECTOR_KEY>" --port 5050',
      "Visit the returned URL to open the terminal (e.g. http://hyperrcompute.com/hyperrcompute/terminal?key=...)"
    ]
  },
  {
    question: "is hyperrcompute secure",
    description: "Yes, Hyperrcompute sessions are encrypted and peer-to-peer. You decide the container, job duration, and connection.",
    commands: []
  },
  {
    question: "does hyperrcompute support docker",
    description: "Yes. All workloads are containerized. You can run any Docker image using the CLI.",
    commands: [
      "hyperrcompute --image <YOUR_IMAGE> --live"
    ]
  },
  {
    question: "can i use hyperrcompute without nodejs",
    description: "Yes. On Linux, you can download the native binary and run Hyperrcompute without Node.js.",
    commands: [
      "./hyperrcompute-linux --image <IMAGE> --live"
    ]
  },
  {
    question: "what is a connector key",
    description: "A connector key is a secure key used to access your containerized GPU session. You generate it from the dashboard when setting up a session.",
    commands: []
  },
  {
    question: "what is live mode",
    description: "Live mode lets you stream container logs and status in real time. It is useful for debugging or interactive jobs.",
    commands: [
      "--live"
    ]
  }
];

export default FAQs;
