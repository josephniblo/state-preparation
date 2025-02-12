import qutip as qt
import numpy as np


def hwp_matrix(theta) -> qt.Qobj:
    """
    Returns the matrix for a Half-Wave Plate (HWP) with fast axis at angle theta.

    Parameters:
    theta (float): The angle of the fast axis of the HWP in radians.

    Returns:
    numpy.ndarray: The 2x2 matrix representing the HWP operation.
    """
    return qt.Qobj(
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
    return qt.Qobj(
        [
            [
                np.cos(theta) ** 2 - 1j * np.sin(theta) ** 2,
                (1 - 1j) * np.sin(theta) * np.cos(theta),
            ],
            [
                (1 - 1j) * np.sin(theta) * np.cos(theta),
                -1j * np.sin(theta) ** 2 + np.cos(theta) ** 2,
            ],
        ]
    )


# Example usage
if __name__ == "__main__":
    # Define a generic pure state
    state = qt.basis(2, 0)  # |0>

    # Define angles for HWP and QWP
    theta_hwp = np.pi / 4  # 45 degrees
    theta_qwp = np.pi / 4  # 45 degrees

    # Get the matrices
    hwp = hwp_matrix(theta_hwp)
    qwp = qwp_matrix(theta_qwp)

    # Apply the matrices to the state
    state_after_hwp = hwp * state
    state_after_qwp = qwp * state_after_hwp

    print("State after HWP:", state_after_hwp)
    print("State after QWP:", state_after_qwp)

