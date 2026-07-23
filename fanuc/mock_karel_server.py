#!/usr/bin/env python3
"""Serveur mock du controleur FANUC/KAREL, pour tester l'interface Node-RED
"Controle robot TCP" sans robot reel.

Il reproduit le meme protocole que fanuc/robot_tcp_server.kl :

  Commandes recues (ASCII brut, sans \\n) :
      "Jx:angle"  ex "J1:45"  -> deplace l'axe x de <angle> degres
      "HOME"                  -> retour a la position de repos
      "exit"                  -> ferme la connexion

  Reponses envoyees (champs separes par ';') :
      "<STATUT>;J1:v;...;J6:v"
  avec <STATUT> = "POSITION ATTEINTE" | "HORS LIMITES" | "EXIT OK"

Usage :
    python3 fanuc/mock_karel_server.py          # ecoute sur 0.0.0.0:59002
"""
import socketserver

HOST, PORT = "0.0.0.0", 59002
LIM_MIN, LIM_MAX = -180.0, 180.0
HOME = [0.0, -90.0, 90.0, 0.0, 0.0, 0.0]


class KarelHandler(socketserver.BaseRequestHandler):
    def handle(self):
        angles = list(HOME)
        print(f"[mock-karel] client connecte : {self.client_address}")
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            cmd = data.decode(errors="ignore").strip()
            if not cmd:
                continue
            print(f"[mock-karel] <- {cmd!r}")

            if cmd == "exit":
                self.request.sendall(b"EXIT OK")
                break
            elif cmd.upper().startswith("HOME"):
                angles = list(HOME)
                reply = self._reply("POSITION ATTEINTE", angles)
            elif cmd.startswith("J") and ":" in cmd:
                try:
                    idx = int(cmd[1:cmd.index(":")])
                    delta = float(cmd[cmd.index(":") + 1:])
                except ValueError:
                    reply = self._reply("COMMANDE INCONNUE", angles)
                    self.request.sendall(reply.encode())
                    continue
                target = angles[idx - 1] + delta
                if 1 <= idx <= 6 and LIM_MIN <= target <= LIM_MAX:
                    angles[idx - 1] = target
                    reply = self._reply("POSITION ATTEINTE", angles)
                else:
                    reply = self._reply("HORS LIMITES", angles)
            else:
                reply = self._reply("COMMANDE INCONNUE", angles)

            print(f"[mock-karel] -> {reply!r}")
            self.request.sendall(reply.encode())
        print("[mock-karel] client deconnecte")

    @staticmethod
    def _reply(statut, angles):
        pairs = ";".join(f"J{i + 1}:{a:.2f}" for i, a in enumerate(angles[:6]))
        return f"{statut};{pairs}"


if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), KarelHandler) as srv:
        srv.allow_reuse_address = True
        print(f"[mock-karel] serveur en ecoute sur {HOST}:{PORT}")
        srv.serve_forever()
