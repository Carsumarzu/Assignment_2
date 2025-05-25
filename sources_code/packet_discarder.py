# packet_discarder.py
import socket
import random
import argparse
import time

def main(listen_host, listen_port, dest_host, dest_port, discard_rate, verbose=False):
    """
    Listens for UDP packets, randomly discards some, and forwards the rest.

    Args:
        listen_host (str): The host IP to listen on (e.g., '0.0.0.0' for all interfaces).
        listen_port (int): The port to listen on for incoming packets from FFMPEG sender.
        dest_host (str): The destination host IP (Receiver PC).
        dest_port (int): The destination port on the Receiver PC.
        discard_rate (float): The probability of discarding a packet (e.g., 0.05 for 5%).
        verbose (bool): If True, print information about processed packets.
    """

    # --- 1. Create Sockets ---
    # Socket to listen for incoming packets from FFMPEG Sender
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        listen_sock.bind((listen_host, listen_port))
        print(f"[*] Listening on {listen_host}:{listen_port}")
    except socket.error as e:
        print(f"[!] Error binding to listen socket: {e}")
        return

    # Socket to send packets to the final FFMPEG Receiver
    # We don't need to bind this socket, just use it to send.
    forward_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[*] Forwarding packets to {dest_host}:{dest_port}")
    print(f"[*] Packet discard rate: {discard_rate*100:.2f}%")

    packet_count = 0
    discarded_count = 0

    try:
        while True:
            # --- 2. Receive Packet ---
            try:
                data, addr = listen_sock.recvfrom(65535) # Max UDP packet size
                packet_count += 1
                if verbose and packet_count % 100 == 0: # Print stats every 100 packets
                    print(f"\rProcessed: {packet_count}, Discarded: {discarded_count} ({discarded_count/packet_count*100 if packet_count > 0 else 0:.2f}%)", end="")

            except socket.timeout:
                # This can happen if listen_sock.settimeout() is used.
                # For now, we'll let it block indefinitely.
                continue
            except Exception as e:
                print(f"\n[!] Error receiving packet: {e}")
                continue

            # --- 3. Discard Logic ---
            if random.random() < discard_rate:
                discarded_count += 1
                if verbose:
                    # print(f"Packet from {addr} DISCARDED")
                    pass # Avoid too much console spam for discarded packets
                continue # Skip forwarding

            # --- 4. Forward Logic ---
            try:
                forward_sock.sendto(data, (dest_host, dest_port))
                if verbose:
                    # print(f"Packet from {addr} FORWARDED to {dest_host}:{dest_port}")
                    pass
            except Exception as e:
                print(f"\n[!] Error forwarding packet: {e}")

    except KeyboardInterrupt:
        print("\n[*] Program terminated by user.")
    finally:
        print(f"\n--- Stats ---")
        print(f"Total packets received: {packet_count}")
        print(f"Total packets discarded: {discarded_count}")
        if packet_count > 0:
            print(f"Actual discard percentage: {discarded_count/packet_count*100:.2f}%")
        listen_sock.close()
        forward_sock.close()
        print("[*] Sockets closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Packet Discarder/Forwarder")
    parser.add_argument("--listen_host", type=str, default="0.0.0.0",
                        help="Host IP to listen on (default: 0.0.0.0)")
    parser.add_argument("--listen_port", type=int, required=True,
                        help="Port to listen on for incoming packets from FFMPEG sender")
    parser.add_argument("--dest_host", type=str, required=True,
                        help="Destination host IP (Receiver PC)")
    parser.add_argument("--dest_port", type=int, required=True,
                        help="Destination port on the Receiver PC")
    parser.add_argument("--discard_rate", type=float, default=0.0,
                        help="Probability of discarding a packet (e.g., 0.05 for 5%, default: 0.0)")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")

    args = parser.parse_args()

    if not (0.0 <= args.discard_rate <= 1.0):
        print("[!] Error: Discard rate must be between 0.0 and 1.0")
    else:
        main(args.listen_host, args.listen_port, args.dest_host, args.dest_port, args.discard_rate, args.verbose)
