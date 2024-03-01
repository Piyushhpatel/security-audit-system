import hashlib
import os
import datetime

# Path to the directory you want to scan
scan_directory = "E:\\"

# List of file paths containing SHA256 hashes
hash_files = [
    "hard_signatures/SHA256-Hashes_pack1.txt",
    "hard_signatures/SHA256-Hashes_pack2.txt",
    "hard_signatures/SHA256-Hashes_pack3.txt",
]

def load_hashes_from_files(hash_files):
    """Load SHA256 hashes from text files."""
    hashes = set()
    for file_path in hash_files:
        with open(file_path, "r") as f:
            hashes.update(line.strip() for line in f)
    return hashes

def calculate_hash(file_path, hash_algorithm="sha256", block_size=65536):
    """Calculate hash of a file."""
    hash_obj = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hash_obj.update(block)
    return hash_obj.hexdigest()

def scan_and_log_malware(directory, malware_hashes, log_file):
    """Scan files in the directory and log scan results."""
    total_files = 0
    healthy_files = 0
    suspicious_files = 0

    with open(log_file, "a") as log:
        log.write(f"Scan started at {datetime.datetime.now()}\n")
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                total_files += 1
                file_path = os.path.join(root, file_name)
                file_hash_sha256 = calculate_hash(file_path, "sha256")

                if file_hash_sha256 in malware_hashes:
                    log.write(f"Suspicious file found: {file_path}\n")
                    suspicious_files += 1
                else:
                    healthy_files += 1

                print(f"Scanning: {file_path}", end="\r")

    with open(log_file, "a") as log:
        log.write(f"Scan completed at {datetime.datetime.now()}\n")
        log.write(f"Total files scanned: {total_files}\n")
        log.write(f"Healthy files: {healthy_files}\n")
        log.write(f"Suspicious files: {suspicious_files}\n")
        log.write("Scan results:\n")

    print("\nScanning complete. Check the log.txt for details.")

if __name__ == "__main__":
    log_file = "log.txt"
    malware_hashes = load_hashes_from_files(hash_files)
    scan_and_log_malware(scan_directory, malware_hashes, log_file)