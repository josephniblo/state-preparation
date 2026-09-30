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

def get_rl_state(target_state: qt.Qobj):
    """
    Convert a target state in the H, V basis to the R, L basis.

    Parameters:
    target_state: Desired final state after applying the wave plates.

    Returns:
    qt.Qobj: The target state in the R, L basis.
    """
    return qt.Qobj(
        [
            1 / np.sqrt(2) * (target_state[0] - 1j * target_state[1]),
            1 / np.sqrt(2) * (target_state[0] + 1j * target_state[1]),
        ]
    )

def get_omega_chi_from_target_state_rl_basis(target_state_rl_basis: qt.Qobj) -> tuple[float, float]:
    # remove global phase and normalise
    phase_factor = np.exp(-1j * np.angle(target_state_rl_basis[0]))[0]
    target_state_rl_basis = phase_factor * target_state_rl_basis
    target_state_rl_basis = target_state_rl_basis.unit()

    print(f"target_state_rl_basis: {target_state_rl_basis.full()}")

    psi = 2 * np.arccos(target_state_rl_basis[0])[0].real
    chi = np.angle(target_state_rl_basis[1])[0]

    omega = np.pi / 2 - psi

    return omega, chi

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

    target_state_rl_basis = get_rl_state(target_state)

    # if target_state is very close to R or L, omega and chi are not well defined, so we can just return the positions for R or L
    if np.isclose(target_state_rl_basis[0], 0): # R
        return 0, np.pi / 4
    elif np.isclose(target_state_rl_basis[1], 0): # L
        return 0, -np.pi / 4

    omega, chi = get_omega_chi_from_target_state_rl_basis(target_state_rl_basis)

    print(f"omega: {omega}, chi: {chi}")

    theta_hwp = (chi - omega) / 4
    theta_qwp = chi / 2

    return theta_hwp, theta_qwp

def get_qwp_hwp_from_projection_basis(
    projection_basis: qt.Qobj,
) -> tuple[float, float]:
    """
    Calculate QWP and HWP positions for projection onto projection_basis.

    The optical sequence is QWP -> HWP -> PBS, with H transmitted.
    """

    if not projection_basis.isket:
        raise ValueError("The projection basis must be a ket.")

    projection_basis_rl = get_rl_state(projection_basis.unit())

    # R projection: R -> H requires QWP(-45°)
    if np.isclose(abs(projection_basis_rl[1]), 0):
        return -np.pi / 4, 0.0

    # L projection: L -> H requires QWP(+45°)
    if np.isclose(abs(projection_basis_rl[0]), 0):
        return +np.pi / 4, 0.0

    omega, chi = get_omega_chi_from_target_state_rl_basis(
        projection_basis_rl
    )

    theta_qwp = chi / 2 + np.pi / 2
    theta_hwp = (chi - omega) / 4

    return theta_qwp, theta_hwp



def hwp_matrix(theta) -> qt.Qobj:
    """
    Returns the matrix for a Half-Wave Plate (HWP) with fast axis at angle theta.

    Parameters:
    theta (float): The angle of the fast axis of the HWP in radians.

    Returns:
    numpy.ndarray: The 2x2 matrix representing the HWP operation.
    """
    return 1j * qt.Qobj(
        (
            [np.cos(2 * theta), np.sin(2 * theta)],
            [np.sin(2 * theta), -np.cos(2 * theta)],
        )
    )


def qwp_matrix(theta) -> qt.Qobj:
    """
    Returns the matrix for a Quarter-Wave Plate (QWP) with fast axis at angle theta.

    Parameters:
    theta (float): The angle of the fast axis of the QWP in radians.

    Returns:
    numpy.ndarray: The 2x2 matrix representing the QWP operation.
    """
    return (1 / np.sqrt(2)) * qt.Qobj(
        [
            [
                1 + 1j * np.cos(2 * theta),
                1j * np.sin(2 * theta),
            ],
            [
                1j * np.sin(2 * theta),
                1 - 1j * np.cos(2 * theta),
            ],
        ]
    )





if __name__ == "__main__":
    h_state = qt.basis(2, 0)  # H state

    # Example usage
    print("Testing H")
    target_state = qt.basis(2, 0)  # H state
    hwp_position, qwp_position = get_hwp_qwp_from_target_state(target_state)
    print(f"HWP position for target state {target_state}: HWP position {hwp_position}, QWP position: {qwp_position}")

    M_H = hwp_matrix(hwp_position) 
    M_Q = qwp_matrix(qwp_position)

    print(f"M_H: {M_H.full()}")
    print(f"M_Q: {M_Q.full()}")

    state_after_hwp_qwp = M_Q * M_H * h_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")


    print("\n Testing V")
    target_state = qt.basis(2, 1)  # V state
    hwp_position, qwp_position = get_hwp_qwp_from_target_state(target_state)
    print(f"HWP position for target state {target_state}: HWP position {hwp_position}, QWP position: {qwp_position}")

    state_after_hwp_qwp = M_Q * M_H * h_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")


    print("\n Testing D")
    target_state = (qt.basis(2, 0) + qt.basis(2, 1)).unit()  # Diagonal state
    hwp_position, qwp_position = get_hwp_qwp_from_target_state(target_state)
    print(f"HWP position for target state {target_state}: HWP position {hwp_position}, QWP position: {qwp_position}")

    M_H = hwp_matrix(hwp_position)
    M_Q = qwp_matrix(qwp_position)
    state_after_hwp_qwp = M_Q * M_H * h_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")


    print("\n Testing A")
    target_state = (qt.basis(2, 0) - qt.basis(2, 1)).unit()  # Anti-diagonal state
    hwp_position, qwp_position = get_hwp_qwp_from_target_state(target_state)
    print(f"HWP position for target state {target_state}: HWP position {hwp_position}, QWP position: {qwp_position}")

    M_H = hwp_matrix(hwp_position)
    M_Q = qwp_matrix(qwp_position)
    state_after_hwp_qwp = M_Q * M_H * h_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")


    print("\n Testing R")
    target_state = (qt.basis(2, 0) + 1j * qt.basis(2, 1)).unit()  # Right circular state
    hwp_position, qwp_position = get_hwp_qwp_from_target_state(target_state)
    print(f"HWP position for target state {target_state}: HWP position {hwp_position}, QWP position: {qwp_position}")

    M_H = hwp_matrix(hwp_position)
    M_Q = qwp_matrix(qwp_position)
    state_after_hwp_qwp = M_Q * M_H * h_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")


    print("\n Testing L")
    target_state = (qt.basis(2, 0) - 1j * qt.basis(2, 1)).unit()  # Left circular state
    hwp_position, qwp_position = get_hwp_qwp_from_target_state(target_state)
    print(f"HWP position for target state {target_state}: HWP position {hwp_position}, QWP position: {qwp_position}")

    M_H = hwp_matrix(hwp_position)
    M_Q = qwp_matrix(qwp_position)
    state_after_hwp_qwp = M_Q * M_H * h_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")


    # prepare R then project into R
    target_state = (qt.basis(2, 0) + 1j * qt.basis(2, 1)).unit()  # Right circular state
    qwp_position, hwp_position = get_qwp_hwp_from_projection_basis(target_state)
    M_H = hwp_matrix(hwp_position)
    M_Q = qwp_matrix(qwp_position)
    state_after_hwp_qwp = M_H * M_Q * target_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")

    # prepare L then project into L
    target_state = (qt.basis(2, 0) - 1j * qt.basis(2, 1)).unit()  # Left circular state
    qwp_position, hwp_position = get_qwp_hwp_from_projection_basis(target_state)
    M_H = hwp_matrix(hwp_position)
    M_Q = qwp_matrix(qwp_position)
    state_after_hwp_qwp = M_H * M_Q * target_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")

    # prepare D then project into D
    target_state = (qt.basis(2, 0) + qt.basis(2, 1)).unit()  # Diagonal state
    qwp_position, hwp_position = get_qwp_hwp_from_projection_basis(target_state)
    M_H = hwp_matrix(hwp_position)
    M_Q = qwp_matrix(qwp_position)
    state_after_hwp_qwp = M_H * M_Q * target_state
    print(f"State after HWP and QWP: {state_after_hwp_qwp.full()}")