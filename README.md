# 📡 Bitwise Error Detection

A simple and educational Python project that demonstrates two core **error detection algorithms** used in digital communications:

- ✅ 2D Parity Check
- 🔄 Cyclic Redundancy Check (CRC)

Perfect for students or anyone learning about bit-level error detection techniques.


---

## ⚙️ Features

### 1️⃣ 2D Parity Check
- Accepts binary input (length must be a multiple of 7)
- Builds a parity matrix with horizontal and vertical parity bits
- Introduces a random error into the matrix
- Detects the position of the error using parity recalculation

### 2️⃣ CRC (Cyclic Redundancy Check)
- Takes a binary message and a generator polynomial
- Calculates the CRC remainder
- Appends it to form the transmitted message
- Simulates checking the received message for errors

---

## 🧠 Concepts Covered

- Bitwise XOR operations
- Matrix manipulation with NumPy
- Error simulation and detection
- Binary polynomial division (CRC logic)

---

## 🛠 Requirements

- Python 3.x
- NumPy

Install dependencies:

```bash
pip install numpy

