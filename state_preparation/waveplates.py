import numpy as np
import qutip as qt


def get_hwp_from_target_state(target_state: qt.Qobj) -> float:
    """
    Calculate the required wave plate position for a Half-Wave Plate (HWP).
    Assumes that the input state is a pure state polarised in H = [1, 0] and the output state is a pure state which is a real linear combination of H and V.

    Parameters:
    target_state: Desired final state after applying the half wave plate.

    Returns:
    float: The required position for the half wave plate.
    """
    # get the angle of the plane through R, L and the target state
    target_state = target_state.unit()

    # check if the target state is a real linear combination of H and V
    if target_state != target_state.conj():
        raise ValueError(
            "The target state is not a real linear combination of H and V."
        )

    # Calculate the angle of the half wave plate
    hwp_position = (np.arctan2(target_state[1].real, target_state[0].real))[0]

    return hwp_position
