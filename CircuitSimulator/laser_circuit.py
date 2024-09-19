from sorter import sort_receivers_by_activation_time, sort_receivers_by_total_energy
from emitter import Emitter
from receiver import Receiver
from photon import Photon
from mirror import Mirror
from board_displayer import BoardDisplayer

'''
Name:   Mingyu Du
SID:    540227714
Unikey: midu0228

LaserCircuit - Responsible for storing all the components of the circuit and
handling the computation of running the circuit. It's responsible for delegating
tasks to the specific components e.g. making each emitter emit a photon, getting
each photon to move and interact with components, etc. In general, this class is
responsible for handling any task related to the circuit.

You are free to add more attributes and methods, as long as you aren't
modifying the existing scaffold.
'''


class LaserCircuit:

    def __init__(self, width: int, height: int):
        '''
        Initialise a LaserCircuit instance given a width and height. All
        lists of components and photons are empty by default.
        board_displayer is initialised to a BoardDisplayer instance. clock is
        0 by default.

        emitters:        list[Emitter]  - all emitters in this circuit
        receivers:       list[Receiver] - all receivers in this circuit
        photons:         list[Photon]   - all photons in this circuit
        mirrors:         list[Mirror]   - all mirrors in this circuit
        width:           int            - the width of this circuit board
        height:          int            - the height of this circuit board
        board_displayer: BoardDisplayer - helper class for storing and
                                          displaying the circuit board
        clock:           int            - a clock keeping track of how many
                                          nanoseconds this circuit has run for

        Parameters
        ----------
        width  - the width to set this circuit board to
        height - the width to set this circuit board to
        '''
        self.width = width
        self.height = height
        self.board_displayer = BoardDisplayer(width, height)
        self.clock = 0

        # Initializing lists for circuit components
        self.emitters = []
        self.receivers = []
        self.photons = []
        self.mirrors = []

    def emit_photons(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Gets each emitter in this circuit's list of emitters to emit a photon.
        The photons emitted should be added to this circuit's photons list.
        '''
        index = 0
        while index < len(self.emitters):
            emitter = self.emitters[index]
            photon = emitter.emit_photon()
            self.photons.append(photon)
            index += 1

    def is_finished(self) -> bool:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Returns whether or not this circuit has finished running. The
        circuit is finished running if every photon in the circuit has been
        absorbed.

        Returns
        -------
        True if the circuit has finished running or not, else False.
        '''
        index = 0
        while index < len(self.photons):
            if not self.photons[index].is_absorbed():
                return False  # Found a photon that has not been absorbed
            index += 1
        return True  # All photons have been absorbed

    def print_emit_photons(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for each emitter emitting a photon.

        It will also need to write the output into a
        output/emit_photons.out output file.

        You can assume the output/ path exists.
        '''

        output_message = "0ns: Emitting photons.\n"
        file_contents = ""
        index = 0
        while index < len(self.emitters):
            emitter = self.emitters[index]
            emitter_details = str(emitter)
            output_message += emitter_details + "\n"
            file_contents += emitter_details + "\n"
            index += 1

        print(output_message, end='')

        file_path = "output/emit_photons.out"
        with open(file_path, "w") as file:
            file.write(file_contents)

    def print_activation_times(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for the activation times for each receiver, sorted
        by activation time in ascending order. Any receivers that have not
        been activated should not be included.

        It will also need to write the output into a
        output/activation_times.out output file.

        You can assume the output/ path exists.
        '''
        # Filter out receivers that are not activated
        activated_receivers = []
        index = 0
        print('')
        while index < len(self.receivers):
            if self.receivers[index].is_activated():
                activated_receivers.append(self.receivers[index])
            index += 1

        # Sort the activated receivers by activation time
        sorted_receivers = sort_receivers_by_activation_time(
            activated_receivers)

        # Prepare the output string
        output_message = "Activation times:\n"
        file_contents = ""
        index = 0
        while index < len(sorted_receivers):
            receiver = sorted_receivers[index]
            line = "R{}: {}ns\n".format(
                receiver.get_symbol(), receiver.get_activation_time())
            output_message += line
            file_contents += line
            index += 1

        # Print to console
        print(output_message)

        # Write to file
        file_path = "output/activation_times.out"
        with open(file_path, "w") as file:
            file.write(file_contents)

    def print_total_energy(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for the total energy absorbed for each receiver,
        sorted by total energy absorbed in descending order. Any receivers
        that have not been activated should not be included.

        It will also need to write the output into a
        output/total_energy_absorbed.out output file.

        You can assume the output/ path exists.
        '''
        # Filter out receivers that are not activated
        activated_receivers = []
        index = 0
        while index < len(self.receivers):
            if self.receivers[index].is_activated():
                activated_receivers.append(self.receivers[index])
            index += 1

        # Sort the activated receivers by total energy
        sorted_receivers = sort_receivers_by_total_energy(activated_receivers)

        # Prepare the output string
        output_message = "Total energy absorbed:\n"
        file_contents = ""
        index = 0
        while index < len(sorted_receivers):
            receiver = sorted_receivers[index]
            line = str(receiver)
            output_message += line + "\n"
            file_contents += line + "\n"
            index += 1

        # Print to console
        print(output_message)

        # Write to file
        file_path = "output/total_energy.out"
        with open(file_path, "w") as file:
            file.write(file_contents)

    def print_board(self) -> None:
        '''Calls the print_board method in board_displayer.'''
        self.board_displayer.print_board()

    def get_collided_emitter(self, entity: Emitter | Receiver | Photon | Mirror | None) -> Emitter | None:
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another emitter in the
        circuit.

        If it does, return the emitter already in the entity's position.
        Else, return None, indicating there is no emitter occupying entity's
        position.

        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        An emitter if it has the same position as entity, else None.
        '''
        # remove the line below once you start implementing this function
        index = 0
        while index < len(self.emitters):
            emitter = self.emitters[index]
            if emitter.x == entity.x and emitter.y == entity.y:
                return emitter
            index += 1
        return None

    def get_collided_receiver(self, entity: Emitter | Receiver | Photon | Mirror | None) -> Receiver | None:
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another receiver in the
        circuit.

        If it does, return the emitter already in the entity's position.
        Else, return None, indicating there is no receiver occupying entity's
        position.

        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        A receiver if it has the same position as entity, else None.
        '''
        # remove the line below once you start implementing this function
        index = 0
        while index < len(self.receivers):
            receiver = self.receivers[index]
            if receiver.x == entity.x and receiver.y == entity.y:
                return receiver
            index += 1
        return None

    def get_collided_mirror(self, entity: Emitter | Receiver | Photon | Mirror | None) -> Mirror | None:
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another mirror in the
        circuit.

        If it does, return the mirror already in the entity's position.
        Else, return None, indicating there is no mirror occupying entity's
        position.

        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        A mirror if it has the same position as entity, else None.
        '''
        # remove the line below once you start implementing this function
        if entity is None:
            return None

        index = 0
        while index < len(self.mirrors):
            mirror = self.mirrors[index]
            if mirror.x == entity.x and mirror.y == entity.y:
                return mirror
            index += 1

        return None

    def get_collided_component(self, photon: Photon) -> Emitter | Receiver | Mirror | None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        # will require extensions in ADD-MY-MIRRORS
        '''
        Given a photon, returns the component it has collided with (if any).
        A collision occurs if the positions of photon and the component are
        the same.

        Parameters
        ----------
        photon - a photon to check for collision with the circuit's components

        Returns
        -------
        If the photon collided with a component, return that component.
        Else, return None.

        Hint
        ----
        Use the three collision methods above to handle this.
        '''
        # Check collision with emitters
        collided_emitter = self.get_collided_emitter(photon)
        if collided_emitter:
            return collided_emitter

        # Check collision with receivers
        collided_receiver = self.get_collided_receiver(photon)
        if collided_receiver:
            return collided_receiver

        # Check collision with mirrors (if implemented)

        collided_mirror = self.get_collided_mirror(photon)
        if collided_mirror:
            return collided_mirror

        # If no collisions are found
        return None

    def is_all_pulse_set(self) -> bool:
        '''
        Checks if all emitters in the circuit have their pulse sequences set without using restricted keywords or functions.

        Returns
        -------
        True if all emitters have their pulse sequences set, otherwise False.
        '''
        index = 0
        while index < len(self.emitters):
            if not self.emitters[index].is_pulse_sequence_set():
                return False  # If any emitter does not have its pulse sequence set, return False
            index += 1
        return True

    def tick(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Runs a single nanosecond (tick) of this circuit. If the circuit has
        already finished, this method should return out early.

        Otherwise, for each photon that has not been absorbed, this method is
        responsible for moving it, updating the board to show its new position
        and checking if it collided with a component (and handling it if did
        occur). At the end, we then increment clock.
        '''
        if self.is_finished():
            return

        # Increment the circuit's clock
        self.clock += 1

        index = 0
        while index < len(self.photons):
            photon = self.photons[index]
            if not photon.is_absorbed():
                # Move the photon
                photon.move(self.get_width(), self.get_height())

                # Update the board to show new position of photon
                self.board_displayer.add_photon_to_board(photon)

                # Check for collisions with any component
                collided_component = self.get_collided_component(photon)
                if collided_component:
                    # Handle interaction with the component, providing current clock time as timestamp
                    photon.interact_with_component(
                        collided_component, self.clock)
                    if not photon.is_absorbed():

                        photon.move(self.get_width(), self.get_height())

            index += 1

    def run_circuit(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Runs the entire circuit from start to finish. This involves getting
        each emitter to emit a photon, and continuously running tick until the
        circuit is finished running. All output in regards of running the
        circuit should be contained in this method.
        '''
        print("========================")
        print("   RUNNING CIRCUIT...")
        print("========================\n")

        # Emit photons from each emitter and print/emitter output
        self.emit_photons()
        self.print_emit_photons()  # This should handle the file writing internally

        # Run the simulation until all photons are absorbed
        while not self.is_finished():
            self.tick()
            # Every 5 ticks or on the last tick, display the board and activated receivers
            if self.clock % 5 == 0 or self.is_finished():
                print(
                    f"\n{self.clock}ns: {self.count_activated_receivers()}/{len(self.receivers)} receiver(s) activated.")
            self.board_displayer.print_board()

        # # Ensure the last tick's output is shown only once
        # if self.clock % 5 != 0:
        #     print(f"{self.clock}ns: {self.count_activated_receivers()}/{len(self.receivers)} receiver(s) activated.")
        #     self.board_displayer.print_board()

        # Output activation times and total energy absorbed
        self.print_activation_times()
        self.print_total_energy()

        print("========================")
        print("   CIRCUIT FINISHED!")
        print("========================")

    def count_activated_receivers(self):
        """
        Counts the number of activated receivers.
        """
        count = 0
        index = 0
        while index < len(self.receivers):
            if self.receivers[index].is_activated():
                count += 1
            index += 1
        return count

    def add_emitter(self, emitter: Emitter) -> bool:
        '''
        If emitter is not an Emitter instance, return False. Else, you need to
        perform the following checks in order for any errors:
          1)  The emitter's position is within the bounds of the circuit.
          2)  The emitter's position is not already taken by another emitter in
              the circuit.
          3)  The emitter's symbol is not already taken by another emitter in
              the circuit.

        If at any point a check is not passed, an error message is printed
        stating the causeof the error and returns False, skipping any further
        checks. If all checks pass, then the following needs to occur:
          1)  emitter is added in the circuit's list of emitters. emitter
              needs to be added such that the list of emitters remains sorted
              in alphabetical order by the emitter's symbol. You can assume the
              list of emitters is already sorted before you add the emitter.
          2)  emitter's symbol is added into board_displayer.
          3)  The method returns True.

        Paramaters
        ----------
        emitter - the emitter to add into this circuit's list of emitters

        Returns
        ----------
        Returns true if all checks are passed and the emitter is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.

        Hint
        ----
        Use the get_collided_emitter method to check for position collision.
        You will need to find your own way to check for symbol collisions
        with other emitters.
        '''

        if not isinstance(emitter, Emitter):
            print("Error: Not an emitter instance.")
            return False

        if emitter.x < 0 or emitter.x >= self.width or emitter.y < 0 or emitter.y >= self.height:
            print(
                f"Error: position ({emitter.x}, {emitter.y}) is out-of-bounds of {self.width}x{self.height} circuit board")
            return False

        collided_emitter = self.get_collided_emitter(emitter)
        if collided_emitter:
            print(
                f"Error: position ({emitter.x}, {emitter.y}) is already taken by emitter '{collided_emitter.symbol}'")
            return False

        index = 0
        while index < len(self.emitters):
            if self.emitters[index].symbol == emitter.symbol:
                print(
                    f"Error: Emitter symbol '{emitter.symbol}' is already taken by another emitter.")
                return False
            index += 1

        # Insert emitter into the sorted list of emitters by symbol
        index = 0
        while index < len(self.emitters) and self.emitters[index].symbol < emitter.symbol:
            index += 1
        self.emitters.insert(index, emitter)

        self.board_displayer.add_component_to_board(emitter)

        return True

    def get_emitters(self) -> list[Emitter]:
        '''Returns emitters.'''
        return self.emitters

    def add_receiver(self, receiver: Receiver) -> bool:
        '''
        If receiver is not a Receiver instance, return False. Else, you need to
        perform the following checks in order for any errors:
          1)  The receiver's position is within the bounds of the circuit.
          2)  The receiver's position is not already taken by another emitter
              or receiver in the circuit.
          3)  The receiver's symbol is not already taken by another receiver in
              the circuit.

        If at any point a check is not passed, an error message is printed stating
        the cause of the error and returns False, skipping any further checks. If
        all checks pass, then the following needs to occur:
          1)  receiver is added in the circuit's list of receivers. receiver
              needs to be added such that the list of receivers  remains sorted
              in alphabetical order by the receiver's symbol. You can assume the
              list of receivers is already sorted before you add the receiver.
          2)  receiver's symbol is added into board_displayer.
          3)  The method returns True.

        Paramaters
        ----------
        receiver - the receiver to add into this circuit's list of receivers

        Returns
        ----------
        Returns true if all checks are passed and the receiver is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.

        Hint
        ----
        Use the get_collided_emitter and get_collided_receiver methods to
        check for position collisions.
        You will need to find your own way to check for symbol collisions
        with other receivers.
        '''
        # Check if receiver is a Receiver instance
        if not isinstance(receiver, Receiver):
            print("The object is not a receiver.")
            return False

        # Check if the receiver's position is within the circuit bounds
        if receiver.x < 0 or receiver.x >= self.width or receiver.y < 0 or receiver.y >= self.height:
            print(
                f"Error: position ({receiver.x}, {receiver.y}) is out-of-bounds of {self.width}x{self.height} circuit board")
            return False

        # Check if position is already taken by another emitter or receiver
        collided_emitter = self.get_collided_emitter(receiver)
        if collided_emitter:
            print(
                f"Error: position ({receiver.x}, {receiver.y}) is already taken by emitter '{collided_emitter.symbol}'")
            return False

        collided_receiver = self.get_collided_receiver(receiver)
        if collided_receiver:
            print(
                f"Error: position ({receiver.x}, {receiver.y}) is already taken by receiver '{collided_receiver.symbol}'")
            return False

        # Check if the receiver's symbol is already taken
        index = 0
        while index < len(self.receivers):
            existing_receiver = self.receivers[index]
            if existing_receiver.symbol == receiver.symbol:
                print(f"Error: symbol '{receiver.symbol}' is already taken")
                return False
            index += 1

        # Insert the receiver into the sorted list of receivers
        index = 0
        while index < len(self.receivers) and self.receivers[index].symbol < receiver.symbol:
            index += 1
        self.receivers.insert(index, receiver)

        # Add receiver's symbol to the board displayer
        self.board_displayer.add_component_to_board(receiver)

        return True

    def get_receivers(self) -> list[Receiver]:
        '''Returns receivers.'''
        return self.receivers

    def add_photon(self, photon: Photon) -> bool:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        If the photon passed in is not a Photon instance, it does not add it in
        and returns False. Else, it adds photon in this circuit's list of
        photons and returns True.

        Paramaters
        ----------
        photon - the photon to add into this circuit's list of photons

        Returns
        -------
        Returns True if the photon is added in, else False.
        '''
        if isinstance(photon, Photon):
            self.photons.append(photon)
            return True
        else:
            return False

    def get_photons(self) -> list[Photon]:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''Returns photons.'''
        return self.photons

    def add_mirror(self, mirror: Mirror) -> bool:
        # only requires implementation once you reach ADD-MY-MIRRORS
        '''
        If mirror is not a Mirror instance, return False. Else, you need to
        perform the following checks in order for any errors:
          1)  The mirror's position is within the bounds of the circuit.
          2)  The mirror's position is not already taken by another emitter,
              receiver or mirror in the circuit.

        If at any point a check is not passed, an error message is printed
        stating the cause of theerror and returns False, skipping any further
        checks. If all checks pass, then the following needs to occur:
          1)  mirror is added in the circuit's list of mirrors.
          2) mirror's symbol is added into board_displayer.
          3)   The method returns True.

        Paramaters
        ----------
        mirror - the mirror to add into this circuit's list of mirrors

        Returns
        ----------
        Returns true if all checks are passed and the mirror is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.
        '''
        if not isinstance(mirror, Mirror):
            return False

        # Check 1: Mirror's position is within the bounds of the circuit.
        if mirror.x < 0 or mirror.x >= self.width or mirror.y < 0 or mirror.y >= self.height:
            print(
                f"Error: position ({mirror.x}, {mirror.y}) is out-of-bounds of {self.width}x{self.height} circuit board")
            return False

        index = 0
        # Check for Emitters
        while index < len(self.emitters):
            emitter = self.emitters[index]
            if emitter.x == mirror.x and emitter.y == mirror.y:
                print(
                    f"Error: position ({mirror.x}, {mirror.y}) is already taken by emitter '{emitter.symbol}'")
                return False
            index += 1

        index = 0
        # Check for Receivers
        while index < len(self.receivers):
            receiver = self.receivers[index]
            if receiver.x == mirror.x and receiver.y == mirror.y:
                print(
                    f"Error: position ({mirror.x}, {mirror.y}) is already taken by receiver '{receiver.symbol}'")
                return False
            index += 1

        index = 0
        # Check for Mirrors
        while index < len(self.mirrors):
            existing_mirror = self.mirrors[index]
            if existing_mirror.x == mirror.x and existing_mirror.y == mirror.y:
                print(
                    f"Error: position ({mirror.x}, {mirror.y}) is already taken by mirror '{existing_mirror.symbol}'")
                return False
            index += 1

        # All checks passed, add the mirror to the list and update the board displayer.
        self.mirrors.append(mirror)
        self.board_displayer.add_component_to_board(mirror)
        return True

    def get_mirrors(self) -> list[Mirror]:
        # only requires implementation once you reach ADD-MY-MIRRORS
        '''Returns mirrors.'''
        return self.mirrors

    def get_width(self) -> int:
        '''Returns width.'''
        return self.width

    def get_height(self) -> int:
        '''Returns height.'''
        return self.height

    def test_receivers(self):
        # Add a test receiver
        test_receiver = Receiver('Test', 1, 1)
        self.receivers.append(test_receiver)

        # Test activation and string conversion
        if self.receivers[0].is_activated():
            print("Receiver is activated")
        else:
            print("Receiver is not activated")

        print(str(self.receivers[0]))


# circuit = LaserCircuit(6, 10)
# circuit.print_board()
# e1 = Emitter('C', 3, 7)
# # e2 = Emitter('B', 8, 1)
# # e3 = Emitter('C', 8, 1)


# circuit.add_emitter(e1)
# # circuit.add_emitter(e2)
# # circuit.add_emitter(e3)
# circuit.print_board()
# circuit.emit_photons()
# circuit.print_board()
# circuit.get_photons()
# circuit.is_finished()

# circuit.tick()
# r1 = Receiver('R0', 15, 2)
# r2 = Receiver('R1', 8, 4)
# r3 = Receiver('R1', 9, 0)
# r4 = Receiver('R1', 0, 13)


# circuit.add_receiver(r1)
# circuit.add_receiver(r2)
# circuit.add_receiver(r3)
# circuit.add_receiver(r4)

# print(circuit.get_width())
# circuit.print_board()


# circuit.get_receivers()


# circuit.test_receivers()
# circuit.run_circuit()
