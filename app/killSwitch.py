def killSwitch(command):
    if command.strip().upper() in ["EXIT", "2", "QUIT", "Q"]:
        print("Exiting PulseCheck...")
        exit(0)
