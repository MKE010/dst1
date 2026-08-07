import random
import hashlib
import time

# Import from your other files
from utils import clrScrn, wait, header
from data_structures import MyStack, H_Table, maxHeap, graphObj
from algorithms import run_dijkstra, myBfs

class GameEngine:
    def __init__(self):
        self.u = H_Table()
        self.lead = maxHeap()
        self.logged_in_user = None
        self.g = graphObj()
        
        edges = [
            ('A', 'B', 3), ('A', 'F', 6), ('B', 'C', 2), ('C', 'D', 5),
            ('D', 'E', 1), ('F', 'G', 4), ('F', 'J', 6), ('G', 'E', 3),
            ('G', 'W', 5), ('G', 'M', 4), ('J', 'K', 3), ('J', 'P', 5),
            ('K', 'W', 2), ('K', 'R', 3), ('W', 'M', 3), ('M', 'S', 1),
            ('O', 'P', 3), ('O', 'Q', 2), ('P', 'R', 1), ('R', 'S', 2),
            ('R', 'T', 4), ('S', 'U', 6), ('Q', 'T', 5), ('Q', 'V', 5),
            ('T', 'U', 2), ('U', 'V', 3)
        ]
        
        for e in edges:
            self.g.add(e[0], e[1], e[2])

        self.map_str = r"""
                  (B)----------2----------(C)----------5----------(D)
                 /                                                   \
                3                                                     1
               /                                                       \
             (A)----------6----------(F)----------4----------(G)----------3----------(E)
                                    /                        |  \
                                   6                         5   4
                                  /                          |    \
                                (J)------3------(K)----2----(W)-3-(M)
                                  \               \               /
                                   5               3             1
                                    \               \           /
                      (O)------3------(P)------1------(R)---2---(S)
                        \                             /           \
                         2                           4             6
                          \                         /               \
                           (Q)----------5---------(T)-------2-------(U)
                             \                                      /
                              5                                    3
                               \                                  /
                                \-----------(V) Goal-------------/
        """

    def crypt(self, p):
        return hashlib.sha256(p.encode()).hexdigest()

    def Start(self):
        while 1:
            clrScrn()
            header("RED RIDING HOOD ADVENTURE")
            print("            GRAPH PATH FINDING GAME             \n")
            print("            1. Login")
            print("            2. Register")
            print("            3. Leaderboard")
            print("            4. Exit\n")
            print("Select Option:")
            c = input("> ")

            if c == '1':
                res = self.do_login()
                if res == True:
                    self.play()
            elif c == '2':
                self.do_register()
            elif c == '3':
                self.show_lb()
            elif c == '4':
                clrScrn()
                break

    def do_register(self):
        clrScrn()
        header("ACCOUNT REGISTRATION")
        print("Enter new username:")
        un = input("> ")
        if self.u.check_exist(un) == True:
            print("\n[!] Error: Username already exists.")
            wait()
            return
        
        print("\nEnter password:")
        pw = input("> ")
        enc_pw = self.crypt(pw)
        self.u.insert(un, {"password": enc_pw, "total_score": 0})
        print("\n[OK] Account created successfully!")
        wait()

    def do_login(self):
        clrScrn()
        header("USER LOGIN")
        print("Username:")
        un = input("> ")
        print("\nPassword:")
        pw = input("> ")

        print("\nChecking User Database...\n")
        time.sleep(0.7)

        if self.u.check_exist(un) == False:
            print("[!] Error: Account not found.")
            wait()
            return False

        data = self.u.get(un)
        if data["password"] == self.crypt(pw):
            self.logged_in_user = un
            print("[OK] Account Found\n")
            time.sleep(0.5)
            print("Loading Saved Data...\n")
            print("Player         : " + str(un))
            print("Previous Score : " + str(data['total_score']) + "\n")
            print("Encryption:")
            print("SHA-256 Verification Successful\n")
            wait()
            return True
        else:
            print("[!] Error: Incorrect password.")
            wait()
            return False

    def show_lb(self):
        clrScrn()
        header("TOP PLAYERS", "(MAX HEAP DATA)")
        print("Rank       Username             Score")
        print("------------------------------------------------")
        
        t = self.lead.get_sorted()
        if len(t) == 0:
            print("No scores yet.")
        else:
            c = 1
            for p in t:
                print(f"#{c:<9} {p['username']:<20} {p['score']}")
                c = c + 1
        print()
        wait()

    def play(self):
        vl = []
        for n in self.g.nodes.keys():
            if n != 'V':
                vl.append(n)
                
        p_pos, w_pos = random.sample(vl, 2)
        tg = 'V'
        sc = 0
        undo_q = MyStack()
        
        usr_d = self.u.get(self.logged_in_user)
        tot = usr_d["total_score"]

        while 1:
            spath = run_dijkstra(self.g, p_pos, tg)
            s_next = None
            if len(spath) > 1:
                s_next = spath[1]

            clrScrn()
            header("RED RIDING HOOD", "GAME MAP")
            print("PLAYER INFO")
            print("---------------------------------")
            print("Name  : " + self.logged_in_user)
            print("Score : " + str(sc))
            print("HP    : ########## 100%\n")
            print("MAP")
            print(self.map_str)
            print("P = Player\nW = Wolf\nG = Grandma House (Node V)\n")
            
            print("Current Position:")
            print("Player : " + p_pos)
            print("Wolf   : " + w_pos)
            print("Goal   : " + tg + "\n")
            
            print("Path Algorithm : Dijkstra\n")
            print("Recommended Path:")
            j_str = ""
            for x in range(len(spath)):
                if x == len(spath)-1:
                    j_str += spath[x]
                else:
                    j_str += spath[x] + " -> "
            print(j_str)
            
            print("\nActions:")
            print("[1] Follow Path")
            print("[2] Choose Different Route")
            print("[3] Undo Move\n")
            
            choice = input("> ")

            old_p = p_pos
            n_list = []
            for n, w in self.g.get_adj(p_pos):
                n_list.append(n)
                
            did_move = False
            sc_add = 0

            if choice == '1':
                if s_next != None:
                    undo_q.push((p_pos, w_pos, sc))
                    p_pos = s_next
                    sc_add = 3
                    did_move = True
            elif choice == '2':
                j2 = ""
                for abc in n_list:
                    j2 += abc + ", "
                print("\nAvailable Neighbors: " + j2)
                c_move = input("Enter node to move to > ")
                c_move = c_move.strip().upper()
                if c_move in n_list:
                    undo_q.push((p_pos, w_pos, sc))
                    p_pos = c_move
                    if c_move == s_next:
                        sc_add = 3
                    else:
                        sc_add = 1
                    did_move = True
                else:
                    print("\n[!] Invalid Selection.")
                    time.sleep(1)
                    continue
            elif choice == '3':
                if undo_q.is_empty() == False:
                    data_back = undo_q.pop()
                    p_pos = data_back[0]
                    w_pos = data_back[1]
                    sc = data_back[2]
                    sc = sc - 2
                    print("\n[!] Undo successful. Penalty applied.")
                    time.sleep(1)
                    continue
                else:
                    print("\n[!] Cannot undo on the first turn.")
                    time.sleep(1)
                    continue
            else:
                continue

            if did_move == True:
                sc = sc + sc_add
                clrScrn()
                header("PLAYER MOVEMENT")
                print("Previous Position:")
                print(old_p)
                print("\nSelected Position:")
                print(p_pos)
                print("\nPath Evaluation")
                print("---------------------------------")
                print("Optimal Path:")
                if s_next != None:
                    print(old_p + " -> " + s_next)
                
                print("\nResult:")
                if p_pos == s_next:
                    print("[OK] Correct Decision\n")
                else:
                    print("[OK] Valid Alternate Route\n")
                print("Score +" + str(sc_add) + "\n")
                print("Current Score:")
                print(sc)
                print("\nUndo Move Available\n")
                wait()

            if p_pos == tg:
                sc = sc + 5
                self.end_scr("SUCCESS!", "Red Riding Hood reached Grandma's House", tot, sc)
                break
                
            if p_pos == w_pos:
                self.end_scr("GAME OVER", "The Wolf caught Red Riding Hood!", tot, sc)
                break

            d = random.randint(1, 6)
            old_w = w_pos
            did_w_move = False
            
            clrScrn()
            header("WOLF TURN")
            print("Enemy:\nWolf\n")
            print("Movement Algorithm:\nBFS\n")
            print("Movement Rule:\nOne Node Per Turn (Even=Move, Odd=Stay)\n")
            print("Dice Result:\n" + str(d) + "\n")

            if d % 2 == 0:
                print("Movement Allowed\n")
                w_path = myBfs(self.g, w_pos, p_pos)
                if len(w_path) > 1:
                    w_pos = w_path[1]
                    did_w_move = True
                print("Wolf Movement:")
                if did_w_move == True:
                    print(old_w + " -> " + w_pos + "\n")
                else:
                    print("Blocked / No Move\n")
            else:
                print("Movement Denied (Odd Roll)\n")
                print("Wolf Stays in Place\n")
            
            wait()

            if w_pos == p_pos:
                self.end_scr("GAME OVER", "The Wolf caught Red Riding Hood!", tot, sc)
                break

    def end_scr(self, stat, msg, p_s, g_s):
        n_tot = p_s + g_s
        
        ud = self.u.get(self.logged_in_user)
        ud["total_score"] = n_tot
        self.lead.insert(self.logged_in_user, n_tot)

        clrScrn()
        header("GAME RESULT")
        print("STATUS:\n" + stat + "\n")
        print(msg + "\n")
        print("FINAL SCORE REPORT")
        print("---------------------------------")
        print("Previous Score : " + str(p_s))
        print("Game Reward    : " + str(g_s))
        print("Final Score    : " + str(n_tot) + "\n")
        
        print("Saving Data...\n")
        time.sleep(0.5)
        print("[OK] Database Updated")
        print("[OK] BST Updated")
        print("[OK] MAX HEAP Updated\n")
        print("Thank You For Playing!\n")
        wait()