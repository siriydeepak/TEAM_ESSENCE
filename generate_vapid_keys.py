#!/usr/bin/env python3
"""
AetherShelf Sentinel — VAPID Key Generator
===========================================
Run this ONCE to generate your Web Push VAPID keys.
Keys are saved to .env and printed for manifest use.

Usage:
    python generate_vapid_keys.py
"""

import base64
import os
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("Installing cryptography...")
    os.system("pip install cryptography")
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization


def generate_vapid_keys():
    """Generate VAPID EC P-256 key pair for Web Push."""
    print("\n🔐 AetherShelf Sentinel — VAPID Key Generator")
    print("=" * 50)

    # Generate EC private key on P-256 curve
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

    # Serialize private key (raw bytes, 32 bytes for P-256)
    private_bytes = private_key.private_numbers().private_value.to_bytes(32, "big")
    private_b64 = base64.urlsafe_b64encode(private_bytes).rstrip(b"=").decode("utf-8")

    # Serialize public key (uncompressed point: 0x04 + X + Y = 65 bytes)
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )
    public_b64 = base64.urlsafe_b64encode(public_bytes).rstrip(b"=").decode("utf-8")

    print(f"\n✅ VAPID_PUBLIC_KEY  = {public_b64}")
    print(f"✅ VAPID_PRIVATE_KEY = {private_b64}")

    # Append to .env file
    env_path = Path(__file__).resolve().parent / ".env"
    env_content = env_path.read_text(encoding="utf-8") if env_path.exists() else ""

    lines = env_content.splitlines()
    # Remove any existing VAPID lines
    lines = [l for l in lines if not l.startswith("VAPID_PUBLIC_KEY") and not l.startswith("VAPID_PRIVATE_KEY") and not l.startswith("VAPID_SUBJECT")]
    lines.append(f'VAPID_PUBLIC_KEY="{public_b64}"')
    lines.append(f'VAPID_PRIVATE_KEY="{private_b64}"')
    lines.append('VAPID_SUBJECT="mailto:sentinel@aethershelf.app"')
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n📝 Keys saved to {env_path}")
    print("\n📋 Copy the VAPID_PUBLIC_KEY into public/sw.js and public/index.html")
    print('   Look for the placeholder: "YOUR_VAPID_PUBLIC_KEY_HERE"')
    print("\n⚠️  Keep VAPID_PRIVATE_KEY secret — it never leaves the server!\n")

    return public_b64, private_b64


if __name__ == "__main__":
    generate_vapid_keys()
