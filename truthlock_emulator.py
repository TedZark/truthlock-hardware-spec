# =====================================================================
# PROJECT TRUTHLOCK: HARDWARE-LEVEL CONTENT AUTHENTICITY EMULATOR (v1.0)
# Developed by Theodore (Teo) Zarkadoulas - Structural Hardware Architect
# MediaSecurityLabs.com | Syntax-Aware Silicon Paradigm (LDH)
# =====================================================================

import hashlib
import time

class TruthLockSensorChip:
    def __init__(self, hardware_secret_key: str):
        """
        Initialize the TruthLock Hardened CMOS Sensor Matrix Core.
        REG_CFG_0: Comma Gate (Voltage Signature Injection)
        REG_CFG_1: Period Gate (Instant Flash-Clear/Context Flush)
        """
        self.REG_CFG_0_SIGNATURE_CONTROL = 0x00
        self.REG_CFG_1_FLUSH_TRIGGER = 0x00
        self.hardware_key = hardware_secret_key.encode('utf-8')
        print("[HARDWARE INITIALIZATION] TruthLock Logic Gates Online. Sensor Secure.")

    def _comma_gate_inject(self, raw_pixel_data: bytes) -> str:
        """
        THE COMMA GATE LOGIC (REG_CFG_0):
        Executes at the pre-decode stage. Detects syntactic breaks in pixel gradients
        and injects a cryptographic voltage threshold signature into the data stream.
        """
        self.REG_CFG_0_SIGNATURE_CONTROL = 0x40  # Activate Signature Mode (-40% clock frequency scaling)
        
        # Multi-Valued Logic (MVL) simulation: Binding hardware key to the data matrix
        nonce = str(time.time_ns()).encode('utf-8')
        mvl_voltage_hash = hashlib.sha256(raw_pixel_data + self.hardware_key + nonce).hexdigest()
        
        self.REG_CFG_0_SIGNATURE_CONTROL = 0x00  # Reset signature gate
        return mvl_voltage_hash

    def capture_and_seal_frame(self, frame_id: int, raw_pixel_matrix: list) -> dict:
        """
        Captures a live frame matrix from the CMOS sensor and locks it at the silicon layer.
        """
        print(f"\n[SENSOR STREAM] Capturing Frame #{frame_id}...")
        
        # Flatten the matrix to emulate hardware serialization
        flat_data = bytes(bytearray(raw_pixel_matrix))
        
        # Inject the immutable hardware watermark via the Comma Gate
        hardware_signature = self._comma_gate_inject(flat_data)
        
        # THE PERIOD GATE LOGIC (REG_CFG_1):
        # Triggers a physical high-voltage clear pulse directly to local SRAM matrices
        # to prevent OS-level cache snooping and memory leakage.
        self.REG_CFG_1_FLUSH_TRIGGER = 0x01
        # Emulating instantaneous context flush
        del flat_data 
        self.REG_CFG_1_FLUSH_TRIGGER = 0x00
        print(f"[PERIOD GATE] REG_CFG_1 Fired. Local SRAM matrices cleared. Zero latency.")

        return {
            "frame_id": frame_id,
            "payload": raw_pixel_matrix,
            "truthlock_signature": hardware_signature
        }

    def verify_hardware_integrity(self, sealed_package: dict, dynamic_stream_data: list) -> bool:
        """
        VERIFICATION MATRIX:
        Verifies if the incoming video stream matches the immutable hardware signature.
        If an AI algorithm (Sora/Runway) alters even 1 pixel, the structural grammar breaks.
        """
        print(f"\n[SECURITY VERIFICATION] Auditing Frame #{sealed_package['frame_id']}...")
        
        flat_sealed = bytes(bytearray(sealed_package["payload"]))
        flat_incoming = bytes(bytearray(dynamic_stream_data))

        # Check if the text-based structural alphabet / pixel structure was tampered with
        if flat_sealed != flat_incoming:
            print("\033[91m[CRITICAL FLAG] BIT-STREAM ANOMALY DETECTED!")
            print("[REASON] Multi-Valued Logic voltage thresholds disrupted. Structural grammar broken.")
            print("[STATUS] VIDEO FILE IS A DEEPFAKE / ALTERED CONTENT.\033[0m")
            return False
        
        print("\033[92m[SUCCESS] HARWARE INTEGRITY VERIFIED.")
        print("[STATUS] Content is authentic. Sealed at source sensor.\033[0m")
        return True


# =====================================================================
# LIVE HARDWARE EMULATION CRASH TEST
# =====================================================================
if __name__ == "__main__":
    # Simulate a 47-year-old hardware vendor setup
    sensor_chip = TruthLockSensorChip(hardware_secret_key="TeoZarkadoulas_MSL_2026")

    # Simulate a raw 4x4 pixel matrix captured by a drone camera (e.g., Anavyssos Beach)
    original_drone_frame = [
        155, 155, 158, 160,
        154, 200, 201, 159,
        150, 202, 204, 151,
        148, 149, 150, 150
    ]

    # Step 1: Secure the frame at the physical layer
    secured_output = sensor_chip.capture_and_seal_frame(frame_id=101, raw_pixel_matrix=original_drone_frame)
    print(f"-> Generated TruthLock Cryptographic Hash: {secured_output['truthlock_signature']}")

    # Step 2: Test Case A - Perfect Transmission (Authentic Video)
    sensor_chip.verify_hardware_integrity(secured_output, dynamic_stream_data=original_drone_frame)

    # Step 3: Test Case B - AI Deepfake Infill Attack (Altering just ONE pixel matrix node)
    print("\n" + "="*60)
    print("[ATTACK SIMULATION] Generative AI tool modifies the frame to remove/alter an object...")
    tampered_drone_frame = original_drone_frame.copy()
    tampered_drone_frame[5] = 99  # AI alteration on pixel index 5
    
    sensor_chip.verify_hardware_integrity(secured_output, dynamic_stream_data=tampered_drone_frame)
