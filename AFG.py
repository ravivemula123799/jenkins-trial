import sys
from frequency_module import FunctionGenerator, parse_frequency, InvalidFrequencyError, set_frequency

def main():
    while True:
        # Ask user to enter a frequency or exit the program
        user_input = input("Enter a frequency (e.g., '1Hz' or just '50Hz') or 'exit' to quit: ").strip()
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            sys.exit()

        # Ask user for the waveform type (only RAMP or CONTINUOUS allowed)
        waveform_input = input("Enter the waveform type (RAMP): ").strip().upper()

        # Ensure valid waveform input
        if waveform_input not in ['RAMP']:
            print("Invalid waveform type. Please enter either 'RAMP'.")
            continue

        # Store waveform choice
        waveform = waveform_input

        # If waveform is 'RAMP', ask for mode input
        mode = None
        if waveform == 'RAMP':
            mode = input("Enter the mode (Continuous): ").strip().capitalize()
            if mode != 'RAMP':
                print("Invalid mode for RAMP waveform. Please enter 'Continuous'.")
                #continue

        # Ask for the channel number (CH1 or CH2)
        channel = input("Select the fg channel either CH1 or CH2: ").strip().upper().lstrip("CH")
        if not channel.isdigit():
            print("Invalid channel number. Please enter a valid channel (e.g., 'CH1').")
            continue

        # Ask for scope channel input
        ch_scope = input("Select the scope channel either CH1, CH2, CH3, or CH4: ").strip().upper().lstrip("CH")
        if not ch_scope.isdigit():
            print("Invalid channel number. Please enter a valid channel (e.g., 'CH1').")
            continue

        # Ask for phase input (either maximum, minimum, or numeric value)
        phase_input = input("Enter the phase (e.g., 'maximum', 'minimum', or a number): ").strip()
        if phase_input in ['maximum', 'minimum']:
            phase = (lambda s: s[:4].upper() + s[4:].lower())(phase_input)
        else:
            try:
                phase = float(phase_input)
            except ValueError:
                print("Invalid phase input.")
                continue

        # Ask for amplitude input
        amplitude = input("Enter the float value for amplitude (in volts): ")

        # Open the log file and write the user's configuration
        with open('AWG_log.csv', 'w') as file:
            original_stdout = sys.stdout
            sys.stdout = file
            
            try:
                print(f"Valid frequency ranges for RAMP and CONTINUOUS:\nRAMP: 1 µHz to 8 kHz\nCONTINUOUS: 1 µHz to 50 MHz")
                print(f"Channel set to CH{channel}\nWaveform is set to {waveform}\nPhase is set to {phase}\nAmplitude is set to {amplitude} Vpp")
                
                # Call the set_frequency function with the user's input
                set_frequency(channel, user_input, waveform, mode, phase, amplitude, ch_scope)
            
            finally:
                # Restore the original stdout
                sys.stdout = original_stdout
                
                # Optionally print a message to the console
                print("Log has been written to AWG_log.csv")

# Call the main function
main()

