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


def get_hwp_qwp_from_target_state(target_state: qt.Qobj) -> tuple[float, float]:
    """
    Calculate the required wave plate position for a Half-Wave Plate (HWP) followed by a Quarter-Wave Plate (QWP).
    Assumes that the input state is a pure state polarised in H = [1, 0] and the output state is a pure state.

    Parameters:
    target_state: Desired final state after applying the wave plates.

    Returns:
    tuple[float, float]: The required position for the half wave plate and the quarter wave plate.
    """
    # check if the target state is pure
    if not target_state.isket:
        raise ValueError("The target state is not a ket.")

    # Rewrite psi in the R, L basis
    target_state_rl_basis = qt.Qobj(
        [
            1 / 2 * (target_state[0] - 1j * target_state[1]),
            1 / 2 * (target_state[0] + 1j * target_state[1]),
        ]
    )

    # remove global phase
    phase_factor = np.exp(-1j * np.angle(target_state_rl_basis[0]))[0]
    target_state_rl_basis = phase_factor * target_state_rl_basis
    target_state_rl_basis = target_state_rl_basis.unit()

    # |psi> = cos(theta / 2) |R> + exp(i*psi) sin(theta / 2) |L>
    psi = 2 * np.arccos(target_state_rl_basis[0])[0]
    chi = np.angle(target_state_rl_basis[1])[0]

    omega = np.pi / 2 - psi
    print(omega)

    theta_hwp = (chi - omega) / 4
    theta_qwp = chi / 2

    print(target_state)
    print(target_state_rl_basis)
    print(theta_hwp, theta_qwp)

    return theta_hwp, theta_qwp
