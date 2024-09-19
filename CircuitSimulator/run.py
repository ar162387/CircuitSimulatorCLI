import sys
from input_parser import parse_emitter, parse_receiver, parse_size, parse_pulse_sequence, parse_mirror
from emitter import Emitter
from receiver import Receiver
from mirror import Mirror
from laser_circuit import LaserCircuit

'''
Name:   Mingyu Du
SID:    540227714
Unikey: midu0228

run - Runs the entire program. It needs to take in the inputs and process them
into setting up the circuit. The user can specify optional flags to perform
additional steps, such as -RUN-MY-CIRCUIT to run the circuit and -ADD-MY-MIRRORS
to include mirrors in the circuit.

You are free to add more functions, as long as you aren't modifying the
existing scaffold.
'''


def is_run_my_circuit_enabled(args: list[str]) -> bool:
    # only requires implementation once you reach RUN-MY-CIRCUIT
    '''
    Returns whether or not '-RUN-MY-CIRCUIT' is in args.

    Parameters
    ----------
    args - the command line arguments of the program
    '''
    target = '-RUN-MY-CIRCUIT'
    i = 0
    while i < len(args):
        if args[i] == target:
            return True
        i += 1
    return False


def is_add_my_mirrors_enabled(args: list[str]) -> bool:
    # only requires implementation once you reach ADD-MY-MIRRORS
    '''
    Returns whether or not '-ADD-MY-MIRRORS' is in args.

    Parameters
    ----------
    args - the command line arguments of the program
    '''
    target = '-ADD-MY-MIRRORS'
    index = 0
    while index < len(args):
        if args[index] == target:
            return True
        index += 1
    return False


def initialise_circuit() -> LaserCircuit:
    # only requires implementation once you reach GET-MY-INPUTS
    '''
    Gets the inputs for the board size, emitters and receivers and processes
    it to create a LaserCircuit instance and return it. You should be using
    the functions you have implemented in the input_parser module to handle
    validating each input.

    Returns
    -------
    A LaserCircuit instance with a width and height specified by the user's
    inputted size. The circuit should also include each emitter and receiver
    the user has inputted.
    '''
    # Initialize variables
    circuit = None
    emitters_added = 0
    receivers_added = 0

    print('Creating circuit board...')
    # validate board size
    while True:

        board_size_input = input("> ")
        size = parse_size(board_size_input)
        if size is not None:
            circuit = LaserCircuit(size[0], size[1])
            print(f"{size[0]}x{size[1]} board created.\n")
            break

    # Add emitters
    print("Adding emitter(s)...")
    while emitters_added < 10:
        emitter_input = input("> ")
        if emitter_input == "END EMITTERS":
            break
        emitter = parse_emitter(emitter_input)
        if emitter is not None:
            if circuit.add_emitter(emitter):
                emitters_added += 1

    print(f"{emitters_added} emitter(s) added.\n")

    # Add receivers
    print("Adding receiver(s)...")
    while receivers_added < 10:
        receiver_input = input("> ")
        if receiver_input == "END RECEIVERS":
            break
        receiver = parse_receiver(receiver_input)
        if receiver is not None:
            # Assuming add_receiver method exists on LaserCircuit
            if circuit.add_receiver(receiver):
                receivers_added += 1

    print(f"{receivers_added} receiver(s) added.\n")

    return circuit


def set_pulse_sequence(circuit: LaserCircuit, file_obj) -> None:
    # only requires implementation once you reach RUN-MY-CIRCUIT
    '''
    Handles setting the pulse sequence of the circuit. 
    The lines for the pulse sequence will come from the a file named
    input/<file_name>.in. 
    You should be using the functions you have implemented in the input_parser module 
    to handle validating lines from the file.

    Parameter
    ---------
    circuit - The circuit to set the pulse sequence for.
    file_obj - A file like object returned by the open()
    '''
    print("Setting pulse sequence...")
    emitters = circuit.get_emitters()
    emitter_dict = {}
    emitter_symbols = []

    # Initialize emitter dictionary and symbols list
    index = 0
    while index < len(emitters):
        emitter = emitters[index]
        emitter_dict[emitter.symbol] = emitter
        emitter_symbols.append(emitter.symbol)
        index += 1

    line_number = 0
    while True:
        line = file_obj.readline()
        if line == '':  # End of file reached
            break
        line_number += 1

        if len(emitter_symbols) == 0:
            break

        print("-- ({})".format(', '.join(emitter_symbols)))

        result = parse_pulse_sequence(line)
        if result is None:
            print(f"Line {line_number}: {line.strip()}")
            print("Error: Invalid pulse sequence configuration.")
            continue

        emitter_symbol, frequency, direction = result
        emitter = emitter_dict.get(emitter_symbol, None)

        if emitter is None:
            print(f"Line {line_number}: {line.strip()}")
            print(f"Error: emitter '{emitter_symbol}' does not exist")
        elif emitter.is_pulse_sequence_set():
            print(f"Line {line_number}: {line.strip()}")
            print(
                f"Error: emitter '{emitter_symbol}' already has its pulse sequence set")
        else:
            emitter.set_pulse_sequence(frequency, direction)
            print(f"Line {line_number}: {line.strip()}")

        # Remove set emitter from the list and update display
        if emitter and emitter.is_pulse_sequence_set():
            emitter_symbols.remove(emitter_symbol)

    print("Pulse sequence set.\n")


def add_mirrors(circuit: LaserCircuit) -> None:
    # only requires implementation once you reach ADD-MY-MIRRORS
    '''
    Handles adding the mirrors into the circuit. You should be using the
    functions you have implemented in the input_parser module to handle
    validating each input. 

    Parameters
    ----------
    circuit - the laser circuit to add the mirrors into
    '''
    print("Adding mirror(s)...")
    mirror_count = 0

    while True:
        user_input = input("> ")
        if user_input == "END MIRRORS":
            break

        mirror = parse_mirror(user_input)
        if mirror is None:
            continue  # parse_mirror already prints errors

        # Attempt to add the mirror to the circuit
        if circuit.add_mirror(mirror):
            mirror_count += 1

    print(f"{mirror_count} mirror(s) added.")


def main(args: list[str]) -> None:
    # only requires implementation once you reach GET-MY-INPUTS
    # will require extensions in RUN-MY-CIRCUIT and ADD-MY-MIRRORS
    '''
    Responsible for running all code related to the program.

    Parameters
    ----------
    args - the command line arguments of the program
    '''

    circuit = initialise_circuit()

    # Check for ADD-MY-MIRRORS flag
    if not is_add_my_mirrors_enabled(args):

        print("\n<ADD-MY-MIRRORS FLAG DETECTED!>")
        add_mirrors(circuit)
        print('')

    circuit.print_board()
    print('')

    # Check if the RUN-MY-CIRCUIT flag is present in the args
    if not is_run_my_circuit_enabled(args):
        print("<RUN-MY-CIRCUIT FLAG DETECTED!>\n")

        try:
            # Try to open the input file to check if it exists
            with open('input/pulse_sequence.in', 'r') as file_obj:
                # If the file opens successfully, set the pulse sequence
                set_pulse_sequence(circuit, file_obj)

            # After setting pulse sequence, check if all pulses are set
            if circuit.is_all_pulse_set():
                circuit.run_circuit()

        except FileNotFoundError:
            print(
                "Error: -RUN-MY-CIRCUIT flag detected but input/pulse_sequence.in does not exist")


if __name__ == '__main__':
    '''
    Entry point of program. We pass the command line arguments to our main
    program. We do not recommend modifying this.
    '''
    main(sys.argv)
