from laser_circuit import LaserCircuit
from circuit_for_testing import get_my_lasercircuit
from run import set_pulse_sequence

'''
Name:   Mingyu Du
SID:    540227714
Unikey: midu0228

This test program checks if the set_pulse_sequence function is implemented
correctly.

You can modify this scaffold as needed (changing function names, parameters, 
or implementations...), however, DO NOT ALTER the code in circuit_for_testing 
file, which provides the circuit. The circuit can be retrieved by calling 
get_my_lasercircuit(), and it should be used as an argument for the 
set_pulse_sequence function when testing.

Make sure to create at least six functions for testing: two for positive cases,
two for negative cases, and two for edge cases. Each function should take
different input files.

NOTE: Whenever we use ... in the code, this is a placeholder for you to
replace it with relevant code.
'''


def test_pulse_sequence(file_path: str):
    my_circuit = get_my_lasercircuit()
    with open(file_path, 'r') as file_obj:
        set_pulse_sequence(my_circuit, file_obj)


if __name__ == '__main__':
    test_files = [
        '/home/input/positive_1.in',
        '/home/input/positive_2.in',
        '/home/input/negative_1.in',
        '/home/input/negative_2.in',
        '/home/input/edge_1.in',
        '/home/input/edge_2.in'
    ]

    index = 0
    while index < len(test_files):
        test_pulse_sequence(test_files[index])
        print(f"Test with {
              test_files[index]} completed. Check output or logs for details.")
        index += 1
