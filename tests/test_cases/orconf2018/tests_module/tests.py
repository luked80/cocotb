"""
Example test module showing usage of the MODULE command line switch.
"""

import cocotb

from cocotb.triggers import Timer
from cocotb.result import ReturnValue, TestFailure, TestError, TestSuccess

@cocotb.test()
def passing_test(dut):
    """
    Example showing an implicitly passing test.
    """
    dut._log.info("Implicitly passing test.")
    yield Timer(1)

@cocotb.test()
def passing_test_explicit(dut):
    """
    Example showing how to explicitly pass a test.
    """
    dut._log.info("Explicitly passing test.")
    yield Timer(1)
    raise TestSuccess

@cocotb.test()
def passing_test_explicit_with_message(dut):
    """
    Example showing how to explicitly pass a test.
    """
    dut._log.info("Explicitly passing test with a message.")
    yield Timer(1)
    raise TestSuccess("This test is passing!")

@cocotb.test()
def failing_test(dut):
    """
    Example showing how to fail a test.
    """
    dut._log.info("Failing test example.")
    yield Timer(1)
    raise TestFailure

@cocotb.test()
def failing_test_with_message(dut):
    """
    Example showing how to fail a test with a message.
    """
    dut._log.info("Failing test example with message.")
    yield Timer(1)
    raise TestFailure("This test is failing!")
