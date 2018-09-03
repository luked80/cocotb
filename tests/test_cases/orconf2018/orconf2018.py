
"""
Accompanying tutorial for the Orconf 2018 presentation "An(other) Introduction to Cocotb"
"""

import cocotb
from cocotb.triggers import (Timer, Join, RisingEdge, FallingEdge, Edge,
                             ReadOnly, ReadWrite, NextTimeStep)
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.result import ReturnValue, TestFailure, TestError, TestSuccess

@cocotb.test()
def my_first_test(dut):
    """
    My first test that toggles a clock input.
    """
    dut._log.info("Running my first test!")
    for cycle in range(10):
        dut.clk <= 1
        yield Timer(1)
        dut.clk <= 0
        yield Timer(1)
    dut._log.info("Finished running my first test!")

@cocotb.test()
def accessing_the_design(dut):
    """
    Example of how to access to design from cocotb.
    """

    # Get a reference to the "clk" signal on the top-level
    clk = dut.clk

    # Get a reference to a register "count" in a sub module "sub_module_inst"
    count = dut.sub_module_inst.count

    # Get a reference to the "sub_module_inst" module instance
    inst = dut.sub_module_inst
    
    dut._log.info("dut type is %s" % type(dut))

    yield Timer(1)

@cocotb.test()
def reading_values(dut):
    """
    Example of how to read values from signals in the simulator.
    """
    # Set some value so we have something to read back
    dut.stream_in_data = 42
    yield Timer(1)

    # Read a value back from the dut
    data_in = dut.stream_in_data.value

    # Print out it's binary representation
    dut._log.info(data_in.binstr)

    # Print out it's integer representation
    dut._log.info("%i" % data_in.integer)
    dut._log.info("%i" % int(data_in))

    # Can also cast signal reference directly as a int
    data_in_int = int(dut.stream_in_data)
    dut._log.info("%i" % data_in_int)

@cocotb.test()
def reading_xz_values(dut):
    """
    Example of how to read values from signals in the simulator.
    Expecting this test to error as we try to cast a z value to int.
    """
    # Set some value so we have something to read back
    dut.stream_in_data = BinaryValue('001xx01x')
    yield Timer(1)

    # Read a value back from the dut
    try:
        data_in = dut.stream_in_data.value
    except ValueError:
        dut._log.info("casting x's to int raises ValueError")        

    # Print out it's binary representation
    dut._log.info(data_in.binstr)

    # Print out it's integer representation
    try:
        dut._log.info("%i" % int(data_in))
    except ValueError:
        dut._log.info("casting x's to int raises ValueError")        

    yield Timer(1)

    # Attempt to the same with z values
    dut.stream_in_data = BinaryValue('1z10zz01')
    dut._log.info(data_in.binstr)
    try:
        dut._log.info("%s" % int(dut.stream_in_data))
    except ValueError:
        dut._log.info("casting z's to int raises ValueError")        


@cocotb.test()
def assigning_values(dut):
    """
    Example of how to assign values to the design from cocotb.
    """
    # Get a reference to the clk signal and assign a value
    clk = dut.clk
    clk <= 1
    clk.value = 1

    # Direct assignment through the hierarchy
    dut.stream_in_data <= 12

    # Assign a value to a memory deep in the hierarchy
    dut.sub_module_inst.memory.array[4] <= 2

    yield Timer(1)

@cocotb.test()
def assigning_hex_values(dut):
    """
    Example of how to assign values using hex numbers from cocotb.
    """
    # Assigning hex values
    dut.stream_in_data <= 0xc
    yield Timer(1)
    dut.stream_in_data <= 0xa

    yield Timer(1)

@cocotb.test()
def assigning_xz_values(dut):
    """
    Example of how to assign x/z values to the design from cocotb.
    """
    # Assigning x/z values
    dut.stream_in_data <= BinaryValue('001xz01x')
    yield Timer(1)
    dut.stream_in_data <= BinaryValue('zzzzxxxx')

    yield Timer(1)


@cocotb.test()
def yielding_to_the_simulator(dut):
    """
    The yield keyword is used to pass control of execution
    back to the simulator.
    """
    dut._log.info("About to wait 10ns")
    yield Timer(10,units="ns")
    dut._log.info("Simulation time has advanced 10ns")

@cocotb.test()
def simulator_triggers(dut):
    """
    Show the four different trigger types for interacting
    with the simulator.
    """
    cocotb.fork(Clock(dut.clk,2).start())
    dut._log.info("Waiting for a rising edge on dut.clk")
    yield RisingEdge(dut.clk)
    dut._log.info("Waiting for a falling edge on dut.clk")
    yield FallingEdge(dut.clk)
    dut._log.info("Waiting for any edge on dut.clk")
    yield Edge(dut.clk)
    dut._log.info("Waiting for any edge on dut.clk")
    yield Edge(dut.clk)

"""
Quick example of decorators in python:
@trace
def square(x):
    return x*x

def square(x):
    return x*x
square = trace(square)
"""

@cocotb.coroutine
def wait_10ns():
    """
    Simple coroutine to wait 10ns
    """
    yield Timer(10,units="ns")

@cocotb.coroutine
def wait_100ns():
    """
    Example of a coroutine calling a coroutine
    """
    for x in range(10):
        yield wait_10ns()

@cocotb.coroutine
def wait_10ns_with_retval():
    """
    Simple coroutine to wait 10ns and return a value.
    """
    yield Timer(10,units="ns")
    raise ReturnValue("Hello")

@cocotb.test()
def yielding_to_coroutines(dut):
    """
    Showing how to pass control of execution within cocotb
    by creating and yield'ing to coroutines.
    """
    dut._log.info("About to wait for 10ns.")
    yield wait_10ns()
    dut._log.info("About to wait for 100ns.")
    yield wait_100ns()
    dut._log.info("About to wait for another 100ns.")
    yield wait_100ns()

    return_value = yield wait_10ns_with_retval()
    dut._log.info("Coroutine returned %s" % return_value)

@cocotb.test()
def forking_and_joining(dut):
    """
    Show how to fork and join coroutines within cocotb.
    """
    dut._log.info("Forking a coroutine.")
    cocotb.fork(wait_100ns())

    dut._log.info("Forking a coroutine.")
    forked_wait = cocotb.fork(wait_10ns())
    dut._log.info("Waiting for the forked coroutine to finish.")
    yield forked_wait.join()

    dut._log.info("Forking another coroutine.")
    forked_wait = cocotb.fork(wait_10ns())
    dut._log.info("Waiting for the forked coroutine to finish with alternate syntax.")
    yield Join(forked_wait)


@cocotb.test()
def advanced_yielding(dut):
    """
    Showing what can be done with cocotb's
    yield/fork/join capabilities.
    """
    dut._log.info("Creating a reference to a Timer Trigger.")
    timer_handle = Timer(13)
    dut._log.info("yield on the Timer.")
    yield timer_handle
    dut._log.info("yield on the Timer again.")
    yield timer_handle

    dut._log.info("We can yield on a list of Triggers.")
    yield_result = yield [Timer(1),Timer(2),Timer(3)]
    dut._log.info("Trigger list has yield'ed to %s" % yield_result)

    forked_coro = cocotb.fork(wait_100ns())
    timeout_timer = Timer(99,"ns")
    dut._log.info("Wait for either the forked coroutine or timeout Timer to finish.")
    yield_result = yield [forked_coro.join(),timeout_timer]
    if yield_result == timeout_timer:
        dut._log.info("As expected the 99ns timeout timer fired first.")
    else:
        dut._log.info("Unexpectedly the 100ns coroutine fired first.")


@cocotb.test()
def exploring_design_hierarchy(dut):
    """
    Example showing how to explore the design hierarchy.
    """
    for design_element in dut:
        dut._log.info("Found %s : python type = %s: " % (design_element,type(design_element)))
        dut._log.info("         : _name = %s " % design_element._name)
        dut._log.info("         : _path = %s " % design_element._path)
        if design_element._name == "clk":
            dut._log.warning("Found the clk - twiddling it")
            design_handle = design_element._handle
            design_handle <= 0
            yield Timer(1)
            design_handle <= 1
            yield Timer(1)
            design_handle <= 0

    yield Timer(1)
