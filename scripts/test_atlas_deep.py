#!/usr/bin/env python3
"""
Deep MongoDB Atlas Diagnostic - find the exact problem
"""

import sys
import socket
import dns.resolver
from pymongo import MongoClient, errors
import pymongo

print("=" * 80)
print("MONGODB ATLAS DEEP DIAGNOSTIC")
print("=" * 80)

ATLAS_URI = input("\nPaste your MongoDB Atlas connection string: ").strip()

if not ATLAS_URI:
    print("❌ No connection string provided")
    sys.exit(1)

# Parse the URI
print("\n" + "=" * 80)
print("STEP 1: Parse Connection String")
print("=" * 80)

try:
    from pymongo.uri_parser import split_options
    from urllib.parse import urlparse

    # Extract components
    parsed = urlparse(ATLAS_URI)
    scheme = parsed.scheme
    netloc = parsed.netloc
    hostname = parsed.hostname
    username = parsed.username
    password = parsed.password

    print(f"✅ Successfully parsed URI")
    print(f"   Scheme: {scheme}")
    print(f"   Username: {username if username else '(none)'}")
    print(f"   Password: {'●' * len(password) if password else '(none)'}")
    print(f"   Hostname(s): {hostname}")

except Exception as e:
    print(f"❌ Failed to parse URI: {e}")
    sys.exit(1)

# Step 2: DNS Resolution
print("\n" + "=" * 80)
print("STEP 2: DNS Resolution")
print("=" * 80)

if scheme == "mongodb+srv":
    # For SRV records, we need to resolve _mongodb._tcp.<hostname>
    srv_name = f"_mongodb._tcp.{hostname}"
    print(f"Looking up SRV record: {srv_name}")

    try:
        answers = dns.resolver.resolve(srv_name, 'SRV')
        print(f"✅ SRV records found:")
        for rdata in answers:
            print(f"   Target: {rdata.target.to_unicode()} Port: {rdata.port}")
    except dns.resolver.NXDOMAIN:
        print(f"❌ SRV record NOT FOUND (NXDOMAIN)")
        print(f"   → Check your cluster name is correct")
        print(f"   → Check your cluster region is correct")
    except dns.resolver.NoNameservers:
        print(f"❌ No nameservers available")
        print(f"   → Your network may not have DNS access")
    except Exception as e:
        print(f"❌ DNS lookup failed: {type(e).__name__}: {e}")
else:
    # For mongodb:// we resolve the hostname directly
    print(f"Looking up A/AAAA records for: {hostname}")
    try:
        addr_info = socket.getaddrinfo(hostname, 27017, socket.AF_UNSPEC, socket.SOCK_STREAM)
        print(f"✅ Hostname resolves to:")
        for family, socktype, proto, canonname, sockaddr in addr_info:
            print(f"   {sockaddr[0]} (family: {family})")
    except socket.gaierror as e:
        print(f"❌ Hostname resolution failed: {e}")
    except Exception as e:
        print(f"❌ DNS lookup failed: {type(e).__name__}: {e}")

# Step 3: TCP Connectivity
print("\n" + "=" * 80)
print("STEP 3: TCP Connectivity")
print("=" * 80)

if hostname:
    print(f"Testing TCP connection to {hostname}:27017...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((hostname, 27017))
        sock.close()

        if result == 0:
            print(f"✅ TCP port 27017 is reachable")
        else:
            print(f"❌ TCP connection failed: {result}")
            print(f"   → Firewall may be blocking port 27017")
    except Exception as e:
        print(f"❌ TCP test error: {e}")

# Step 4: PyMongo Information
print("\n" + "=" * 80)
print("STEP 4: PyMongo Details")
print("=" * 80)

print(f"PyMongo version: {pymongo.version}")

# Try to connect with maximum debug info
print("\n" + "=" * 80)
print("STEP 5: Connection Attempt with Error Details")
print("=" * 80)

try:
    print("Attempting connection...")
    client = MongoClient(
        ATLAS_URI,
        serverSelectionTimeoutMS=15000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
    )

    print("Sending ping command...")
    result = client.admin.command("ping")
    print(f"✅ CONNECTION SUCCESSFUL!")
    print(f"   Response: {result}")

except errors.ServerSelectionTimeoutError as e:
    print(f"❌ SERVER SELECTION TIMEOUT")
    print(f"\nFull Error Details:")
    print(str(e))
    print("\n📋 Diagnostic Steps:")

    error_str = str(e)
    if "DNS" in error_str or "NXDOMAIN" in error_str or "nodename" in error_str:
        print("  1. DNS Issue detected")
        print("     → Verify cluster name (from Atlas → Connect)")
        print("     → Verify cluster region")
        print("     → Try: ping ac-bjhoinw-shard-00-00.zbnuw7o.mongodb.net")

    if "refused" in error_str.lower() or "connection reset" in error_str.lower():
        print("  2. Connection Refused")
        print("     → Cluster may not be running")
        print("     → Check in Atlas console if cluster is GREEN")
        print("     → Try restarting the cluster")

    if "authorization" in error_str.lower() or "auth" in error_str.lower():
        print("  3. Authentication Issue")
        print("     → Check username and password")
        print("     → Check user exists in Atlas (Security → Database Access)")

    if "network" in error_str.lower():
        print("  4. Network Issue")
        print("     → Check IP allowlist (Security → Network Access)")
        print("     → Your current IP must be in the list")
        print("     → You can temporarily allow 0.0.0.0/0 (all IPs) for testing")

except errors.OperationFailure as e:
    print(f"❌ OPERATION FAILED (likely auth)")
    print(f"Details: {e}")
    print("\nCheck:")
    print("  1. Username and password in connection string")
    print("  2. User exists in Atlas (Security → Database Access)")
    print("  3. User has 'readWrite' permission on 'admin' database")

except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {type(e).__name__}")
    print(f"Details: {e}")

print("\n" + "=" * 80)
print("INFORMATION TO VERIFY IN ATLAS CONSOLE")
print("=" * 80)
print("""
1. CLUSTER STATUS
   → Cloud.mongodb.com → Clusters
   → Your cluster should show a GREEN checkmark
   → If paused/stopped, click Resume

2. DATABASE USER
   → Cloud.mongodb.com → Security → Database Access
   → Verify user exists with correct username
   → Password must match (case-sensitive, special chars matter)
   → User must have 'readWrite' role

3. IP ALLOWLIST
   → Cloud.mongodb.com → Security → Network Access
   → Your current IP must be listed OR use 0.0.0.0/0 (TESTING ONLY)
   → Check your actual IP at: https://whatismyipaddress.com
   → OR allow all IPs temporarily to test

4. CONNECTION STRING
   → Cloud.mongodb.com → Clusters → Connect → Drivers → Python 3.12+
   → Copy the FULL string and use it as-is
   → Username/password must match your database user credentials

5. CLUSTER NAME
   → Verify the cluster name in your connection string matches Atlas
   → Example: ac-bjhoinw-shard-00-00.zbnuw7o is your cluster ID
""")

print("=" * 80)

