def killSwitch(command):
    if command.strip().upper() in ["EXIT", "4"]:
        print("Exiting PulseCheck...")
        exit(0)
