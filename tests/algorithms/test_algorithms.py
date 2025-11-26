import numpy as np

from geqo.algorithms.algorithms import (
    PCCM,
    QFT,
    InversePCCM,
    InverseQFT,
    PermuteQubits,
    QubitReversal,
    decompose_mcp,
    decompose_mcu,
    stateInitialize,
    unitaryDecomposer,
)
from geqo.core.basic import BasicGate
from geqo.core.quantum_circuit import Sequence
from geqo.gates.fundamental_gates import (
    Hadamard,
    InversePhase,
    PauliY,
    Phase,
    SwapQubits,
)
from geqo.gates.multi_qubit_gates import Toffoli
from geqo.gates.rotation_gates import InverseRx, InverseRy, Rx, Ry, Rzz
from geqo.operations.controls import QuantumControl
from geqo.simulators.cupy import unitarySimulatorCuPy
from geqo.simulators.numpy import simulatorStatevectorNumpy


class TestAlgorithms:
    def test_permute_qubits(self):
        order = [2, 3, 0, 1]
        op = PermuteQubits(order)
        clone_op = PermuteQubits(order)
        diff_op = Hadamard()
        inv_order = [order.index(x) for x in range(len(order))]
        seq = Sequence([*range(len(order))], [], [(op, [*range(len(order))], [])])

        assert op.targetOrder == order
        assert str(op) == "PermuteQubits(" + str(order) + ")"
        assert op == clone_op
        assert op != diff_op
        assert op.getInverse() == PermuteQubits(inv_order)
        assert op.getEquivalentSequence() == seq
        assert op.getNumberQubits() == len(order)
        assert op.getNumberClassicalBits() == 0
        assert op.isUnitary()
        assert not op.hasDecomposition()

    def test_qubit_reversal(self):
        num_qubits = 5
        op = QubitReversal(num_qubits)
        clone_op = QubitReversal(num_qubits)
        diff_op = Hadamard()
        op_and_targets = [
            (SwapQubits(), [i, num_qubits - i - 1], []) for i in range(num_qubits // 2)
        ]
        seq = Sequence([*range(num_qubits)], [], op_and_targets)

        assert op.numberQubits == num_qubits
        assert str(op) == "QubitReversal(" + str(num_qubits) + ")"
        assert op == clone_op
        assert op != diff_op
        assert op.getInverse() == op
        assert op.getEquivalentSequence() == seq
        assert op.getNumberQubits() == num_qubits
        assert op.getNumberClassicalBits() == 0
        assert op.isUnitary()
        assert op.hasDecomposition()

    def test_QFT(self):
        num_qubits = 5
        prefix = "pre"
        op = QFT(num_qubits, prefix)
        clone_op = QFT(num_qubits, prefix)
        diff_op = Hadamard()
        op_and_targets = []
        for i in range(num_qubits):
            op_and_targets.append((Hadamard(), [i], []))
            for j in range(1, num_qubits - i):
                op_and_targets.append(
                    (
                        QuantumControl([1], Phase(prefix + "Ph" + str(j))),
                        [i + j, i],
                        [],
                    )
                )
        op_and_targets.append((QubitReversal(num_qubits), list(range(num_qubits)), []))
        seq = Sequence(list(range(num_qubits)), [], op_and_targets)

        assert op.numberQubits == num_qubits
        assert op.nameSpacePrefix == prefix
        assert str(op) == "QFT(" + str(num_qubits) + ', "' + prefix + '")'
        assert op == clone_op
        assert op != diff_op
        assert op.getInverse() == InverseQFT(num_qubits, prefix)
        assert op.getEquivalentSequence() == seq
        assert op.getNumberQubits() == num_qubits
        assert op.getNumberClassicalBits() == 0
        assert op.isUnitary()
        assert op.hasDecomposition()

    def test_inverse_QFT(self):
        num_qubits = 5
        prefix = "pre"
        op = InverseQFT(num_qubits, prefix)
        clone_op = InverseQFT(num_qubits, prefix)
        diff_op = Hadamard()
        op_and_targets = []
        op_and_targets.append((QubitReversal(num_qubits), list(range(num_qubits)), []))
        for i in reversed(range(num_qubits)):
            for j in reversed(range(1, num_qubits - i)):
                op_and_targets.append(
                    (
                        QuantumControl([1], InversePhase(prefix + "Ph" + str(j))),
                        [i + j, i],
                        [],
                    )
                )
            op_and_targets.append((Hadamard(), [i], []))

        seq = Sequence(list(range(num_qubits)), [], op_and_targets)

        assert op.qft == QFT(num_qubits, prefix)
        assert op.nameSpacePrefix == prefix
        assert str(op) == "InverseQFT(" + str(num_qubits) + ', "' + prefix + '")'
        assert op == clone_op
        assert op != diff_op
        assert op.getInverse() == QFT(num_qubits, prefix)
        assert op.getEquivalentSequence() == seq
        assert op.getNumberQubits() == num_qubits
        assert op.getNumberClassicalBits() == 0
        assert op.isUnitary()
        assert op.hasDecomposition()

    def test_PCCM(self):
        name = "a"
        prefix = "pre"
        op = PCCM(name, prefix)
        clone_op = PCCM(name, prefix)
        diff_op = Hadamard()
        gate1 = Rx(prefix + "RX(π/2)")
        gate2 = Rx(prefix + "RX(π/2)")
        gate3 = QuantumControl([1], Rx(prefix + "RX(" + name + ")"))
        gate4 = QuantumControl([1], Rx(prefix + "RX(-π/2)"))
        gate5 = Rx(prefix + "RX(-π/2)")
        gate6 = Ry(prefix + "RY(-π/2)")
        op_and_targets = [
            (gate1, [0], []),
            (gate2, [1], []),
            (gate3, [0, 1], []),
            (gate4, [1, 0], []),
            (gate5, [0], []),
            (gate6, [1], []),
        ]
        seq = Sequence([0, 1], [], op_and_targets)

        assert op.name == name
        assert op.nameSpacePrefix == prefix
        assert str(op) == 'PCCM("' + name + '", "' + prefix + '")'
        assert op == clone_op
        assert op != diff_op
        assert op.getInverse() == InversePCCM(name, prefix)
        assert op.getEquivalentSequence() == seq
        assert op.getNumberQubits() == 2
        assert op.getNumberClassicalBits() == 0
        assert op.isUnitary()
        assert op.hasDecomposition()

    def test_inverse_PCCM(self):
        name = "a"
        prefix = "pre"
        op = InversePCCM(name, prefix)
        clone_op = InversePCCM(name, prefix)
        diff_op = Hadamard()
        gate1 = InverseRx(prefix + "RX(π/2)")
        gate2 = InverseRx(prefix + "RX(π/2)")
        gate3 = QuantumControl([1], InverseRx(prefix + "RX(" + name + ")"))
        gate4 = QuantumControl([1], InverseRx(prefix + "RX(-π/2)"))
        gate5 = InverseRx(prefix + "RX(-π/2)")
        gate6 = InverseRy(prefix + "RY(-π/2)")
        op_and_targets = [
            (gate6, [1], []),
            (gate5, [0], []),
            (gate4, [1, 0], []),
            (gate3, [0, 1], []),
            (gate2, [1], []),
            (gate1, [0], []),
        ]
        seq = Sequence([0, 1], [], op_and_targets)

        assert op.pccm == PCCM(name, prefix)
        assert op.nameSpacePrefix == prefix
        assert str(op) == 'InversePCCM("' + name + '", "' + prefix + '")'
        assert op == clone_op
        assert op != diff_op
        assert op.getInverse() == PCCM(name, prefix)
        assert op.getEquivalentSequence() == seq
        assert op.getNumberQubits() == 2
        assert op.getNumberClassicalBits() == 0
        assert op.isUnitary()
        assert op.hasDecomposition()

    def test_state_initialize(self):
        state = np.array([1, 2 + 0.5j, 3 - 1.2j, 4])
        state = state / np.sqrt(np.sum(state * np.conj(state)))
        seq, params = stateInitialize(state)

        sim = simulatorStatevectorNumpy(2, 0)
        sim.values = params
        sim.apply(seq, [0, 1])
        result = sim.state

        assert np.allclose(state, result.flatten(), rtol=1e-05, atol=1e-06)

    def test_unitary_decomposer(self):
        random = Sequence(
            [0, 1, 2],
            [],
            [
                (PauliY(), [1], []),
                (Rzz("a"), [0, 2], []),
                (Toffoli(), [2, 1, 0], []),
                (SwapQubits(), [0, 2], []),
                (Rx("b"), [1], []),
            ],
        )

        sim = unitarySimulatorCuPy(3)
        sim.setValue("a", 1.23)
        sim.setValue("b", 4.56)
        sim.prepareBackend([Toffoli()])
        sim.apply(random, [0, 1, 2])
        u2 = sim.u

        # decompose the Givens operators into Ry and Rz gates
        seq_u2, u2_params = unitaryDecomposer(u2, decompose_givens=True)

        # verify if the decomposed sequence is equivalent to the u2 gate
        sim = unitarySimulatorCuPy(3)
        sim.values = u2_params
        sim.setValue("u2", u2)
        sim.apply(BasicGate("u2", 3), [0, 1, 2])
        sim.apply(seq_u2.getInverse(), [0, 1, 2])
        test_u2 = sim.u
        assert np.allclose(
            np.array(test_u2).astype(np.complex128),
            np.identity(8).astype(np.complex128),
            rtol=1e-05,
            atol=1e-06,
        )

    def test_decompose_unitary_into_single_rotation_phase(self):
        random = Sequence(
            [0, 1, 2, 3],
            [],
            [
                (PauliY(), [3], []),
                (Rzz("a"), [0, 2], []),
                (Toffoli(), [2, 1, 0], []),
                (SwapQubits(), [0, 3], []),
                (Rx("b"), [1], []),
            ],
        )

        sim = unitarySimulatorCuPy(4)
        sim.setValue("a", 1.23)
        sim.setValue("b", 4.56)
        sim.prepareBackend([Toffoli()])
        sim.apply(random, [0, 1, 2, 3])
        u2 = sim.u
        seq_u2, u2_params = unitaryDecomposer(u2)

        op = []
        de_params = {}
        for gnt in seq_u2.gatesAndTargets:
            gate = gnt[0]
            qtargets = gnt[1]
            if isinstance(gate, QuantumControl) and isinstance(gate.qop, BasicGate):
                u = u2_params[gate.qop.name]
                givens_seq, givens_params = decompose_mcu(
                    u, gate.onoff, qtargets, seq_u2.getNumberQubits()
                )
                for g in givens_seq.gatesAndTargets:
                    op.append(g)
                de_params.update(givens_params)
            elif isinstance(gate, QuantumControl) and isinstance(gate.qop, Phase):
                theta = u2_params[gate.qop.name]
                phase_seq, phase_params = decompose_mcp(
                    theta, gate.onoff, qtargets, seq_u2.getNumberQubits()
                )
                for g in phase_seq.gatesAndTargets:
                    op.append(g)
                de_params.update(phase_params)
            else:
                op.append(gnt)

        de_seq = Sequence(seq_u2.qubits, seq_u2.bits, op)
        sim = unitarySimulatorCuPy(4)
        sim.values = de_params
        sim.apply(de_seq, [*range(4)])
        output = sim.u

        assert np.allclose(
            output,
            u2,
            rtol=1e-05,
            atol=1e-06,
        )
