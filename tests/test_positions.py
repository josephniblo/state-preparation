import state_preparation.waveplates as wp
import state_preparation.utils as utils
import qutip as qt


def test_get_hwp_from_target_state():
    h = qt.basis(2, 0)  # |0>
    v = qt.basis(2, 1)  # |1>

    state = (h + 2 * v).unit()  # |H> + |V>

    theta = wp.get_hwp_from_target_state(state)

    hwp = utils.hwp_matrix(theta)
    state_after_hwp = hwp * state

    assert (
        qt.tracedist(state_after_hwp, state) < 1
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
