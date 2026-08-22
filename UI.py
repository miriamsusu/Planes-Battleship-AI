
class PlacementUI:
    def __init__(self, player_board, builder):
        self.board = player_board
        self.builder = builder

    def _get_user_input(self):
        user_input = input("\nEnter Head location (e.g., A 5): ").strip().split()
        if len(user_input) < 2:
            raise ValueError("Invalid format. Use 'Letter Number' (e.g., B 3).")

        row_letter = user_input[0].upper()
        col_num = int(user_input[1]) - 1

        row_idx = ord(row_letter) - ord('A')

        direction = input("Enter direction (UP, DOWN, LEFT, RIGHT): ").strip().upper()
        return row_idx, col_num, direction

    def run(self):
        planes_placed = 0
        print("--- PLANE PLACEMENT PHASE ---")

        while planes_placed < 3:
            print(self.board)
            print(f"Placing Plane {planes_placed + 1} of 3")

            try:
                row, col, direction = self._get_user_input()
                if self.builder.place_plane(row, col, direction):
                    print("Plane placed successfully!")
                    planes_placed += 1
                else:
                    print("Retry, your plane coordinates were not valid")

            except ValueError as e:
                print(f"Error: {e}. Try again.")
            except IndexError:
                print("Error: Coordinates are out of the A-J / 1-10 range.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        print("\nAll planes deployed!")
        print(self.board)


class GuessCoordsUI:
    def __init__(self, computer_board, player_board, player_logic, computer_logic, ai_agent):
        self._comp_board = computer_board
        self._player_board = player_board
        self._player_logic = player_logic
        self._comp_logic = computer_logic
        self._ai = ai_agent

    def get_user_input(self):
        try:
            user_input = input("\nYour Turn - Enter coordinates (e.g. A 6): ").strip().split()
            if len(user_input) < 2: return None, None

            row_idx = ord(user_input[0].upper()) - ord('A')
            col_num = int(user_input[1]) - 1
            return row_idx, col_num
        except (ValueError, IndexError):
            print("Invalid input format!")
            return None, None

    def run_logic(self):
        planes_down_by_player = 0
        planes_down_by_computer = 0
        turn = 0

        while planes_down_by_player < 3 and planes_down_by_computer < 3:
            if turn % 2 == 0:
                print("\n--- PLAYER ATTACK ---")
                r, c = self.get_user_input()
                if r is None: continue
                status = self._player_logic.try_coords(r, c)
                if status == "hit":
                    print("You hit a plane body!")
                elif status == "down":
                    planes_down_by_player += 1
                    print(f"You downed a plane! ({3 - planes_down_by_player} remaining)")
                elif status == "empty":
                    print("You missed")
            else:
                print("\n--- COMPUTER ATTACK ---")
                r, c = self._ai.get_move()
                status = self._comp_logic.try_coords(r, c)
                self._ai.process_result(r, c, status)

                row_letter = chr(ord('A') + r)
                print(f"Computer shot at {row_letter} {c + 1}...")

                if status == "hit":
                    print("The computer hit your plane!")
                elif status == "down":
                    planes_down_by_computer += 1
                    print(f"The computer downed one of your plane! ({3 - planes_down_by_computer} remaining)")
                elif status == "empty":
                    print("The computer missed.")
                print(self._player_board)
            turn += 1
        if planes_down_by_player == 3:
            print("\nYou won!")
        else:
            print("\nThe computer won!")