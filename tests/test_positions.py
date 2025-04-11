import state_preparation.waveplates as wp
import state_preparation.utils as utils
import qutip as qt
import numpy as np


def test_get_hwp_from_target_state():
    h = qt.basis(2, 0)  # |0>
    v = qt.basis(2, 1)  # |1>

    state = (h + 2 * v).unit()  # |H> + |V>

    theta = wp.get_hwp_from_target_state(state)

    hwp = utils.hwp_matrix(theta)
    state_after_hwp = hwp * state

    assert (
        qt.tracedist(state_after_hwp, state) < 1e-10
    ), "The final state is not close to the target state."


def test_get_hwp_from_target_state_invalid_target_state():
    h = qt.basis(2, 0)  # |0>
    v = qt.basis(2, 1)  # |1>

    state = (h + 2j * v).unit()  # |H> + |V>

    # assert that we get a ValueError if the target state is not a real linear combination of H and V
    try:
        theta = wp.get_hwp_from_target_state(state)
    except ValueError:
        pass
    else:
        raise AssertionError("A ValueError should have been raised.")


def test_get_hwp_qwp_from_target_state_h():
    h = qt.basis(2, 0)  # |0>
    v = qt.basis(2, 1)  # |1>

    initial_state = h.unit()  # |H>
    target_state = h.unit()  # |H>

    theta_hwp, theta_qwp = wp.get_hwp_qwp_from_target_state(target_state)

    hwp = utils.hwp_matrix(theta_hwp)
    state_after_hwp = hwp * initial_state

    qwp = utils.qwp_matrix(theta_qwp)
    state_after_qwp = qwp * state_after_hwp

    # check the final state is close to the target state, ignoring global phase
    assert (
        qt.tracedist(state_after_qwp, target_state) < 1e-10
    ), "The final state is not close to the target state."


def test_get_hwp_qwp_from_target_state_v():
    h = qt.basis(2, 0)  # |0>
    v = qt.basis(2, 1)  # |1>

    initial_state = h.unit()  # |H>
    target_state = v.unit()  # |V>

    theta_hwp, theta_qwp = wp.get_hwp_qwp_from_target_state(target_state)

    hwp = utils.hwp_matrix(theta_hwp)
    state_after_hwp = hwp * initial_state

    qwp = utils.qwp_matrix(theta_qwp)
    state_after_qwp = qwp * state_after_hwp

    # check the final state is close to the target state, ignoring global phase
    assert (
        qt.tracedist(state_after_qwp, target_state) < 1e-10
    ), "The final state is not close to the target state."


def test_get_hwp_qwp_from_target_state_h_v():
    h = qt.basis(2, 0)  # |0>
    v = qt.basis(2, 1)  # |1>

    initial_state = h.unit()  # |H>

    target_state = (h + v).unit()  # |H> + |V>

    theta_hwp, theta_qwp = wp.get_hwp_qwp_from_target_state(target_state)

    hwp = utils.hwp_matrix(theta_hwp)
    state_after_hwp = hwp * initial_state

    qwp = utils.qwp_matrix(theta_qwp)
    state_after_qwp = qwp * state_after_hwp

    # check the final state is close to the target state, ignoring global phase
    assert (
        qt.tracedist(state_after_qwp, target_state) < 1e-10
    ), "The final state is not close to the target state."


def test_get_hwp_qwp_from_target_state_h_iv():
    h = qt.basis(2, 0)  # |0>
    v = qt.basis(2, 1)  # |1>

    initial_state = h.unit()  # |H>

    target_state = (h + 1j * v).unit()  # |H> + i|V>

    theta_hwp, theta_qwp = wp.get_hwp_qwp_from_target_state(target_state)

    hwp = utils.hwp_matrix(theta_hwp)
    state_after_hwp = hwp * initial_state

    qwp = utils.qwp_matrix(theta_qwp)
    state_after_qwp = qwp * state_after_hwp

    # check the final state is close to the target state, ignoring global phase
    assert (
        qt.tracedist(state_after_qwp, target_state) < 1e-10
    ), "The final state is not close to the target state."


def test_get_hwp_qwp_from_target_state_ah_bv():
    h = qt.basis(2, 0)  # |0>
    v = qt.basis(2, 1)  # |1>

    initial_state = h.unit()  # |H>

    target_state = (0.6 * h + 0.8j * v).unit()  # 0.6|H> + 0.8i|V>

    theta_hwp, theta_qwp = wp.get_hwp_qwp_from_target_state(target_state)

    hwp = utils.hwp_matrix(theta_hwp)
    state_after_hwp = hwp * initial_state

    qwp = utils.qwp_matrix(theta_qwp)
    state_after_qwp = qwp * state_after_hwp

    # remove global phase
    phase = np.exp(-1j * np.angle(state_after_qwp[0]))
    state_after_qwp = phase * state_after_qwp

    # check the final state is close to the target state, ignoring global phase
    assert (
        qt.tracedist(state_after_qwp, target_state) < 1e-10
    ), "The final state is not close to the target state."


def test_get_hwp_qwp_from_target_state_invalid_target_state():
    rho = qt.fock_dm(2, 0)  # |0><0|

    # assert that we get a ValueError if the target state is not a ket
    try:
        theta = wp.get_hwp_qwp_from_target_state(rho)
    except ValueError:
        pass
    else:
        raise AssertionError("A ValueError should have been raised.")
