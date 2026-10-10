import time
import logging

# Configure enterprise-grade logging for transaction monitoring
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class MEVSecurityGuard:
    """
    Institutional MEV-Resistant Transaction Guard.
    Protects decentralized exchange trades and automated bots from front-running,
    sandwich attacks, and sudden gas price spikes.
    """
    def __init__(self, max_allowed_slippage_pct: float, max_gas_gwei: float):
        self.max_allowed_slippage_pct = max_allowed_slippage_pct
        self.max_gas_gwei = max_gas_gwei

    def inspect_transaction(self, estimated_slippage: float, current_gas_gwei: float) -> dict:
        threats = []
        
        # Check for sandwich or front-running slippage manipulation
        if estimated_slippage > self.max_allowed_slippage_pct:
            threats.append("HIGH_SLIPPAGE_SANDWICH_RISK")
            
        # Check for malicious mempool gas surges
        if current_gas_gwei > self.max_gas_gwei:
            threats.append("GAS_PRICE_SURGE_DETECTED")

        if threats:
            logging.warning(f"Transaction BLOCKED by MEV Guard. Threats: {threats}")
            return {"status": "REJECTED", "threats": threats}
        
        logging.info("Transaction secure. Approved for broadcast.")
        return {"status": "APPROVED", "threats": []}

# --- Execution & Verification ---
if __name__ == "__main__":
    guard = MEVSecurityGuard(max_allowed_slippage_pct=0.5, max_gas_gwei=120.0)
    
    print("--- Running Live Security Diagnostic ---")
    
    # Simulating a safe trade
    print("\n[Test 1] Standard Market Conditions:")
    guard.inspect_transaction(estimated_slippage=0.2, current_gas_gwei=95.0)
    
    # Simulating a malicious attack vector
    print("\n[Test 2] Malicious Front-Running / Gas Spike Vector:")
    guard.inspect_transaction(estimated_slippage=1.2, current_gas_gwei=145.0)
