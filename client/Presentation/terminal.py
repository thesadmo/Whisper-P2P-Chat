
import curses
import asyncio
from client.Service.ServerAPI import ServerAPI


chat_messages = []
current_room = ""
my_username = ""


# update the chat screen with messages called from get_messages function
def show_messages(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, f"Room: {current_room}", curses.color_pair(2) | curses.A_BOLD)

    for i, message in enumerate(chat_messages, start=2):
        stdscr.addstr(i, 0, message, curses.color_pair(2))

    stdscr.refresh()

# get messages asynchronously
async def get_messages():
    global chat_messages
    while True:
        messages = api.get_messages()        # function from ServiceAPI to get msgs from the server
        if messages:
            chat_messages.extend(messages)
            
            curses.wrapper(show_messages)  # show messages on the screen
        await asyncio.sleep(1)

# user yb3t msg gdeda
def send_message(username, message):
    api.send_message(username, message)   # function from ServiceAPI

# Welcome screen
def welcome_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "WELCOME TO P2P CHAT APP",
                  curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "1. Sign up", curses.color_pair(3))
    stdscr.addstr(3, 0, "2. Log in", curses.color_pair(3))
    stdscr.addstr(5, 0, "Select an option (1/2): ")
    stdscr.refresh()
    choice = stdscr.getch()
    if choice == ord('1'):
        return "signup"
    elif choice == ord('2'):
        return "login"
    else:
        return "welcome"

# Signup screen
def signup_screen(stdscr):
    stdscr.clear()

    stdscr.addstr(0, 8, "Sign-Up", curses.color_pair(2) | curses.A_BOLD)

    stdscr.addstr(2, 0, "Enter your username: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    username = stdscr.getstr(3, 0, 30).decode('utf-8')

    stdscr.addstr(5, 0, "Enter your password: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.noecho()
    password = stdscr.getstr(6, 0, 30).decode('utf-8')

    stdscr.addstr(7, 0, "Confirm your password: ",
                  curses.color_pair(4) | curses.A_BOLD)
    confirm_password = stdscr.getstr(8, 0, 30).decode('utf-8')

    if password == confirm_password:
        if api.create_account(username, password):
            my_username= username
            stdscr.addstr(
                9, 0, "Account created successfully. Press any button to return.")
            return "home"
        else:
            stdscr.addstr(
                9, 0, "Username is taken. Press any button to return.")
        stdscr.getch()
        return "welcome"
    else:
        stdscr.addstr(
            9, 0, "Passwords do not match. Press any key to go back.")
        stdscr.getch()
        return "welcome"

# Login screen
def login_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "Log-In", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Enter your username: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    username = stdscr.getstr(3, 0, 30).decode('utf-8')

    stdscr.addstr(5, 0, "Enter your password: ",
                  curses.color_pair(4) | curses.A_BOLD)
    curses.noecho()
    password = stdscr.getstr(6, 0, 30).decode('utf-8')

    if api.login(username, password):
        my_username= username
        return "home"
    stdscr.addstr(
        9, 0, "Login failed. Press any key to go back.")
    stdscr.getch()
    return "welcome"

# Home screen
def home_screen(stdscr):
    stdscr.clear()
    stdscr.clear()

    stdscr.addstr(0, 8, "HOME", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "1. Create Room", curses.color_pair(5))
    stdscr.addstr(3, 0, "2. List Available Rooms", curses.color_pair(5))
    stdscr.addstr(4, 0, "3. Join Room", curses.color_pair(5))
    stdscr.addstr(5, 0, "4. List Users", curses.color_pair(5))
    stdscr.addstr(6, 0, "5. Private Chat", curses.color_pair(5))
    stdscr.addstr(7, 0, "6. Logout", curses.color_pair(5))
    stdscr.addstr(9, 0, "Select an option (1-6): ")
    stdscr.refresh()

    choice = stdscr.getch()
    if choice == ord('1'):
        return "create_room"
    elif choice == ord('2'):
        return "list_rooms"
    elif choice == ord('3'):
        return "join_room"
    elif choice == ord('4'):
        return "list_users"
    elif choice == ord('5'):
        return "private_chat"
    elif choice == ord('6'):
        api.logout()
        return None
    else:
        return "home"

# List rooms screen
def list_rooms_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "List Rooms", curses.color_pair(4) | curses.A_BOLD)

    available_rooms = ["Gaming Room", "Music Room",
                       "Studying Room", "Wael Ghonim Space"]

    for i, room_name in enumerate(available_rooms, start=2):
        stdscr.addstr(
            i, 0, f"{i-1}. Room Name: {room_name}", curses.color_pair(2))

    stdscr.addstr(len(available_rooms) + 5, 0, "Press 0 to go back to home.")
    stdscr.refresh()

    choice = stdscr.getch()
    if choice == ord('0'):
        return "home"
    else:
        return "list_rooms"

# List users screen
def list_users_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "List Users", curses.color_pair(4) | curses.A_BOLD)

    online_users = api.list_users()

    for i, user in enumerate(online_users, start=2):
        stdscr.addstr(i, 0, f"{i-1}. {user}", curses.color_pair(2))

    stdscr.addstr(len(online_users) + 5, 0, "Press 0 to go back to home.")
    stdscr.refresh()

    choice = stdscr.getch()
    if choice == ord('0'):
        return "home"
    else:
        return "list_users"

# Create room screen
def create_room_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "Create New Room", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Enter the room name: ", curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    room_name = stdscr.getstr(3, 0, 30).decode('utf-8')
    curses.noecho()

    if api.is_room_name_valid(room_name):
        api.create_room(room_name)
        stdscr.addstr(5, 0, f"Room '{room_name}' created successfully. Press any key to start chatting")
        stdscr.getch()  
        return "room_chatting"
    else:
        stdscr.addstr(5, 0, f"Invalid room name. Press any key to go back.")
        stdscr.getch()
        return "create_room"

# Join room screen
def join_room_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "Join Room", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Enter the room name: ", curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    room_name = stdscr.getstr(3, 0, 30).decode('utf-8')
    current_room= room_name
    curses.noecho()

    if api.is_room_name_valid(room_name):
        stdscr.addstr(5, 0, f"Joining room '{room_name}'...")
        stdscr.addstr(6, 0, "Press any key to start chatting")
        stdscr.getch()
        return "room_chatting"
    else:
        stdscr.addstr(5, 0, f"Room '{room_name}' is not available. Press any key to go back.")
        stdscr.getch()
        return "join_room"


def private_chat_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 8, "Join Private Chat", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Enter the username: ", curses.color_pair(4) | curses.A_BOLD)
    curses.echo()
    other_username = stdscr.getstr(3, 0, 30).decode('utf-8')
    curses.noecho()

    online_users = api.list_users()

    if other_username in online_users:  
        stdscr.addstr(5, 0, f"Joining private chat with '{other_username}'...")
        stdscr.addstr(6, 0, "Press any key to start chatting")
        stdscr.getch()
        return "private_chatting"  
    else:
        stdscr.addstr(5, 0, f"User '{other_username}' is not available. Press any key to go back.")
        stdscr.getch()
        return "private_chat"
    


async def room_chatting_screen(stdscr):
    global current_room, chat_messages
    stdscr.clear()
    stdscr.addstr(0, 8, f"Room: {current_room}", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 0, "Press 'q' to exit the room.", curses.color_pair(4) | curses.A_BOLD)

    # Display messages
    for i, message in enumerate(chat_messages, start=4):
        stdscr.addstr(i, 0, message, curses.color_pair(2))

    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('q'):       #press q to exit room
            return "home"
        elif key == ord('m'):     # press m to send a new msg
                        
            curses.echo()
            username = my_username
            message = input("Enter your message: ")
            curses.noecho()
            send_message(username, message)

            # Re-Update the screen with the msg that i just sent
            chat_messages.append(f"{username}: {message}")
            
            # clear screen then show all msgs ( old ones + the one i just made )

            stdscr.clear()
            stdscr.addstr(0, 8, f"Room: {current_room}", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(2, 0, "Press 'q' to exit the room.", curses.color_pair(4) | curses.A_BOLD)

            for i, msg in enumerate(chat_messages, start=4):
                stdscr.addstr(i, 0, msg, curses.color_pair(2))

            stdscr.refresh()



# main that uses async to be able to use the library functions
async def main(stdscr):
    global current_room, chat_messages

    api = ServerAPI(server_ip, server_port)
    
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.bkgd(curses.color_pair(1))

    current_screen = "welcome"
    is_running = True

    while is_running:
        if current_screen == "welcome":
            current_screen = welcome_screen(stdscr)
        elif current_screen == "signup":
            current_screen = signup_screen(stdscr)
        elif current_screen == "login":
            current_screen = login_screen(stdscr)
        elif current_screen == "home":
            current_screen = home_screen(stdscr)
        elif current_screen == "list_rooms":
            current_screen = list_rooms_screen(stdscr)
        elif current_screen == "list_users":
            current_screen = list_users_screen(stdscr)
        elif current_screen == "create_room":
            current_screen = create_room_screen(stdscr)  
        elif current_screen == "join_room":
            current_screen = join_room_screen(stdscr)
        elif current_screen == "private_chat":
            current_screen = private_chat_screen(stdscr)
        elif current_screen == "room_chatting":
            
            message_loop = asyncio.create_task(get_messages())   # start asynchronos loop to keep getting msgs 
            current_screen = await room_chatting_screen(stdscr)
            
            message_loop.cancel()        #close loop when leaving room 
        else:
            curses.endwin()
            is_running = False



if __name__ == "__main__":
    server_ip = input("Enter server ip: ")
    server_port = 12121
    curses.wrapper(main, server_ip, server_port)
