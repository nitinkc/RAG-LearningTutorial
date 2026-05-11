#!/usr/bin/env python3
"""
Standalone MongoDB Atlas connection diagnostic script.
Run this to isolate the connection issue.
"""

import sys
import ssl
import socket
from pymongo import MongoClient, errors
import pymongo

print("=" * 80)
print("MONGODB ATLAS CONNECTION DIAGNOSTIC")
print("=" * 80)

# 1. Environment Check
print("\n[Step 1] Environment Information")
print(f"  Python version: {sys.version}")
print(f"  PyMongo version: {pymongo.version}")
print(f"  OpenSSL version: {ssl.OPENSSL_VERSION}")

# 2. User input
print("\n[Step 2] Connection Details")
ATLAS_URI = input("Paste your MongoDB Atlas connection string: ").strip()
if not ATLAS_URI.startswith("mongodb"):
    print("❌ Invalid connection string. Must start with 'mongodb'")
    sys.exit(1)

# 3. Extract host info for debugging
print("\n[Step 3] Parsing Connection URI")
try:
    if "://" in ATLAS_URI:
        scheme, rest = ATLAS_URI.split("://", 1)
        if "@" in rest:
            creds, hosts_part = rest.split("@", 1)
            hosts = hosts_part.split("/")[0]
            host_list = hosts.split(",")
            print(f"  Scheme: {scheme}")
            print(f"  Hosts found: {host_list}")
            print(f"  First host: {host_list[0]}")
        else:
            print("  ❌ Could not parse credentials from URI")
except Exception as e:
    print(f"  ❌ Error parsing URI: {e}")

# 4. Raw TCP connectivity test
print("\n[Step 4] TCP Connectivity Test")
host_for_test = host_list[0] if 'host_list' in locals() else "localhost"
port = 27017
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((host_for_test, port))
    sock.close()
    if result == 0:
        print(f"  ✅ TCP connection to {host_for_test}:{port} succeeded")
    else:
        print(f"  ❌ TCP connection failed with code {result}")
except Exception as e:
    print(f"  ❌ TCP test error: {e}")

# 5. PyMongo connection without TLS
print("\n[Step 5] Connection Test WITHOUT TLS (should fail on Atlas)")
try:
    client = MongoClient(ATLAS_URI, serverSelectionTimeoutMS=5000, ssl=False)
    client.admin.command("ping")
    print("  ✅ Connected without TLS (unexpected — Atlas requires TLS)")
except errors.ServerSelectionTimeoutError as e:
    print(f"  ⚠️  Expected timeout without TLS: {str(e)[:100]}...")
except Exception as e:
    print(f"  ❌ Error: {type(e).__name__}: {str(e)[:100]}...")

# 6. PyMongo connection with standard TLS
print("\n[Step 6] Connection Test WITH TLS (standard)")
try:
    client = MongoClient(
        ATLAS_URI,
        serverSelectionTimeoutMS=10000,
        tls=True,
        tlsAllowInvalidCertificates=False
    )
    client.admin.command("ping")
    print("  ✅ Successfully connected to MongoDB Atlas with TLS!")
except errors.ServerSelectionTimeoutError as e:
    print(f"  ❌ Timeout with TLS: {str(e)[:200]}...")
except ssl.SSLError as e:
    print(f"  ❌ SSL Error: {type(e).__name__}")
    print(f"     Details: {str(e)[:200]}...")
except errors.OperationFailure as e:
    print(f"  ❌ Authentication failed: {str(e)[:200]}...")
except Exception as e:
    print(f"  ❌ Unexpected error: {type(e).__name__}: {str(e)[:200]}...")

# 7. PyMongo connection with tlsAllowInvalidCertificates=True (bypass proxy)
print("\n[Step 7] Connection Test WITH TLS + Certificate Bypass")
try:
    client = MongoClient(
        ATLAS_URI,
        serverSelectionTimeoutMS=10000,
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    client.admin.command("ping")
    print("  ✅ Successfully connected with certificate bypass!")
    print("     (This works on corporate networks with TLS inspection)")
except errors.ServerSelectionTimeoutError as e:
    print(f"  ❌ Still timeout even with bypass: {str(e)[:200]}...")
except ssl.SSLError as e:
    print(f"  ❌ SSL Error even with bypass: {type(e).__name__}: {str(e)[:200]}...")
except Exception as e:
    print(f"  ❌ Error: {type(e).__name__}: {str(e)[:200]}...")

# 8. Summary & recommendations
print("\n" + "=" * 80)
print("DIAGNOSIS SUMMARY")
print("=" * 80)
print("""
If Step 6 succeeded:
  ✅ Your connection is working. Use normal MongoClient(URI)

If Step 6 failed but Step 7 succeeded:
  ⚠️  Corporate TLS inspection detected.
  → Use: MongoClient(URI, tlsAllowInvalidCertificates=True)
  → OR: Connect to personal network (hotspot)

If both Step 6 & 7 failed:
  ❌ Check:
    1. Connection string is correct (user/pass/cluster name)
    2. IP allowlist in Atlas includes your current IP
    3. Database user exists and has correct password
    4. No firewall blocking port 27017
""")
print("=" * 80)

