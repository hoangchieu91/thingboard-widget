import http.server
import socketserver
import os
import json
import sys

PORT = 8099

class SandboxRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/log_report':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                report = json.loads(post_data.decode('utf-8'))
                report_file = "/tmp/sandbox_widget_report.json"
                with open(report_file, "w") as f:
                    json.dump(report, f, indent=2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "saved": report_file}).encode('utf-8'))
                print(f" -> Saved AI Diagnostic Report to: {report_file}")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def main():
    sandbox_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(sandbox_dir)

    print("=================================================================")
    print(f"🚀 THINGSBOARD OFFLINE WORKBENCH WITH AI DIAGNOSTIC API:")
    print(f"   👉 http://localhost:{PORT}")
    print(f"   📋 AI Report File: /tmp/sandbox_widget_report.json")
    print("=================================================================")

    with ReusableTCPServer(("", PORT), SandboxRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping Sandbox server.")

if __name__ == "__main__":
    main()
